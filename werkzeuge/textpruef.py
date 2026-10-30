"""Textprüfung vor Vorlage und Aufnahme: textpruef.py <kapitelnummer|datei> [--ohne-netz]

Die Worttreue-Prüfung (Whisper) vergleicht die Aufnahme mit dem Text; ein Tippfehler im Text („what“ statt „was“) wird
mitgesprochen, gilt dann als wortgetreu und landet im Video. Darum vorher, ohne Credits:
1. Unbekannte Wörter: nicht im deutschen Wörterbuch (pyspellchecker) und nicht in `texte/woerter_ok.txt`. Findet
   Tippfehler und fremdsprachige Wörter (LanguageTool übersieht „what“ im deutschen Satz). Seltene, aber richtige Wörter
   nach Prüfung in `woerter_ok.txt` eintragen.
2. Doppelte Wörter („die die“): grammatisch oft richtig, beim Zuhören holprig (PLAN.md, Stil).
3. Vorleseregeln aus PLAN.md: Klammern, „als wie“, Einschübe zwischen zwei Gedankenstrichen, Sätze mit sechs und mehr Kommas.
4. LanguageTool (api.languagetool.org, de-DE): Grammatik, Zeichensetzung, Groß- und Kleinschreibung. Der Text ist ohnehin
   öffentlich im Repo; mit --ohne-netz entfällt dieser Teil.
"""
import json, os, re, sys, urllib.parse, urllib.request

HIER = os.path.dirname(os.path.abspath(__file__)); R = os.path.dirname(HIER); sys.path.insert(0, HIER)
import stellen

ziel = sys.argv[1]
datei = f"{R}/texte/kapitel{int(ziel):02d}.txt" if ziel.isdigit() else ziel
text = stellen.rein(open(datei, encoding="utf-8").read()).strip()
ok = set()
if os.path.exists(f"{R}/texte/woerter_ok.txt"):
    ok = {z.split("#")[0].strip().lower() for z in open(f"{R}/texte/woerter_ok.txt", encoding="utf-8")} - {""}
funde = []
umfeld = lambda i, j: text[max(0, i - 35):j + 35].replace("\n", " ")

# 1. unbekannte Wörter
from spellchecker import SpellChecker
sp = SpellChecker(language="de")
for m in re.finditer(r"[A-Za-zÄÖÜäöüß]+(?:-[A-Za-zÄÖÜäöüß]+)*", text):
    w = m.group(0).lower()
    if w in ok or all(t in sp or t in ok for t in w.split("-")): continue
    funde.append(("unbekannt", m.group(0), umfeld(m.start(), m.end())))
# 2. doppelte Wörter
for m in re.finditer(r"\b(\w+)\s+\1\b", text, re.I):
    funde.append(("doppelt", m.group(0), umfeld(m.start(), m.end())))
# 3. Vorleseregeln
roh = open(datei, encoding="utf-8").read()   # Ergänzungen sind im Text ohne Klammern nicht mehr zu sehen
for m in stellen.ZUSATZ.finditer(roh): funde.append(("Ergänzung", m.group(0), roh[max(0, m.start() - 35):m.end() + 5].replace("\n", " ")))
for name, muster in [("Klammer", r"[()]"), ("als wie", r"\bals wie\b"), ("Einschub", r"–[^–.!?]{1,80}–")]:
    for m in re.finditer(muster, text): funde.append((name, m.group(0), umfeld(m.start(), m.end())))
for s in re.split(r"(?<=[.!?])[“”»«\"]?\s+", text):   # Satzende auch vor schließendem Anführungszeichen
    if s.count(",") >= 6: funde.append(("Kommakette", f"{s.count(',')} Kommas", s[:110] + " …"))
# 4. LanguageTool
if "--ohne-netz" not in sys.argv:
    try:
        daten = urllib.parse.urlencode({"text": text, "language": "de-DE"}).encode()
        r = json.load(urllib.request.urlopen("https://api.languagetool.org/v2/check", data=daten, timeout=60))
        for m in r["matches"]:
            if m["rule"]["id"] in ("GERMAN_WORD_REPEAT_RULE", "GERMAN_SPELLER_RULE"): continue   # schon in 1 und 2
            i = m["offset"]; funde.append(("LanguageTool", m["message"], umfeld(i, i + m["length"])))
    except Exception as e:
        print("LanguageTool nicht erreichbar:", e)

for art, was, wo in funde: print(f"{art:12s} {was:24s} …{wo}…")
print(f"{os.path.basename(datei)}: {len(funde)} Hinweise ({len(text.split())} Wörter)")
