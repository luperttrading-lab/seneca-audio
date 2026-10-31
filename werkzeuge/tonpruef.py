"""Holperstellen in einer fertigen Kapitelaufnahme finden: tonpruef.py <ordner> <kapitel> [--json <datei>]

Arbeitet mit kapitelNN.wav (sonst .mp3) und kapitelNN.daten.json aus kapitel.py; pausen.stellen.json und woerter.json
nur, wenn vorhanden. Wortzeiten `t` sind Whisper-Anfänge und liegen oft bis 0,5 s daneben (meist früh, am Ende des
vorigen Wortes). Eine Stille wird darum dem Wort zugeordnet, dessen Sprechanteil überwiegend auf ihrer Seite liegt.
Prüfungen (Schwellen am Testfall Kapitel 4, ältere Fassung, abgestimmt; Kontrolle an den abgenommenen Kapiteln 5 und 6):
1. Lücke ohne Satzzeichen: Stille ≥ LUECKE (10-ms-Rahmen unter Sprachpegel p95 − 35 dB wie pausen2.py), nicht hinter
   einem Wort mit , . : ; ? ! – (4,5 „Gut | aufgehen:“, eingefügte Pause ein Wort zu früh).
2. Pause ohne Sprechpause: eingefügte Pause an , : ; – mit `vorher` < SPRECH_AB (Regel komma_ab, Nutzer 29.10./31.10.),
   und eingefügte Pausen, die nicht hinter ihrem Wort mit Satzzeichen sitzen.
3. Gedehntes Wort: Sprechzeit des Wortes (ohne Stille) gegen die Zeichenzahl, robust gegen das Kapitel (Median, MAD).
4. Falsche Satzgrenze: Whisper (large-v3-turbo) setzt einen Punkt, wo der Text ein Komma oder nichts hat; die Pause
   klingt dann wie ein Satzende (4,6 „Freude, | dazu“).
5. Knackser: Sprung zwischen zwei Abtastwerten weit über dem örtlichen Pegel.
"""
import difflib, json, os, re, subprocess, sys
import numpy as np

SR, TEMPO, R10 = 44100, 0.96, 441                 # Abtastrate, Tempo der Kette (kette.py), 10-ms-Rahmen
LUECKE = 0.25                                     # s Stille ohne Satzzeichen
SPRECH_AB = 0.15                                  # s echte Sprechpause, ab der eine Pause eingefügt werden darf
SCHLUSS = "“”»«‹›\"')]"                            # schließende Anführungszeichen und Klammern
norm = lambda w: re.sub(r"[^a-zäöü0-9]", "", w.lower().replace("ß", "ss"))
zeichen = lambda w: w.rstrip(SCHLUSS)[-1:] if w.rstrip(SCHLUSS)[-1:] in ",.:;?!–…" else ""
mmss = lambda s: f"{int(s // 60)}:{s % 60:05.2f}"


def lade(f, sr=SR):
    return np.frombuffer(subprocess.run(["ffmpeg", "-nostdin", "-loglevel", "error", "-i", f, "-ac", "1", "-ar", str(sr), "-f", "s16le", "-"],
                                        capture_output=True, check=True).stdout, np.int16).astype(np.float64) / 32768


def stille(x):   # je 10-ms-Rahmen: still? (Schwelle wie pausen2.py, relativ zum Sprachpegel des Kapitels)
    db = 10 * np.log10((x[:len(x) // R10 * R10].reshape(-1, R10) ** 2).mean(1) + 1e-12)
    return db < max(np.percentile(db, 95) - 35, np.percentile(db, 10) + 6)


def laeufe(still, ab):   # zusammenhängende Stillen ≥ ab Sekunden: [(von, bis)]
    d = np.diff(np.concatenate([[0], still.astype(int), [0]])); a, e = np.flatnonzero(d == 1), np.flatnonzero(d == -1)
    return [(i * 0.01, j * 0.01) for i, j in zip(a, e) if (j - i) * 0.01 >= ab - 1e-9]


def sprechzeit(still, a, b):   # Sekunden Sprache (nicht stille Rahmen) zwischen a und b
    i, j = max(0, int(round(a * 100))), min(len(still), int(round(b * 100)))
    return 0.01 * int((~still[i:j]).sum()) if j > i else 0.0


def grenze(s0, s1, t, still):   # Stille (s0, s1) liegt zwischen Wort k und k+1; k = −1 vor dem ersten Wort
    drin = [i for i in range(len(t)) if s0 - 0.02 <= t[i] <= s1 + 0.02]
    if drin: return drin[0] - 1   # ein Wortanfang in der Stille: sie steht vor diesem Wort
    k = int(np.searchsorted(t, s0, side="right")) - 1   # Stille im Bereich von Wort k (t[k] < s0, t[k+1] > s1)
    if k < 0: return -1
    bis = t[k + 1] if k + 1 < len(t) else s1 + 2
    vor, nach = sprechzeit(still, t[k], s0), sprechzeit(still, s1, bis)
    return k if vor >= nach else k - 1   # das Wort liegt überwiegend hinter der Stille: sie steht davor


def whisper(f, t, w, still):   # Whisper-Wörter mit Satzzeichen auf der fertigen Aufnahme: [(wort, von, bis, stückende)]
    from faster_whisper import WhisperModel
    a = lade(f, 16000).astype(np.float32); dauer = len(a) / 16000
    # Stücke ≤ 25 s (Whisper überspringt in langen Dateien sonst Passagen), geschnitten an Satzenden des Texts,
    # damit das erzwungene Stückende keinen falschen Punkt erzeugt; nur notfalls an anderen Pausen
    kand = []
    for s0, s1 in laeufe(still, 0.3):
        k = grenze(s0, s1, t, still)
        if 0 <= k < len(w) - 1: kand.append(((s0 + s1) / 2, zeichen(w[k]) in ".?!…"))
    schnitte = [0.0]
    while dauer - schnitte[-1] > 28:
        c = [(z, ende) for z, ende in kand if 3 < z - schnitte[-1] <= 25]
        if not c: break
        schnitte.append(max(z for z, ende in c if ende) if any(e for _, e in c) else max(z for z, _ in c))
    schnitte.append(dauer)
    m = WhisperModel("large-v3-turbo", device="cpu", compute_type="int8", cpu_threads=4); erg = []
    for s0, s1 in zip(schnitte[:-1], schnitte[1:]):
        segs, _ = m.transcribe(a[int(s0 * 16000):int(s1 * 16000)], language="de", beam_size=5, word_timestamps=True,
                               condition_on_previous_text=False, vad_filter=False)
        stueck = [(x.word.strip(), s0 + x.start, s0 + x.end, False) for s in segs for x in s.words if norm(x.word)]
        if stueck: stueck[-1] = stueck[-1][:3] + (True,)
        erg += stueck
    return erg
