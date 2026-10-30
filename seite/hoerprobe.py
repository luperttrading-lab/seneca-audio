"""Hörprobe eines Kapitels für den Auftraggeber: hoerprobe.py <kapitel> <ordner> <ausordner>

<ordner> ist der Ausordner von werkzeuge/kapitel.py (kapitelNN.mp3, .daten.json, .roh.mp3, .woerter.json, lauf.log).
Baut eine Seite (Vorlage seite/hoerprobe_vorlage.html) mit dem ganzen Kapitel, je einer Tafel pro Paragraf und den
Stellen, die der Betonungsfilter markiert; Text läuft mit, die markierten Wörter haben eine Wellenlinie. Ausgabe:
<ausordner>/index.html und audio/*.mp3, zum Veröffentlichen als Artifact (PLAN.md, Ablauf Schritt 3).
"""
import html, json, os, re, subprocess, sys

HIER = os.path.dirname(os.path.abspath(__file__)); R = os.path.dirname(HIER); sys.path.insert(0, os.path.join(R, "werkzeuge"))
import betonung
from kette import abweichungen, bestaetigt, pnorm

kap, ordner, aus = int(sys.argv[1]), sys.argv[2], sys.argv[3]
b = os.path.join(ordner, f"kapitel{kap:02d}"); os.makedirs(os.path.join(aus, "audio"), exist_ok=True)
D = json.load(open(b + ".daten.json", encoding="utf-8")); W = json.load(open(b + ".woerter.json", encoding="utf-8"))
assert [w["w"] for w in W] == D["w"]
E = betonung.pruefe(b + ".roh.mp3", W); M = [e for e in E if e["markiert"]]
knapp = sum(1 for e in E if not e["markiert"] and betonung.betonung_klein(e) and 3 <= e["abstand"] < 5)
log = open(os.path.join(ordner, "lauf.log"), encoding="utf-8").read() if os.path.exists(os.path.join(ordner, "lauf.log")) else ""
treu = next((z for z in log.splitlines()[::-1] if "Gegenprobe" in z or "large-v3-turbo" in z), "")
pausen = next((z for z in log.splitlines() if "Pausen verlängert" in z), "")
credits = next((z for z in log.splitlines() if "Credits" in z), "")
mm = lambda s: f"{int(s // 60)}:{int(s % 60):02d}"
esc = html.escape


def schneide(name, a, e):
    subprocess.run(["ffmpeg", "-nostdin", "-y", "-loglevel", "error", "-ss", f"{a:.3f}", "-to", f"{e:.3f}", "-i", b + ".mp3",
                    "-af", "afade=t=in:d=0.03,areverse,afade=t=in:d=0.08,areverse", "-b:a", "128k", os.path.join(aus, "audio", name)], check=True)


def eintrag(datei, i0, i1, a, e, mark=()):
    return {"datei": "audio/" + datei, "dauer": round(e - a, 3), "w": [{"w": D["w"][i], "t": round(D["t"][i] - a, 3)} for i in range(i0, i1 + 1)],
            "mark": [m - i0 for m in mark]}


def tafel(k, titel, unter, befund=""):
    t = f'''  <section class="stelle" id="{k}" data-an="false" aria-labelledby="t-{k}">
    <div class="zeile">
      <button type="button" class="knopf" data-k="{k}" data-name="{esc(titel)}" aria-label="{esc(titel)} abspielen"></button>
      <div class="titel"><b id="t-{k}">{esc(titel)}</b><span>{esc(unter)}</span></div>
    </div>
    <p class="text" data-text="{k}"></p>
    <div class="balken"><i data-balken="{k}"></i></div>'''
    return t + (f"\n    <dl><dt>Filter</dt><dd>{befund}</dd></dl>" if befund else "") + "\n  </section>"


