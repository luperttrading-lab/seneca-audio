"""Holperstellen in einer fertigen Kapitelaufnahme finden: tonpruef.py <ordner> <kapitel> [--json <datei>]

Arbeitet mit kapitelNN.wav (sonst .mp3) und kapitelNN.daten.json aus kapitel.py; pausen.stellen.json und woerter.json
nur, wenn vorhanden. Je Fund eine Zeile (Zeit m:ss in der fertigen Aufnahme, Art, Wörter, Messwert), am Ende die Summe;
--json schreibt die Funde als Liste {zeit (s), art, text, wert}. Whisper braucht auf der CPU einige Minuten.
Die Wortanfänge `t` stammen von Whisper und liegen mitunter 0,5 s daneben. Darum zählen zwei Zeitachsen: `t` und die
Wortanfänge, die Whisper hier auf der fertigen Aufnahme hört; Lücken und Dehnungen nur, wenn beide sie zeigen. Eine
Stille gehört zu dem Wort, dessen kräftige Sprache (über p95 − 25 dB, ohne Atem) überwiegend auf ihrer Seite liegt.
Prüfungen und Schwellen (abgestimmt am Testfall Kapitel 4, ältere Fassung; Kontrolle an den abgenommenen Kapiteln 5, 6):
1. Lücke ohne Satzzeichen: Stille ≥ LUECKE (10-ms-Rahmen unter p95 − 35 dB wie pausen2.py), nicht hinter einem Wort
   mit , . : ; ? ! – oder schließendem Anführungszeichen. Test: 4,5 „Gut | aufgehen:“ 0,56 s (Pause ein Wort zu früh).
2. Pause ohne Sprechpause: eingefügte Pause an , : ; – mit `vorher` < SPRECH_AB (Regel komma_ab, Nutzer 29.10./31.10.);
   dazu jede eingefügte Pause, die vor statt hinter ihrem Wort mit Satzzeichen sitzt. Kapitel 5: die zwei bekannten
   Doppelpunkte (0,14/0,12 s, PROTOKOLL 31.10.).
3. Gedehntes Wort: Sprechzeit (ohne Stille) je Zeichen + 2, robuste z-Werte gegen das Kapitel (Median, MAD) ≥ DEHNUNG;
   nur Wörter ohne Satzzeichen, davor dehnt jeder Sprecher. Test: 4,6 „Freundlichkeit und … eine“ +5,1; sonst bis +3,8
   (verschobene Wortanfänge), die abgenommenen Kapitel 5 und 6 bis +3,2.
Bekannter Fehlalarm (Test, 0:53): „Oder: [Pause] Es ist“ wird als „Oder: „Es | ist“ gemeldet (Lücke und Dehnung), weil
beide Whisper-Zeitachsen „Es“ in die zweite Silbe von „Oder“ legen. Die Liste ersetzt das Ohr nicht, sie zeigt, wo zuerst.
4. Falsche Satzgrenze: Whisper (large-v3-turbo) setzt einen Punkt, wo der Text ein Komma oder nichts hat; die Pause
   klingt dann wie ein Satzende (4,6 „Freude, | dazu“). Whisper läuft dafür Satz für Satz: Mit zwei Sätzen Zusammenhang
   setzte es dort ein Komma, weil der Sinn dann mehr zählt als der Ton.
5. Knackser: Sprung im Signal, gemessen über 16,5 kHz. Dort hat die Stimme nichts (ElevenLabs liefert MP3 bis 16 kHz),
   ein Sprung aber schon. Die bloße Differenz zweier Abtastwerte taugt nicht: Sprechansätze nach Stille (d, t) springen
   in den abgenommenen Kapiteln weiter über den örtlichen Pegel als ein Schnitt ohne Blende. Schwelle KNACKS gegen den
   Sprachpegel (p95), in der Pause (2–20 ms beiderseits still) KNACKS_PAUSE. Probe mit künstlichen Schnitten ohne Blende
   in Kapitel 6: Sprünge 0,07 bis 0,2 bei −33 bis −27 dB gefunden, 0,05 (−37 dB) nicht; Knack 0,01 in einer Pause −43 dB.
   Sprechansätze erreichen im Test bis −39 dB, in Kapitel 5 und 6 bis −45 dB; in Pausen nichts über −60 dB.
"""
import difflib, json, os, re, subprocess, sys
import numpy as np

