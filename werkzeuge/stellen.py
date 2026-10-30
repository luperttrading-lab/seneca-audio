"""Stellenmarken im deutschen Text: „[1,2]“ steht vor dem Satz, mit dem im Latein Kapitel 1, Paragraf 2 beginnt.

Die Marken werden nie gesprochen. Vor Stimme, Whisper-Prüfung, Wortzeiten und Pausen kommt der Text ohne Marken:
  stellen.py rein <kapitelNN.txt> <aus.txt>     Text ohne Marken schreiben
  stellen.py liste <kapitelNN.txt>              je Anzeige-Wort die Stelle als JSON („1,1“, „1,1“, …, „1,2“, …)
Die Wortzählung folgt seite/karaoke_daten.py: Absätze an Leerzeilen, Wörter an Leerzeichen, reine Satzzeichen
(„–“) hängen am vorigen Wort.
Ergänzungen des Übersetzers stehen in eckigen Klammern („[ohne es zu erkennen]“, PLAN.md): gesprochen ohne Klammern
(rein), im Video mit Klammern (anzeige, je Wort wie liste).
"""
import json, re, sys

MARKE = re.compile(r"\[(\d+),(\d+)\]\s*")
ZUSATZ = re.compile(r"\[(?!\d+,\d+\])([^\]]*)\]")   # [Ergänzung], keine Stellenmarke
norm = lambda w: re.sub(r"[^a-zäöü0-9]", "", w.lower().replace("ß", "ss"))


def rein(text):
    return ZUSATZ.sub(r"\1", MARKE.sub("", text))


def ohne_klammern(wort):   # ein Anzeige-Wort („[ohne“, „erkennen].“) wie in den Wortzeiten
    return re.sub(r"[\[\]]", "", wort)


def anzeige(text):   # je Anzeige-Wort der Text mit Klammern der Ergänzungen, sonst wie die Wortzeiten (karaoke_daten)
    woerter = []
    for para in text.strip().split("\n\n"):
        for tok in para.split():
            if MARKE.fullmatch(tok + " "): continue
            if not norm(tok) and woerter: woerter[-1] += " " + tok; continue
            woerter.append(tok)
    return woerter


def liste(text):
    stellen, jetzt = [], None
    for para in text.strip().split("\n\n"):
        for tok in para.split():
            m = MARKE.fullmatch(tok + " ")
            if m: jetzt = f"{m.group(1)},{m.group(2)}"; continue
            if not norm(tok) and stellen: continue   # Satzzeichen-Token gehört zum vorigen Wort
            if jetzt is None: sys.exit("Text beginnt ohne Stellenmarke")
            stellen.append(jetzt)
    return stellen


if __name__ == "__main__":
    befehl, datei = sys.argv[1], sys.argv[2]; text = open(datei, encoding="utf-8").read()
    if befehl == "rein": open(sys.argv[3], "w", encoding="utf-8").write(rein(text))
    elif befehl == "liste": print(json.dumps(liste(text), ensure_ascii=False))
    else: sys.exit(__doc__)
