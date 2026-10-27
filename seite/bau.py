import html, json
H = "/tmp/claude-0/-home-user/0523a428-572b-5d43-9560-e7907758c764/scratchpad/hoerproben"
M = json.load(open("/tmp/claude-0/-home-user/0523a428-572b-5d43-9560-e7907758c764/scratchpad/natur/merkmale.json"))
refs = sorted(k for k in M if k.startswith("ref_"))
F = ["Tempo W/s", "Pausenanteil %", "Wörter/Phrase", "Pausen-Schwankung", "Melodie-Spannweite HT", "Abfall HT/s"]
lo = {f: sorted(M[r][f] for r in refs)[1] for f in F}; hi = {f: sorted(M[r][f] for r in refs)[-2] for f in F}
lo["Tempo W/s"], hi["Tempo W/s"] = 2.6, 3.0   # Wunschtempo des Nutzers statt LibriVox-Tempo
de = lambda x, n=2: f"{x:.{n}f}".replace(".", ",").replace("-", "−")
TXT = {  # (zu niedrig, zu hoch, Einheit, Nachkommastellen)
  "Tempo W/s": ("langsamer als dein Wunschtempo", "schneller als dein Wunschtempo", "Wörter pro Sekunde", 2),
  "Pausenanteil %": ("macht zu wenig Pausen", "macht zu viele Pausen", "% Pausenanteil", 1),
  "Wörter/Phrase": ("Phrasen zu kurz", "zu viele Wörter ohne Pause am Stück", "Wörter je Phrase", 2),
  "Pausen-Schwankung": ("Pausen zu gleichförmig, Schwankung der Pausenlängen", "Pausen zu unregelmäßig, Schwankung der Pausenlängen", "", 2),
  "Melodie-Spannweite HT": ("Satzmelodie zu monoton", "Satzmelodie zu lebhaft", "Halbtöne", 1),
  "Abfall HT/s": ("Phrasenenden fallen zu stark ab", "Phrasenenden fallen zu wenig ab", "Halbtöne je Sekunde", 2),
}
def erkl(key):
    m = M[key]; d = 0.0; ab = []
    for f in F:
        a, b = lo[f], hi[f]; w = b - a; x = m[f]
        eps = 0.01 * w   # Rundungsgrenze: winzige Überschreitung zählt als im Bereich
        if x < a - eps: d += (a - x) / w; ab.append(f"{TXT[f][0]}: {de(x, TXT[f][3])} statt {de(a, TXT[f][3])} bis {de(b, TXT[f][3])} {TXT[f][2]}".rstrip())
        elif x > b + eps: d += (x - b) / w; ab.append(f"{TXT[f][1]}: {de(x, TXT[f][3])} statt {de(a, TXT[f][3])} bis {de(b, TXT[f][3])} {TXT[f][2]}".rstrip())
    rest = len(F) - len(ab)
    kopf = f"Abstand {de(d)}. 0 heißt: alle sechs Messwerte liegen im Zielbereich. Je kleiner, desto natürlicher. Das Tempo misst sich an deinem Wunsch von 2,6 bis 3,0 Wörtern pro Sekunde, die übrigen Werte an sieben echten Vorlesern."
    teil = f"{rest} von 6 Werten liegen im Zielbereich." + (" Abweichungen:" if ab else "")
    liste = "".join(f"<li>{html.escape(x)}</li>" for x in ab)
    return de(d), f'<p>{kopf}</p><p>{teil}</p>' + (f"<ul>{liste}</ul>" if ab else "")

def tempo(aid, standard=1.0):
    teile = []
    for k in range(101):              # 0,50 … 1,50 in 0,01-Schritten
        art = "zehntel" if k % 10 == 0 else "halb" if k % 5 == 0 else ""
        lab = f'<b data-k="{k}">{(0.5 + k / 100):.1f}</b>'.replace(".", ",") if k % 10 == 0 else ""
        teile.append(f'<span class="rad-wert {art}">{lab}</span>')
    return f'''<div class="tempo" data-for="{aid}" data-standard="{standard}">
          <span class="tempo-label" id="l-{aid}">Tempo</span>
          <div class="rad" role="slider" tabindex="0" aria-labelledby="l-{aid}" aria-valuemin="0.5" aria-valuemax="1.5" aria-valuenow="1" aria-valuetext="1,00-fach">
            <div class="rad-band"><span class="rad-rand"></span>{"".join(teile)}<span class="rad-rand"></span></div>
          </div>
          <output id="o-{aid}">1,00×</output>
        </div>'''


