"""Hörbuch-Seite bauen: alle fertigen Teile mit Liste, Lesemodus und nahtlosem Weiterspielen.

Aufruf: python3 bau_hoerbuch.py <karaoke.json> <Ausgabeordner> [--artifact] [--vergleich <messung.json>]
Die Tondateien audio/teilNN.m4a liegen im Ausgabeordner. Mit --artifact entsteht eine Fassung ohne Dokumentrahmen
für eine Claude-Seite (dort wird der Rahmen beim Veröffentlichen ergänzt); sie erwartet audio/teilNN.mp3. Mit
--vergleich kommen unter die Teile die Abschnitte aus ABSCHNITTE (Kapitel 1, Absatz 1–2) mit den Messwerten aus der
angegebenen Datei.
"""
import html, json, os, sys
HIER = os.path.dirname(os.path.abspath(__file__))
TEMPO = 0.95
TEILE = [   # (Titel, Stelle, Schlüssel in karaoke.json, Tondatei)
    ("Teil 1", "Kapitel 1,1–2", "a-lupert_ruhig", "teil01.m4a"),
    ("Teil 2", "Kapitel 1,3–5", "a-teil02", "teil02.m4a"),
]
VERGLEICH = [   # (Name, Modell und Einstellungen, Schlüssel in karaoke.json, Schlüssel in der Messung, Tondatei)
    ("Ralf Benz", "Multilingual v2 · Stability 0,75 · Probe 1", "a-v-ralf_v2_a", "v_ralf_v2_a", "v_ralf_v2_a.mp3"),
    ("Ralf Benz", "Multilingual v2 · Stability 0,75 · Probe 2", "a-v-ralf_v2_b", "v_ralf_v2_b", "v_ralf_v2_b.mp3"),
    ("Ralf Benz", "v4 · Stability 0,5 · 27.10.", "a-v-ralf", "v_ralf", "v_ralf.mp3"),
    ("Ralf Benz", "v4 · Stability 1,0", "a-v-ralf_v4_stab10", "v_ralf_v4_stab10", "v_ralf_v4_stab10.mp3"),
    ("Ralf Benz", "Storytel v2 · Stability 0,75", "a-v-ralf_storytel", "v_ralf_storytel", "v_ralf_storytel.mp3"),
    ("Lupert", "v4 · Stability 0,5 · wie am 27.10.", "a-v-lupert_v4_a", "v_lupert_v4_a", "v_lupert_v4_a.mp3"),
    ("Lupert", "Multilingual v2 · Stability 0,75", "a-v-lupert_v2", "v_lupert_v2", "v_lupert_v2.mp3"),
]
PAUSENTEST = [   # gleicher Aufbau wie VERGLEICH; Reihenfolge fest, Tempo wie im Hörbuch
    ("Lupert", "Teil 1 wie im Hörbuch: App, v4 exp, bearbeitet", "a-ab-teil1_bearb", "ab_teil1_bearb", "ab_teil1_bearb.mp3"),
    ("Lupert", "derselbe Take unbearbeitet", "a-ab-teil1_roh", "ab_teil1_roh", "ab_teil1_roh.mp3"),
    ("Lupert", "heute per API, v4, unbearbeitet", "a-ab-heute_roh", "ab_heute_roh", "ab_heute_roh.mp3"),
    ("Lupert", "heute per API, v4, bearbeitet wie Teil 1", "a-ab-heute_bearb", "ab_heute_bearb", "ab_heute_bearb.mp3"),
    ("Ralf Benz", "Multilingual v2, Probe 2, bearbeitet wie Teil 1", "a-ab-ralf_v2_bearb", "ab_ralf_v2_bearb", "ab_ralf_v2_bearb.mp3"),
]
ABSCHNITTE = [   # (Kennung, Überschrift, Einleitung, Tempo, nach Abstand sortieren, Einträge)
    ("pausen", "Teil 1 gegen heute: Pausen", "Kapitel 1, Absatz 1–2, alle mit Tempo 0,95 wie im Hörbuch und gleich laut. „Bearbeitet“ heißt "
     "nur: Pausen verlängert wie in Teil 1 (Satzende 0,9 s, Absatz 1,3 s, Doppelpunkt 0,55 s, Gedankenstrich 0,45 s, Komma 0,35 s, "
     "wo die Stimme schon kurz absetzt). Tonhöhe und Satzmelodie sind unverändert.", 0.95, False, PAUSENTEST),
    ("vergleich", "Stimmen und Modelle zum Vergleich", "Kapitel 1, Absatz 1–2, so wie ElevenLabs sie liefert: unbearbeitet, Tempo 1,0, "
     "gleich laut. Sortiert nach Abstand zu echten Vorlesern; Pausen lassen sich nachträglich verlängern, Satzmelodie und Tonlage nicht. "
     "Melodie ist die Spannweite der Satzmelodie: echte Vorleser 10 bis 11,7 Halbtöne, deine eigene Lesung 8,6.", 1.0, True, VERGLEICH),
]
PLAY = '<svg viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M8 5.5v13a1 1 0 0 0 1.5.86l10.2-6.5a1 1 0 0 0 0-1.72L9.5 4.64A1 1 0 0 0 8 5.5z"/></svg>'
mmss = lambda s: f"{int(s // 60)}:{int(round(s % 60)):02d}"
de = lambda x, n=0: f"{x:.{n}f}".replace(".", ",")