SR, TEMPO, R10 = 44100, 0.96, 441                 # Abtastrate, Tempo der Kette (kette.py), 10-ms-Rahmen
LUECKE = 0.25                                     # s Stille ohne Satzzeichen
SPRECH_AB = 0.15                                  # s echte Sprechpause, ab der eine Pause eingefügt werden darf
DEHNUNG = 4.0                                     # robuste z-Werte (MAD) über dem Kapitel
KNACKS, KNACKS_PAUSE = -35, -55                   # dB Spitze über 16,5 kHz gegen den Sprachpegel; in der Pause
SCHLUSS = "“”»«‹›\"')]"                            # schließende Anführungszeichen und Klammern
norm = lambda w: re.sub(r"[^a-zäöü0-9]", "", w.lower().replace("ß", "ss"))
zeichen = lambda w: next((c for c in (w.rstrip(SCHLUSS)[-1:], w[-1:]) if c and c in ",.:;?!–…" + SCHLUSS), "")   # "" ohne Zeichen
mmss = lambda s: f"{int(s // 60)}:{int(s % 60):02d}"


def lade(f, sr=SR):
    return np.frombuffer(subprocess.run(["ffmpeg", "-nostdin", "-loglevel", "error", "-i", f, "-ac", "1", "-ar", str(sr), "-f", "s16le", "-"],
                                        capture_output=True, check=True).stdout, np.int16).astype(np.float64) / 32768