K0 = json.load(open(f"{H}/karaoke.json", encoding="utf-8"))
min_s = lambda e: f"{int(e // 60)}:{int(round(e % 60)):02d} min"
haupt = [
  ("lupert_ruhig", "tts_lupert_ruhig_095", "Lupert, ruhig", [min_s(K0["a-lupert_ruhig"]["ende"] / 0.95), "dein Stimmklon", "mehr Pausen"],
   "Wie die Fassung darunter, aber mit mehr Zeit zwischen den Gedanken: Satzende 0,9 s, Absatz 1,3 s, Doppelpunkt 0,55 s, Gedankenstrich 0,45 s, Komma 0,35 s, nur wo Lupert schon eine Lücke lässt. Startet mit Tempo 0,95; Dauer und Abstand gelten für dieses Tempo.", "lupert_ruhig.mp3", 0.95),
  ("lupert_exp_pausen", "tts_lupert_exp_pausen", "Lupert, Pausen verlängert", [min_s(K0["a-lupert_exp_pausen"]["ende"]), "dein Stimmklon", "eleven v4"],
   "Deine Lupert-Aufnahme, Wort für Wort unverändert. Nur die Pausen an Punkt, Komma, Doppelpunkt und Gedankenstrich sind auf natürliche Länge gebracht, 22 Stellen, zusammen 5,5 Sekunden. Die Verlängerung bildet das Grundrauschen der jeweiligen Pause nach, ohne Wiederholung, damit nichts knattert.", "lupert_exp_pausen.mp3"),
  ("lupert_exp", "tts_lupert_exp", "Lupert, Original", [min_s(K0["a-lupert_exp"]["ende"]), "dein Stimmklon", "eleven v4"],
   "So, wie ElevenLabs sie geliefert hat. Ein Versprecher am Schluss: „auf anderem Reisen“ statt „anderen“.", "lupert_exp.mp3"),
  ("eleven_ganz", "tts_eleven_ganz_093", "ElevenLabs Christian", ["1:44 min", "eleven v4", "wortgetreu"],
   "Startet mit Tempo 0,93, wie es dir gefallen hat; der Abstand ist bei diesem Tempo gemessen.", "eleven_christian_ganz.mp3", 0.93),
  ("neufassung2", "tts_neu2b", "Gemini Fenrir, zusammengeschnitten", [min_s(K0["a-neufassung2"]["ende"]), "102 Durchläufe", "wortgetreu"],
   "Satzweise in acht Varianten erzeugt, jeder Satz mit dem Anfang des nächsten eingesprochen und in der Pause geschnitten. Misst sich am nächsten an echten Vorlesern, klingt aber nach Gemini.", "neufassung2_bestof.mp3"),
]
tafeln = ""
for eintrag in haupt:
    sid, key, titel, chips, text, datei = eintrag[:6]; standard = eintrag[6] if len(eintrag) > 6 else 1.0
    zahl, pop = erkl(key); aid = f"a-{sid}"
    tafeln += f'''
      <article class="tafel">
        <div class="kopfzeile"><h3>{titel}</h3><button type="button" class="mitlesen" data-audio="{aid}" aria-controls="lesen" aria-expanded="false"><svg viewBox="0 0 24 24" aria-hidden="true"><path fill="none" stroke="currentColor" stroke-width="1.8" stroke-linejoin="round" d="M12 6.5C10.2 5.2 7.6 4.6 4 4.8v12.6c3.6-.2 6.2.4 8 1.7 1.8-1.3 4.4-1.9 8-1.7V4.8c-3.6-.2-6.2.4-8 1.7zM12 6.5v12.6"/></svg>Mitlesen</button></div>
        <div class="meta">{"".join(f'<span class="chip">{c}</span>' for c in chips)}<button type="button" class="chip chip-info" aria-expanded="false" aria-controls="e-{sid}">Abstand {zahl}</button></div>
        <div class="pop" id="e-{sid}" hidden>{pop}</div>
        <p>{text}</p>
        <audio id="{aid}" controls preload="metadata" src="audio/{datei}"></audio>
        {tempo(aid, standard)}
      </article>'''
import difflib, re as _re
K = json.load(open(f"{H}/karaoke.json", encoding="utf-8"))
_n = lambda w: _re.sub(r"[^a-zäöü0-9]", "", w.lower().replace("ß", "ss"))
def volltext(aid, ziel):
    d = K[aid]; absaetze = {}
    for i, (w, pa) in enumerate(zip(d["w"], d["p"])):
        absaetze.setdefault(pa, []).append(f'<span class="lw" data-i="{i}">{html.escape(w)}</span>')
    return "\n".join(f'<p>{" ".join(s)}</p>' for pa, s in sorted(absaetze.items()))
ZIEL = {k: ("t-neu2", "a-neufassung2") for k in ("a-neufassung2", "a-eleven_ganz", "a-lupert_exp", "a-lupert_exp_pausen", "a-lupert_ruhig")}
K = {k: K[k] for k in ZIEL}   # nur noch Daten der Fassungen auf der Seite
for aid, (ziel, basis) in ZIEL.items():
    a, z = [_n(w) for w in K[aid]["w"]], [_n(w) for w in K[basis]["w"]]
    if a == z: K[aid]["map"] = None
    else:
        mp = [-1] * len(a)
        for op, i1, i2, j1, j2 in difflib.SequenceMatcher(None, a, z, autojunk=False).get_opcodes():
            if op == "equal" or (op == "replace" and i2 - i1 == j2 - j1):
                for k in range(i2 - i1): mp[i1 + k] = j1 + k
        for i in range(len(mp)):          # Lücken: auf das vorige zugeordnete Wort zeigen
            if mp[i] < 0: mp[i] = mp[i - 1] if i else 0
        K[aid]["map"] = mp
    K[aid]["ziel"] = ziel
page = open(f"{H}/vorlage.html", encoding="utf-8").read().replace("{{TAFELN}}", tafeln).replace("{{NEU2}}", volltext("a-neufassung2", "t-neu2")).replace("{{KARAOKE}}", json.dumps(K, ensure_ascii=False).replace("</", "<\\/"))
assert "{{" not in page
open(f"{H}/index.html", "w", encoding="utf-8").write(page)
print("ok", len(page))
