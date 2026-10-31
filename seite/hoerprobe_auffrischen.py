"""Bestehende Hörprobe auf die aktuelle Vorlage heben: hoerprobe_auffrischen.py <alte index.html> <neue index.html>

Übernimmt Titel, Beschreibung, Inhalt, Daten und Kapitel aus der veröffentlichten Seite und setzt sie in
seite/hoerprobe_vorlage.html ein; der Kopf vor <title> (<!doctype html>, charset, viewport) bleibt. Ton und Speicher
(Markierungen) des Artifacts bleiben unberührt: nur index.html neu veröffentlichen (publish_files, mode patch).
"""
import json, os, re, sys

alt = open(sys.argv[1], encoding="utf-8").read()
vorlage = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "hoerprobe_vorlage.html"), encoding="utf-8").read()
kopf = alt[:alt.index("<title>")]
titel = re.search(r"<title>(.*?)</title>", alt, re.S).group(1)
beschr = re.search(r'<meta name="description" content="(.*?)">', alt, re.S).group(1)
inhalt = re.search(r'<main class="mit-leiste">\n(.*?)\n  <audio id="ton"', alt, re.S).group(1)
m = re.search(r"var S = (.*?), KAP = (\d+);", alt, re.S); daten, kap = m.group(1), m.group(2)
json.loads(daten)   # Probe: Daten vollständig
neu = (vorlage.replace("{{TITEL}}", titel).replace("{{BESCHREIBUNG}}", beschr).replace("{{INHALT}}", inhalt)
       .replace("{{DATEN}}", daten).replace("{{KAPITEL}}", kap))
assert "{{" not in neu.replace("{{TITEL}}", "")
if not kopf.lower().startswith("<!doctype"): kopf = '<!doctype html><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">' + kopf
open(sys.argv[2], "w", encoding="utf-8").write(kopf + neu)
print(f"{sys.argv[2]}: Kapitel {kap}, {len(json.loads(daten))} Tafeln")