def pegel_db(x):   # je 10-ms-Rahmen in dB
    return 10 * np.log10((x[:len(x) // R10 * R10].reshape(-1, R10) ** 2).mean(1) + 1e-12)


def stille(db):   # je Rahmen: still? (Schwelle wie pausen2.py, relativ zum Sprachpegel des Kapitels)
    return db < max(np.percentile(db, 95) - 35, np.percentile(db, 10) + 6)


def laeufe(still, ab):   # zusammenhängende Stillen ≥ ab Sekunden: [(von, bis)]
    d = np.diff(np.concatenate([[0], still.astype(int), [0]])); a, e = np.flatnonzero(d == 1), np.flatnonzero(d == -1)
    return [(i * 0.01, j * 0.01) for i, j in zip(a, e) if (j - i) * 0.01 >= ab - 1e-9]


def sprechzeit(still, a, b):   # Sekunden Sprache (nicht stille Rahmen) zwischen a und b
    i, j = max(0, int(round(a * 100))), min(len(still), int(round(b * 100)))
    return 0.01 * int((~still[i:j]).sum()) if j > i else 0.0


def grenze(s0, s1, t, laut):   # Stille (s0, s1) liegt zwischen Wort k und k+1; k = −1 vor dem ersten Wort
    drin = [i for i in range(len(t)) if s0 - 0.02 <= t[i] <= s1 + 0.02]
    if drin: return drin[0] - 1   # ein Wortanfang in der Stille: sie steht vor diesem Wort
    k = int(np.searchsorted(t, s0, side="right")) - 1   # Stille im Bereich von Wort k (t[k] < s0, t[k+1] > s1)
    if k < 0: return -1
    bis = t[k + 1] if k + 1 < len(t) else s1 + 2
    vor, nach = sprechzeit(~laut, t[k], s0), sprechzeit(~laut, s1, bis)   # nur kräftige Sprache, kein Atem
    return k if vor >= nach else k - 1   # das Wort liegt überwiegend hinter der Stille: sie steht davor


def umgebung(w, k, mitte=" | ", n=2):   # Wörter um die Grenze hinter Wort k
    return "… " + " ".join(w[max(0, k - n + 1):k + 1]) + mitte + " ".join(w[k + 1:k + 1 + n]) + " …"


def wort_umgebung(w, i, n=2):   # Wörter um Wort i, das Wort selbst in Klammern
    return "… " + " ".join(w[max(0, i - n):i] + [f"[{w[i]}]"] + w[i + 1:i + 1 + n]) + " …"


def whisper(ton, t, w, still, laut):   # Whisper-Wörter mit Satzzeichen: [(wort, von, bis, stückende)]
    from faster_whisper import WhisperModel
    a = lade(ton, 16000).astype(np.float32); dauer = len(a) / 16000
    # Satz für Satz, geschnitten in der Mitte der Pause nach einem Satzende des Texts; Sätze über 25 s notfalls
    # an anderen Pausen (das letzte Wort eines solchen Stücks zählt nicht: Whisper beendet jedes Stück mit Punkt)
    kand = []
    for s0, s1 in laeufe(still, 0.3):
        k = grenze(s0, s1, t, laut)
        if 0 <= k < len(w) - 1: kand.append(((s0 + s1) / 2, zeichen(w[k]) in {".", "?", "!", "…"}))
    schnitte = [0.0] + [z for z, ende in kand if ende] + [dauer]; i = 0
    while i < len(schnitte) - 1:
        if schnitte[i + 1] - schnitte[i] > 25:
            c = [z for z, _ in kand if 3 < z - schnitte[i] <= 25 and z < schnitte[i + 1] - 3]
            if c: schnitte.insert(i + 1, max(c))
        i += 1
    m = WhisperModel("large-v3-turbo", device="cpu", compute_type="int8", cpu_threads=4); erg = []
    for s0, s1 in zip(schnitte[:-1], schnitte[1:]):
        segs, _ = m.transcribe(a[int(s0 * 16000):int(s1 * 16000)], language="de", beam_size=5, word_timestamps=True,
                               condition_on_previous_text=False, vad_filter=False)
        stueck = [(x.word.strip(), s0 + x.start, s0 + x.end, False) for s in segs for x in s.words if norm(x.word)]
        if stueck: stueck[-1] = stueck[-1][:3] + (True,)
        erg += stueck
    return erg


def zuordnung(w, H):   # Textwort i → Index des Whisper-Worts (oder None)
    j_von = [None] * len(w)
    sm = difflib.SequenceMatcher(None, [norm(v) for v in w], [norm(h[0]) for h in H], autojunk=False)
    for op, i1, i2, j1, j2 in sm.get_opcodes():
        if op == "equal" or (op == "replace" and i2 - i1 == j2 - j1):
            for k in range(i2 - i1): j_von[i1 + k] = j1 + k
    return j_von


def fund(zeit, art, text, wert, muster):   # muster: Messwert für die Zeile, etwa "{:.2f} s"
    return {"zeit": round(float(zeit), 2), "art": art, "text": text, "wert": round(float(wert), 2), "anzeige": muster.format(wert).replace(".", ",")}


def pausen(b, t, t2, w, still, laut):   # Prüfung 2; None, wenn pausen.stellen.json oder woerter.json fehlt
    if not (os.path.exists(b + ".pausen.stellen.json") and os.path.exists(b + ".woerter.json")): return None, []
    E = json.load(open(b + ".pausen.stellen.json")); W = json.load(open(b + ".woerter.json", encoding="utf-8"))
    if len(W) != len(t): return None, []
    schieb = lambda s: s + sum(e["L"] for e in E if e["orig"] < s)
    off = float(np.median([t[k] * TEMPO - schieb(W[k]["s"]) for k in range(len(W))]))   # Kopf und Vorlauf (kapitel.py)
    erg, belegt, S = [], [], laeufe(still, 0.05)
    for e in E:
        mit = [k for k in range(len(W)) if W[k]["s"] <= e["orig"] and zeichen(W[k]["w"]) in set(",.:;?!–…")]   # wie pausen2.py
        if not mit: continue
        i = mit[-1]; a = (schieb(e["orig"]) - e["xf"] + off) / TEMPO; z = a + (e["L"] + 2 * e["xf"]) / TEMPO
        ohne = e["z"] in ",:;–" and e["vorher"] < SPRECH_AB; frueh = 0   # frueh: Wörter, die die Pause zu früh sitzt
        ueber = [(min(z, s1) - max(a, s0), s0, s1) for s0, s1 in S if min(z, s1) > max(a, s0)]
        if ueber:
            _, s0, s1 = max(ueber); k1, k2 = grenze(s0, s1, t, laut), grenze(s0, s1, t2, laut)
            if k1 < i and k2 < i: frueh = i - k1; a = s0; belegt.append((s0, s1))
        zf = f"{frueh} Wort zu früh" if frueh == 1 else f"{frueh} Wörter zu früh"
        if ohne: erg.append(fund(a, "Pause ohne Sprechpause", umgebung(w, i - frueh), e["vorher"], "gesprochen {:.2f} s" + (", " + zf if frueh else "")))
        elif frueh: erg.append(fund(a, "Pause vor dem Satzzeichen", umgebung(w, i - frueh), frueh, zf))
    return belegt, erg


def luecken(t, t2, w, still, laut, belegt):   # Prüfung 1
    erg = []
    for s0, s1 in laeufe(still, LUECKE):
        if any(min(s1, b1) > max(s0, b0) for b0, b1 in belegt): continue
        k1, k2 = grenze(s0, s1, t, laut), grenze(s0, s1, t2, laut)
        if all(0 <= k < len(w) - 1 and not zeichen(w[k]) for k in (k1, k2)):
            erg.append(fund(s0, "Lücke ohne Satzzeichen", umgebung(w, k1), s1 - s0, "{:.2f} s"))
    return erg


def dehnung(t, t2, w, still, ende):   # Prüfung 3: Sprechzeit je Zeichen, robuste z-Werte; beide Zeitachsen
    n = len(w); L = np.array([len(norm(v)) for v in w]); frei = np.array([i for i in range(n) if not zeichen(w[i])])
    z = []
    for tt in (t, t2):
        r = np.array([sprechzeit(still, tt[i], tt[i + 1] if i + 1 < n else ende) for i in range(n)]) / (L + 2)
        m = np.median(r[frei]); z.append((r - m) / max(1.4826 * np.median(np.abs(r[frei] - m)), 1e-6))
    zm = np.minimum(*z)
    return [fund(t[i], "gedehntes Wort", wort_umgebung(w, i), zm[i], "{:+.1f} MAD über dem Median") for i in frei if zm[i] >= DEHNUNG]


def satzgrenzen(t, w, H, j_von, still):   # Prüfung 4
    erg = []
    for i, j in enumerate(j_von[:-1]):
        if j is None or H[j][3] or H[j][0].rstrip(SCHLUSS)[-1:] not in {".", "?", "!"} or zeichen(w[i]) not in ("", ","): continue
        bis = H[j + 1][1] if j + 1 < len(H) else H[j][2]
        p = max([s1 - s0 for s0, s1 in laeufe(still, 0.05) if s1 > H[j][2] - 0.2 and s0 < bis + 0.2] or [0])
        erg.append(fund(H[j][2], "Satzende gehört", umgebung(w, i) + f" (Whisper: „{H[j][0]}“)", p, "Pause {:.2f} s"))
    return erg


def knackser(x, db, t, w):   # Prüfung 5: Spitzen über 16,5 kHz, gegen den Sprachpegel (p95 der 10-ms-Rahmen)
    X = np.fft.rfft(x); X[np.fft.rfftfreq(len(x), 1 / SR) < 16500] = 0; h = np.abs(np.fft.irfft(X, len(x)))
    ref = np.percentile(db, 95); ruhig = max(ref - 35, np.percentile(db, 10) + 6); erg, letzte = [], -SR
    leise = lambda s: 10 * np.log10(np.mean(s ** 2) + 1e-12) < ruhig if len(s) else True
    B = h[:len(h) // R10 * R10].reshape(-1, R10)   # je 10-ms-Rahmen die Spitze
    for r in np.flatnonzero(B.max(1) > 10 ** ((ref + KNACKS_PAUSE) / 20)):
        j = r * R10 + int(np.argmax(B[r])); spitze = 20 * np.log10(h[j]) - ref
        pause = leise(x[max(0, j - 882):max(0, j - 88)]) and leise(x[j + 88:j + 882])   # 2–20 ms beiderseits still
        if spitze < (KNACKS_PAUSE if pause else KNACKS): continue
        if j - letzte > SR * 0.05: erg.append(None)
        if erg[-1] is None or spitze > erg[-1]["wert"]:   # je 50 ms nur die höchste Spitze
            k = max(0, int(np.searchsorted(t, j / SR)) - 1)
            erg[-1] = fund(j / SR, "Knackser" + (" in der Pause" if pause else ""), wort_umgebung(w, k), spitze, "{:+.1f} dB zum Sprachpegel")
        letzte = j
    return erg


def pruefe(ordner, kap, H=None):
    b = os.path.join(ordner, f"kapitel{kap:02d}"); ton = b + ".wav" if os.path.exists(b + ".wav") else b + ".mp3"
    D = json.load(open(b + ".daten.json", encoding="utf-8")); t = D["t"]; w = [re.sub(r"[\[\]]", "", v) for v in D["w"]]
    x = lade(ton); db = pegel_db(x); still = stille(db); laut = db >= np.percentile(db, 95) - 25
    if H is None: H = whisper(ton, t, w, still, laut)
    j_von = zuordnung(w, H)
    t2 = np.maximum.accumulate([H[j][1] if j is not None else t[i] for i, j in enumerate(j_von)])   # Whisper hier
    belegt, f2 = pausen(b, t, t2, w, still, laut)
    lu, sg = luecken(t, t2, w, still, laut, belegt or []), satzgrenzen(t, w, H, j_von, still)
    for f in lu:   # Lücke, die Whisper auch als Satzende hört: eine Stelle
        for g in [g for g in sg if abs(g["zeit"] - f["zeit"]) < 0.6]: f["text"] += g["text"][g["text"].rfind(" (Whisper"):]; sg.remove(g)
    funde = f2 + lu + dehnung(t, t2, w, still, D["ende"]) + sg + knackser(x, db, t, w)
    info = {"ton": os.path.basename(ton), "pausen": belegt is not None, "whisper": sum(j is not None for j in j_von), "woerter": len(w)}
    return sorted(funde, key=lambda f: f["zeit"]), info


if __name__ == "__main__":
    argv = sys.argv[1:]; aus = None
    if "--json" in argv: i = argv.index("--json"); aus = argv[i + 1]; del argv[i:i + 2]
    funde, info = pruefe(argv[0], int(argv[1]))
    for f in funde:
        print(f"{mmss(f['zeit'])}  {f['art']:<26} {f['text']}  {f['anzeige']}")
    arten = {}
    for f in funde: arten[f["art"]] = arten.get(f["art"], 0) + 1
    print(f"Kapitel {int(argv[1])}: {len(funde)} Stellen" + (" (" + ", ".join(f"{a} {n}" for a, n in arten.items()) + ")" if funde else "")
          + f"; {info['ton']}, Whisper {info['whisper']}/{info['woerter']} Wörter zugeordnet"
          + ("" if info["pausen"] else ", ohne Prüfung 2 (keine passende pausen.stellen.json mit woerter.json)"))
    if aus: json.dump([{k: f[k] for k in ("zeit", "art", "text", "wert")} for f in funde], open(aus, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
