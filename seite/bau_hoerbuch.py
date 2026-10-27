"""Hörbuch-Seite bauen: alle fertigen Teile mit Liste, Lesemodus und nahtlosem Weiterspielen.

Aufruf: python3 bau_hoerbuch.py <karaoke.json> <Ausgabeordner> [--artifact]
Die Tondateien audio/teilNN.m4a liegen im Ausgabeordner. Mit --artifact entsteht eine Fassung ohne Dokumentrahmen
für eine Claude-Seite (dort wird der Rahmen beim Veröffentlichen ergänzt).
"""
import html, json, os, sys
HIER = os.path.dirname(os.path.abspath(__file__))
TEMPO = 0.95
TEILE = [   # (Titel, Stelle, Schlüssel in karaoke.json, Tondatei)
    ("Teil 1", "Kapitel 1,1–2", "a-lupert_ruhig", "teil01.m4a"),
    ("Teil 2", "Kapitel 1,3–5", "a-teil02", "teil02.m4a"),
]
PLAY = '<svg viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M8 5.5v13a1 1 0 0 0 1.5.86l10.2-6.5a1 1 0 0 0 0-1.72L9.5 4.64A1 1 0 0 0 8 5.5z"/></svg>'
mmss = lambda s: f"{int(s // 60)}:{int(round(s % 60)):02d}"

K = json.load(open(sys.argv[1], encoding="utf-8")); aus = sys.argv[2]; artifact = "--artifact" in sys.argv
liste, texte, daten, gesamt = [], [], [], 0.0
for k, (titel, stelle, schluessel, datei) in enumerate(TEILE):
    d = K[schluessel]; dauer = d["ende"] / TEMPO; gesamt += dauer
    absaetze = {}
    for i, (w, pa) in enumerate(zip(d["w"], d["p"])):
        absaetze.setdefault(pa, []).append(f'<span class="lw" data-i="{i}">{html.escape(w)}</span>')
    texte.append(f'      <div class="teiltext" data-teil="{k}"{" hidden" if k else ""}>\n'
                 + "\n".join(f'<p>{" ".join(s)}</p>' for _, s in sorted(absaetze.items())) + "\n      </div>")
    liste.append(f'    <li><button type="button" class="teil" aria-current="false"><span class="teil-zeichen">{PLAY}</span>'
                 f'<span class="teil-name"><b>{titel}</b> <span>· {stelle}</span></span><span class="teil-dauer">{mmss(dauer)}</span></button></li>')
    daten.append({"titel": titel, "stelle": stelle, "datei": datei, "w": d["w"], "t": d["t"], "ende": d["ende"]})
umfang = f"{len(TEILE)} Teile · {mmss(gesamt)} min" if len(TEILE) > 1 else f"{mmss(gesamt)} min"
seite = (open(os.path.join(HIER, "hoerbuch_vorlage.html"), encoding="utf-8").read()
         .replace("{{LISTE}}", "\n".join(liste)).replace("{{TEXTE}}", "\n".join(texte)).replace("{{UMFANG}}", umfang)
         .replace("{{DATEN}}", json.dumps({"tempo": TEMPO, "teile": daten}, ensure_ascii=False).replace("</", "<\\/")))
assert "{{" not in seite
if artifact:   # Kopf und Körper ohne Dokumentrahmen; dunkles Farbschema per Skript auf das äußere html-Element
    kopf = seite.split("<head>", 1)[1].split("</head>", 1)[0]
    koerper = seite.split("<body>", 1)[1].split("</body>", 1)[0]
    seite = '<script>document.documentElement.setAttribute("data-theme","dark");document.documentElement.lang="de";</script>\n' + kopf + koerper
os.makedirs(aus, exist_ok=True)
open(os.path.join(aus, "index.html"), "w", encoding="utf-8").write(seite)
print("index.html", len(seite), "Zeichen,", umfang)