S, teile = {}, []
markiert = {e["i0"] + e["pos"] for e in M}
subprocess.run(["cp", b + ".mp3", os.path.join(aus, "audio", f"kapitel{kap:02d}.mp3")], check=True)
S["ganz"] = eintrag(f"kapitel{kap:02d}.mp3", 0, len(D["w"]) - 1, 0, D["ende"], sorted(markiert)); S["ganz"]["datei"] = f"audio/kapitel{kap:02d}.mp3"
teile.append(tafel("ganz", f"Kapitel {kap} ganz", f"{mm(D['ende'])} · Helmut Stieglbauer, Tempo 0,96"))
# je Paragraf
stellen_ = sorted(set(D["stelle"]), key=lambda s: int(s.split(",")[1]))
teile.append('  <h2 class="abschnitt">Paragraf für Paragraf</h2>')
for st in stellen_:
    idx = [i for i, s in enumerate(D["stelle"]) if s == st]; i0, i1 = idx[0], idx[-1]
    a = max(0, D["t"][i0] - 0.3); e = D["t"][i1 + 1] - 0.15 if i1 + 1 < len(D["t"]) else D["ende"]
    k = "p" + st.split(",")[1]; schneide(f"{k}.mp3", a, e)
    S[k] = eintrag(f"{k}.mp3", i0, i1, a, e, [m for m in markiert if i0 <= m <= i1])
    teile.append(tafel(k, f"{st.split(',')[0]} ({st.split(',')[1]})", f"bei {mm(a)} · {mm(e - a)}"))
# von Whisper anders gehört (auch in der Gegenprobe): Stelle im Text suchen, Satz schneiden, Wort markieren
zeilen = [z for z in log.splitlines() if "[" in z and "→" in z]
anders = abweichungen(zeilen[-1], D["w"]) if zeilen else {}
ok = bestaetigt(kap); bestaetigte = {i: g for i, g in anders.items() if pnorm(D["w"][i]) in ok}   # texte/verhoerer.txt
anders = {i: g for i, g in anders.items() if i not in bestaetigte}
if anders:
    teile.append('  <h2 class="abschnitt">Whisper hört anders · bitte anhören</h2>')
    for n_, (i, gehoert) in enumerate(sorted(anders.items()), 1):
        s0 = i; s1 = i
        while s0 > 0 and not D["w"][s0 - 1].rstrip("–“”").strip().endswith(tuple(".;:?!")): s0 -= 1
        while s1 < len(D["w"]) - 1 and not D["w"][s1].rstrip("“”").endswith(tuple(".;:?!")): s1 += 1
        a_ = max(0, D["t"][s0] - 0.3); e_ = D["t"][s1 + 1] - 0.15 if s1 + 1 < len(D["t"]) else D["ende"]
        k = f"w{n_}"; schneide(f"{k}.mp3", a_, e_); S[k] = eintrag(f"{k}.mp3", s0, s1, a_, e_, [i])
        st = D["stelle"][i].split(",")
        teile.append(tafel(k, f"„{D['w'][i].strip(',.;:–?!“”„')}“", f"{st[0]} ({st[1]}) · bei {mm(a_)}",
                           f"Whisper hört „{esc(gehoert)}“ (beide Modelle)").replace("<dt>Filter</dt>", "<dt>Whisper</dt>"))
# neu gesprochene Sätze (werkzeuge/satz.py): eingesetzte Fassung im Kapitel und alle Fassungen zum Vergleich
import glob
for j in sorted(glob.glob(os.path.join(ordner, "satz", f"k{kap:02d}_*.json"))):
    if re.search(r"_a\d+\.", os.path.basename(j)): continue   # Wortzeiten einzelner Fassungen
    d = json.load(open(j, encoding="utf-8")); n_ein = d.get("eingesetzt")
    teile.append(f'  <h2 class="abschnitt">Neu gesprochen · „{esc(" ".join(d["satz"].split()[:4]))} …“</h2>')
    for f in d["fassungen"]:
        k = "n" + os.path.basename(j)[:-5].split("_", 1)[1][:12].replace("ä", "ae") + str(f["n"])
        subprocess.run(["cp", os.path.join(ordner, "satz", f["datei"]), os.path.join(aus, "audio", f["datei"])], check=True)
        dauer = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", os.path.join(aus, "audio", f["datei"])], capture_output=True, text=True).stdout)
        S[k] = {"datei": "audio/" + f["datei"], "dauer": round(dauer, 3), "w": f["w"], "mark": []}
        teile.append(tafel(k, f"Fassung {f['n']}" + (" · eingesetzt" if f["n"] == n_ein else ""),
                           ("wortgetreu" if f["wortgetreu"] else "Abweichung") + f" · Betonung {'unauffällig' if not f['betonung'] else 'markiert'}"
                           + (f" · Stimme {f['stimme']:.2f}".replace(".", ",") if f.get("stimme") else "")))