K = json.load(open(sys.argv[1], encoding="utf-8")); aus = sys.argv[2]; artifact = "--artifact" in sys.argv
messung = json.load(open(sys.argv[sys.argv.index("--vergleich") + 1], encoding="utf-8")) if "--vergleich" in sys.argv else None

def text_html(d, k):
    absaetze = {}
    for i, (w, pa) in enumerate(zip(d["w"], d["p"])):
        absaetze.setdefault(pa, []).append(f'<span class="lw" data-i="{i}">{html.escape(w)}</span>')
    return (f'      <div class="teiltext" data-teil="{k}"{" hidden" if k else ""}>\n'
            + "\n".join(f'<p>{" ".join(s)}</p>' for _, s in sorted(absaetze.items())) + "\n      </div>")
def knopf(k, name, zusatz, dauer, mess=""):
    return (f'    <li><button type="button" class="teil" data-n="{k}" aria-current="false"><span class="teil-zeichen">{PLAY}</span>'
            f'<span class="teil-name"><b>{html.escape(name)}</b> <span>· {html.escape(zusatz)}</span>{mess}</span>'
            f'<span class="teil-dauer">{mmss(dauer)}</span></button></li>')

liste, texte, daten, vergleich, gesamt = [], [], [], [], 0.0
for k, (titel, stelle, schluessel, datei) in enumerate(TEILE):
    d = K[schluessel]; dauer = d["ende"] / TEMPO; gesamt += dauer
    texte.append(text_html(d, k)); liste.append(knopf(k, titel, stelle, dauer))
    if artifact: datei = datei.replace(".m4a", ".mp3")   # Claude-Seiten liefern kein .m4a aus
    daten.append({"titel": titel, "stelle": stelle, "datei": datei, "w": d["w"], "t": d["t"], "ende": d["ende"]})
bloecke = []
for kennung, ueberschrift, einleitung, tempo, sortiert, eintraege in (ABSCHNITTE if messung else []):
    if sortiert:   # nach Abstand sortiert, die natürlichste Stimme oben
        eintraege = sorted(eintraege, key=lambda v: float(messung[v[3]]["abstand"].replace(",", ".")))
    vliste = []
    for name, beschr, schluessel, mkey, datei in eintraege:
        k = len(TEILE) + len(vergleich); d = K[schluessel]; m = messung[mkey]
        mess = (f'<span class="teil-mess">Abstand\u00a0{m["abstand"]} · Melodie\u00a0{de(m["mel"], 1)}\u00a0HT · Pausen\u00a0{de(m["pausen"])}\u00a0%'
                f' · Tempo\u00a0{de(m["tempo"], 2)}\u00a0W/s</span>')   # geschützte Leerzeichen: Zahl und Einheit nicht trennen
        texte.append(text_html(d, k)); vliste.append(knopf(k, name, beschr, d["ende"] / tempo, mess))
        vergleich.append({"titel": name, "stelle": beschr, "datei": datei, "w": d["w"], "t": d["t"], "ende": d["ende"], "tempo": tempo})
    bloecke.append(f'  <section class="vergleich" aria-labelledby="h-{kennung}">\n    <h2 id="h-{kennung}">{html.escape(ueberschrift)}</h2>\n'
                   f'    <p>{html.escape(einleitung)}</p>\n    <ol class="teile">\n' + "\n".join(vliste) + "\n    </ol>\n  </section>")
vblock = "\n".join(bloecke)
umfang = f"{len(TEILE)} Teile · {mmss(gesamt)} min" if len(TEILE) > 1 else f"{mmss(gesamt)} min"
seite = (open(os.path.join(HIER, "hoerbuch_vorlage.html"), encoding="utf-8").read()
         .replace("{{LISTE}}", "\n".join(liste)).replace("{{TEXTE}}", "\n".join(texte)).replace("{{UMFANG}}", umfang)
         .replace("{{VERGLEICH}}", vblock)
         .replace("{{DATEN}}", json.dumps({"tempo": TEMPO, "teile": daten, "vergleich": vergleich}, ensure_ascii=False).replace("</", "<\\/")))
assert "{{" not in seite
if artifact:   # Kopf und Körper ohne Dokumentrahmen; dunkles Farbschema per Skript auf das äußere html-Element
    kopf = seite.split("<head>", 1)[1].split("</head>", 1)[0]
    koerper = seite.split("<body>", 1)[1].split("</body>", 1)[0]
    seite = '<script>document.documentElement.setAttribute("data-theme","dark");document.documentElement.lang="de";</script>\n' + kopf + koerper
os.makedirs(aus, exist_ok=True)
open(os.path.join(aus, "index.html"), "w", encoding="utf-8").write(seite)
print("index.html", len(seite), "Zeichen,", umfang, f"+ {len(vergleich)} Vergleichsstimmen" if vergleich else "")
