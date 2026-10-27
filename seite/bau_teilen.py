"""Seite für Empfänger bauen: eine Fassung, großer Play-Knopf, Lesemodus. Schreibt ../index.html (Startseite auf GitHub Pages)."""
import html, json, os
HIER = os.path.dirname(os.path.abspath(__file__))
FASSUNG, DATEI, TEMPO = "a-lupert_ruhig", "lupert_ruhig.m4a", 0.95

d = json.load(open(os.path.join(HIER, "karaoke.json"), encoding="utf-8"))[FASSUNG]
absaetze = {}
for i, (w, pa) in enumerate(zip(d["w"], d["p"])):
    absaetze.setdefault(pa, []).append(f'<span class="lw" data-i="{i}">{html.escape(w)}</span>')
text = "\n".join(f'<p>{" ".join(s)}</p>' for _, s in sorted(absaetze.items()))
dauer = d["ende"] / TEMPO
daten = {"w": d["w"], "t": d["t"], "ende": d["ende"], "tempo": TEMPO}
seite = (open(os.path.join(HIER, "teilen_vorlage.html"), encoding="utf-8").read()
         .replace("{{TEXT}}", text).replace("{{DATEI}}", DATEI)
         .replace("{{DAUER}}", f"{int(dauer // 60)}:{int(round(dauer % 60)):02d} min")
         .replace("{{DATEN}}", json.dumps(daten, ensure_ascii=False).replace("</", "<\\/")))
assert "{{" not in seite
open(os.path.join(HIER, "..", "index.html"), "w", encoding="utf-8").write(seite)
print("index.html", len(seite), "Zeichen, Dauer", f"{dauer:.1f} s")
