"""Vorfilter für Betonungsfehler: betonung.py <ton> <woerter.json> [<aus.json>] [--abstand 5]

Whisper prüft nur die Wörter, nicht die Betonung (29.10.: „die vor uns hergeht“ mit dem Akzent auf „vor“ hörte nur der
Nutzer). Der Filter teilt die Aufnahme an Satzzeichen in Sprechabschnitte und misst je Wort den Tonhöhengipfel
(95-%-Quantil der stimmhaften Rahmen, Halbtöne gegen den Median der ganzen Aufnahme). Markiert wird ein Abschnitt, wenn
der höchste Gipfel auf einem Funktionswort liegt (Artikel, Pronomen, Präposition, Konjunktion, Hilfsverb), nicht am
Abschnittsanfang (dort hebt die Deklination jedes Wort) und mindestens --abstand Halbtöne über dem höchsten Inhaltswort.
Er ersetzt das Ohr nicht: Kontrastbetonung („nicht du, sondern ich“) ist richtig und wird trotzdem markiert.
Schwelle 5 HT (Nutzer, 30.10.): in Kapitel 1 lag der echte Fehler bei +9,9 HT, die übrigen Markierungen bei 1 HT
(höchstens +4,7) klangen alle in Ordnung. Abschnitte zwischen 3 und 5 HT werden mitgezählt, damit sich die Schwelle an
jedem weiteren gemeldeten Fehler nachprüfen lässt.
Die Wortzeiten müssen zur Zeitachse von <ton> passen (Rohaufnahme und woerter.json aus kapitel.py).
"""
import json, os, re, subprocess, sys, tempfile
import numpy as np
import parselmouth

FUNKTION = set("""
der die das den dem des ein eine einen einem einer eines
ich du er sie es wir ihr uns euch mich dich sich mir dir ihm ihn ihnen man
mein meine meinen meinem meiner meines dein deine deinen deinem deiner deines sein seine seinen seinem seiner seines
ihre ihren ihrem ihrer ihres unser unsere unseren unserem unserer unseres euer eure euren eurem eurer
an am auf aus bei beim bis durch für gegen hinter in im ins mit nach neben ohne seit über um unter von vom vor zu zum zur
zwischen wegen
und oder aber denn dass wenn als wie ob weil doch sondern sowie
ist sind war waren wird werden wurde wurden hat haben hatte hatten sei seien wäre wären bin bist seid habe hast
würde würden kann können muss müssen soll sollen will wollen darf dürfen
""".split())
ENDE = tuple(",.;:!?–")
norm = lambda w: re.sub(r"[^a-zäöüß]", "", w.lower())


def gipfel(ton, W):
    with tempfile.TemporaryDirectory() as d:
        wav = os.path.join(d, "t.wav")
        subprocess.run(["ffmpeg", "-nostdin", "-y", "-loglevel", "error", "-i", ton, "-ac", "1", wav], check=True)
        p = parselmouth.Sound(wav).to_pitch_ac(time_step=0.01, pitch_floor=70, pitch_ceiling=250)
    f0, t = p.selected_array["frequency"], p.xs()
    median = np.median(f0[f0 > 0])
    G = []
    for w in W:
        f = f0[(t >= w["s"]) & (t <= w["e"]) & (f0 > 0)]
        G.append(float(np.quantile(12 * np.log2(f / median), 0.95)) if len(f) >= 3 else None)
    return G


def abschnitte(W):
    A, jetzt = [], []
    for i, w in enumerate(W):
        jetzt.append(i)
        if w["w"].rstrip("“”»«\"'").endswith(ENDE) or i == len(W) - 1: A.append(jetzt); jetzt = []
    return A


def betonung_klein(e):   # Gipfel auf einem Funktionswort, nicht am Abschnittsanfang
    return norm(e["woerter"][e["pos"]]) in FUNKTION and e["pos"] > 0


def pruefe(ton, W, abstand=5.0):
    G = gipfel(ton, W); erg = []
    for a in abschnitte(W):
        g = [(i, G[i]) for i in a if G[i] is not None]
        if len(g) < 3: continue
        top = max(g, key=lambda x: x[1])[0]
        inhalt = [x for i, x in g if norm(W[i]["w"]) not in FUNKTION]
        d = G[top] - max(inhalt) if inhalt else float("inf")
        markiert = norm(W[top]["w"]) in FUNKTION and top != a[0] and d >= abstand
        erg.append({"i0": a[0], "i1": a[-1], "von": W[a[0]]["s"], "bis": W[a[-1]]["e"], "woerter": [W[i]["w"] for i in a], "gipfel": [G[i] for i in a],
                    "betont": W[top]["w"], "pos": a.index(top), "abstand": round(d, 2), "markiert": markiert})
    return erg


if __name__ == "__main__":
    argv, abstand = sys.argv[1:], 5.0
    if "--abstand" in argv: i = argv.index("--abstand"); abstand = float(argv[i + 1]); del argv[i:i + 2]
    erg = pruefe(argv[0], json.load(open(argv[1], encoding="utf-8")), abstand)
    if len(argv) > 2: json.dump(erg, open(argv[2], "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    m = [e for e in erg if e["markiert"]]
    for e in m:
        satz = " ".join(w.upper() if j == e["pos"] else w for j, w in enumerate(e["woerter"]))
        print(f"{e['von']:7.2f} s  +{e['abstand']:.1f} HT  {satz}")
    knapp = sum(1 for e in erg if not e["markiert"] and betonung_klein(e) and 3 <= e["abstand"] < abstand)
    print(f"{len(m)} von {len(erg)} Sprechabschnitten markiert (Abstand ≥ {abstand} HT); {knapp} knapp darunter (3 bis {abstand} HT)")