# vom Betonungsfilter markiert
if M:
    teile.append('  <h2 class="abschnitt">Vom Betonungsfilter markiert</h2>')
    for n, e_ in enumerate(M, 1):
        s0 = e_["i0"]; s1 = e_["i1"]
        while s0 > 0 and not D["w"][s0 - 1].rstrip("–“”").strip().endswith(tuple(".;:?!")): s0 -= 1
        while s1 < len(D["w"]) - 1 and not D["w"][s1].rstrip("“”").endswith(tuple(".;:?!")): s1 += 1
        a = max(0, D["t"][s0] - 0.3); e = D["t"][s1 + 1] - 0.15 if s1 + 1 < len(D["t"]) else D["ende"]
        k = f"m{n}"; schneide(f"{k}.mp3", a, e); S[k] = eintrag(f"{k}.mp3", s0, s1, a, e, [e_["i0"] + e_["pos"]])
        st = D["stelle"][e_["i0"]].split(",")
        teile.append(tafel(k, f"Stelle {n}", f"{st[0]} ({st[1]}) · bei {mm(a)} · +{e_['abstand']:.1f} Halbtöne".replace(".", ","),
                           f"Gipfel auf „{esc(e_['betont'].strip(',.;:–'))}“"))

zeile = lambda a, b_: f"<tr><td>{a}</td><td>{b_}</td></tr>"
filt = f"{len(M)} Stelle{'n' if len(M) != 1 else ''} markiert" + (f", {knapp} knapp darunter" if knapp else "")
kopf = f'''  <header class="kopf">
    <span class="eyebrow">Seneca · De vita beata · Kapitel {kap}</span>
    <h1>Hörprobe</h1>
    <p class="lead">Kapitel {kap} mit Helmut, so wie es ins Video kommt. Oben das ganze Kapitel, darunter jeder Paragraf einzeln{", danach die Stellen, die der Betonungsfilter markiert" if M else ""}. Tippe auf den Knopf, der Text läuft mit.</p>
  </header>

  <section class="befund" aria-labelledby="pruef-titel">
    <h2 id="pruef-titel" class="abschnitt">Geprüft</h2>
    <table>
      <thead><tr><th>Prüfung</th><th>Ergebnis</th></tr></thead>
      <tbody>
        {zeile("Worttreue (Whisper)", (f"{len(anders)} Wörter anders gehört, unten zum Anhören" if anders else "wortgetreu") + (f" (dazu {len(bestaetigte)} bestätigte Verhörer: " + ", ".join(esc(D["w"][i].strip(",.;:–?!“”„")) for i in sorted(bestaetigte)) + ")" if bestaetigte else ""))}
        {zeile("Betonungsfilter (ab 5 Halbtönen)", filt)}
        {zeile("Pausen", esc(pausen.split(",")[0]) if pausen else "–")}
        {zeile("Dauer", mm(D["ende"]))}
      </tbody>
    </table>
  </section>
'''
fuss = ('  <p class="fuss">Fällt dir eine Stelle auf, schreib mir Paragraf und Satzanfang. Ich erzeuge den Satz dann allein '
        'neu, in zwei bis drei Fassungen zur Auswahl. Ton: Helmut Stieglbauer (ElevenLabs), Tempo 0,96, −18 LUFS.</p>')
seite = open(os.path.join(HIER, "hoerprobe_vorlage.html"), encoding="utf-8").read()
seite = (seite.replace("{{TITEL}}", f"Kapitel {kap} · Hörprobe")
         .replace("{{BESCHREIBUNG}}", f"Kapitel {kap} von Senecas De vita beata mit Helmut zum Anhören, mit mitlaufendem Text und den Prüfergebnissen.")
         .replace("{{INHALT}}", kopf + "\n".join(teile) + "\n\n" + fuss)
         .replace("{{DATEN}}", json.dumps(S, ensure_ascii=False)))
open(os.path.join(aus, "index.html"), "w", encoding="utf-8").write(seite)
print(f"{aus}/index.html: {len(S)} Tafeln, Filter {filt}; {treu.strip()}")
