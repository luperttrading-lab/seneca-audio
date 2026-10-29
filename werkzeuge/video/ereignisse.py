"""Bildwechsel für das Video aus Wortzeiten: ereignisse.py <zeiten.json> <ausgabe.json> <titel> <abschnitt> <teil>

zeiten.json: {"w": Wörter, "t": Startzeiten im fertigen Ton (s), "p": Absatz je Wort, "stelle": lat. Stelle je Wort,
"titel_ende": Ende der Titelkarte, "ende": Gesamtdauer}. Danach: node render.js <ordner> und ffmpeg -f concat (siehe UEBERGABE.md).
"""
import json, sys

Z = json.load(open(sys.argv[1])); W, T, P, ST = Z["w"], Z["t"], Z["p"], Z["stelle"]; n = len(W)
E = [(0.0, {"modus": "titel"}), (Z["titel_ende"], {"modus": "text", "absatz": P[0], "wort": -1, "vorbis": -1, "stelle": ST[0]})]
ab = P[0]
for i in range(n):
    if P[i] != ab:   # neuer Absatz erscheint kurz vor seinem ersten Wort
        ab = P[i]; E.append((T[i] - 0.35, {"modus": "text", "absatz": ab, "wort": -1, "vorbis": i - 1, "stelle": ST[i]}))
    E.append((T[i], {"modus": "text", "absatz": ab, "wort": i, "vorbis": i, "stelle": ST[i]}))
    nxt = T[i + 1] if i + 1 < n else Z["ende"]
    if nxt > T[i] + 0.9:   # Markierung endet in längeren Pausen
        E.append((T[i] + 0.9, {"modus": "text", "absatz": ab, "wort": -1, "vorbis": i, "stelle": ST[i]}))
E.sort(key=lambda e: e[0])
json.dump({"daten": {"w": W, "p": P, "titel": sys.argv[3], "abschnitt": sys.argv[4], "teil": sys.argv[5]},
           "ereignisse": [{"t": t, "z": z} for t, z in E], "ende": Z["ende"]}, open(sys.argv[2], "w"), ensure_ascii=False)
print(len(E), "Bilder")
