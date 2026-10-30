"""Änderungsvorschläge als Seite mit Farben: aenderungen.py <vorschlaege.json> <ausordner>

Der Auftraggeber liest am Handy; Fett erkennt er im Chat kaum (30.10.). Die Seite zeigt je Stelle den ganzen Satz vorher und
nachher untereinander, Entferntes rot und durchgestrichen, Neues gold hinterlegt; bei Bezügen den Satz davor. Die
Markierung rechnet die Seite selbst aus (Wortvergleich), sie muss nicht von Hand gesetzt werden.
vorschlaege.json: {"kapitel": 5, "titel": "…", "lead": "…", "stellen": [{"stelle": "5,1", "davor": "…" (wahlweise),
"vorher": "…", "nachher": "…", "grund": "…"}]}. Ausgabe: <ausordner>/index.html, zum Veröffentlichen als Artifact.
"""
import difflib, html, json, os, re, sys

HIER = os.path.dirname(os.path.abspath(__file__))
D = json.load(open(sys.argv[1], encoding="utf-8")); aus = sys.argv[2]; os.makedirs(aus, exist_ok=True)
teile = lambda s: re.findall(r"\s+|\w+|[^\w\s]", s)


def markiert(alt, neu):   # beide Sätze mit markierten Unterschieden; Leerraum allein wird nicht markiert
    a, b = teile(alt), teile(neu); va, nb = [], []
    for op, i1, i2, j1, j2 in difflib.SequenceMatcher(None, a, b, autojunk=False).get_opcodes():
        x, y = html.escape("".join(a[i1:i2])), html.escape("".join(b[j1:j2]))
        if op == "equal": va.append(x); nb.append(y); continue
        va.append(marke("del", x)); nb.append(marke("ins", y))
    return "".join(va), "".join(nb)


def marke(tag, t):   # Leerraum am Rand bleibt außerhalb der Markierung, sonst ist ein Leerzeichen gold hinterlegt
    if not t.strip(): return t
    m = re.match(r"^(\s*)(.*?)(\s*)$", t, re.S); return f"{m[1]}<{tag}>{m[2]}</{tag}>{m[3]}"


karten, gruppe = [], None
for n, s in enumerate(D["stellen"], 1):
    if s.get("gruppe") and s["gruppe"] != gruppe:   # mehrere Kapitel auf einer Seite: Zwischenüberschrift je Kapitel
        gruppe = s["gruppe"]; karten.append(f'  <h2 class="gruppe">{html.escape(gruppe)}</h2>')
    v, w = markiert(s["vorher"], s["nachher"])
    davor = f'<p class="davor"><span>Satz davor</span>{html.escape(s["davor"])}</p>' if s.get("davor") else ""
    karten.append(f"""  <article class="stelle" id="s{n}">
    <h2><span class="nr">{n}</span> Abschnitt {html.escape(s["stelle"])}</h2>
    {davor}
    <div class="paar">
      <p class="satz alt"><span class="lbl">Vorher</span>{v}</p>
      <p class="satz neu"><span class="lbl">Nachher</span>{w}</p>
    </div>
    <p class="grund">{html.escape(s.get("grund", ""))}</p>
  </article>""")

vorlage = open(os.path.join(HIER, "aenderungen_vorlage.html"), encoding="utf-8").read()
seite = (vorlage.replace("{{titel}}", html.escape(D["titel"])).replace("{{kapitel}}", str(D["kapitel"]))
         .replace("{{lead}}", html.escape(D["lead"])).replace("{{anzahl}}", str(len(D["stellen"]))).replace("{{karten}}", "\n".join(karten)))
open(os.path.join(aus, "index.html"), "w", encoding="utf-8").write(seite)
print(os.path.join(aus, "index.html"), len(D["stellen"]), "Stellen")
