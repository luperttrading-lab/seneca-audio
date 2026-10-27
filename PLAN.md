# Plan: De vita beata vollständig übersetzen und vertonen

Seneca, *De vita beata* (an Gallio), 28 Kapitel, rund 7.260 lateinische Wörter; das Werk bricht in Kapitel 28 mitten im
Satz ab. Lateinischer Text: [The Latin Library](https://www.thelatinlibrary.com/sen/sen.vita.shtml), je Teil in
`texte/latein/teilNN.txt`. Eigene Übersetzung je Teil in `texte/teilNN.txt`.

## Stil der Übersetzung

Festgelegt an Teil 1 nach den Rückmeldungen des Auftraggebers:

- Nah am Latein: Senecas Bilder, Gedankengang und Satzbau bleiben erkennbar, man soll merken, dass es ein antiker Text ist.
- Zugleich heutiges, flüssiges Deutsch zum Zuhören: nicht gestelzt, nicht flapsig, keine modernen Redensarten
  („tappen im Nebel“ geht nicht; „ist ihr Blick getrübt“ trifft es).
- Römische Begriffe bleiben (Prätor, Wahlen statt „Komitien“); Senecas Ansprache an den Leser als „du“.
- Für das Vorlesen gesetzt: Satzzeichen markieren Pausen, Gedankenstriche sparsam, keine Klammern.
- Kein „als wie“; Einschübe zwischen Gedankenstrichen lieber umstellen (die Stimme stockt sonst mitten im Satz);
  lange Kommaketten in zwei Sätze teilen. Bildhafte Wörter nur, wenn sie natürlich klingen (kein „Knäuel von Menschen“).
- Erster Satz ohne „zu“: „Glücklich leben, mein Bruder Gallio, das wollen alle.“

## Ablauf je Teil

1. Übersetzung aus dem Latein, gegen den lateinischen Text geprüft und mit zwei freien Übersetzungen abgeglichen:
   Aubrey Stewart, englisch 1900 ([Project Gutenberg 64576](https://www.gutenberg.org/ebooks/64576), „Of a Happy Life“)
   und Albert Forbiger, deutsch 1867 (nur als [LibriVox-Lesung](https://archive.org/details/vom_glueckseligen_leben_rr_librivox),
   per Whisper abgeschrieben; zeno.org sperrt automatische Abrufe). Freigabe durch den Auftraggeber.
2. Vertonung in ElevenLabs mit der Stimme Lupert (eleven v4), Datei hochladen.
3. Prüfung auf Worttreue (Whisper), Pausen auf natürliche Länge (`werkzeuge/pausen2.py`: Satzende 0,9 s, Absatz 1,3 s,
   Doppelpunkt/Semikolon 0,55 s, Gedankenstrich 0,45 s, Komma 0,30 s nur dort, wo die Stimme schon mindestens 0,15 s pausiert),
   Lautheit −18 LUFS, Wortzeiten für den Lesemodus.
4. In `seite/bau_hoerbuch.py` eintragen und die Hörbuch-Seite neu bauen (Teile-Liste, Lesemodus, nahtloses Weiterspielen).

Umfang für ElevenLabs: Teil 1 hat 1.486 Zeichen bei 162 lateinischen Wörtern; hochgerechnet etwa 66.000 Zeichen für das
ganze Werk, ohne Neuversuche.

## Teile

Kapitel sind die Einheit; Kapitel 1 ist zweigeteilt, 5 und 6 sowie 27 und 28 sind zusammengelegt, 25 und 26 halbiert.
Hördauer geschätzt aus Teil 1 (0,65 s je lateinisches Wort bei Tempo 0,95).

| Teil | Stelle | lat. Wörter | Hördauer bei 0,95 (geschätzt) | Stand |
|---|---|---|---|---|
| 1 | 1,1–2 | 162 | 1:45 | fertig, öffentlich (1:47) |
| 2 | 1,3–5 | 181 | 1:57 | fertig, öffentlich (1:51) |
| 3 | 2,1–4 | 246 | 2:39 | Übersetzung fertig |
| 4 | 3,1–4 | 227 | 2:27 |  |
| 5 | 4,1–5 | 308 | 3:20 |  |
| 6 | 5,1–4 + 6,1–2 | 255 | 2:45 |  |
| 7 | 7,1–4 | 285 | 3:05 |  |
| 8 | 8,1–6 | 326 | 3:31 |  |
| 9 | 9,1–4 | 204 | 2:12 |  |
| 10 | 10,1–3 | 163 | 1:45 |  |
| 11 | 11,1–4 | 230 | 2:29 |  |
| 12 | 12,1–5 | 243 | 2:37 |  |
| 13 | 13,1–5 | 297 | 3:13 |  |
| 14 | 14,1–3 | 179 | 1:56 |  |
| 15 | 15,1–7 | 376 | 4:04 |  |
| 16 | 16,1–3 | 166 | 1:47 |  |
| 17 | 17,1–4 | 247 | 2:40 |  |
| 18 | 18,1–3 | 152 | 1:38 |  |
| 19 | 19,1–3 | 206 | 2:13 |  |
| 20 | 20,1–6 | 360 | 3:54 |  |
| 21 | 21,1–4 | 186 | 2:00 |  |
| 22 | 22,1–5 | 232 | 2:30 |  |
| 23 | 23,1–5 | 289 | 3:07 |  |
| 24 | 24,1–5 | 332 | 3:35 |  |
| 25 | 25,1–4 | 292 | 3:09 |  |
| 26 | 25,5–8 | 168 | 1:49 |  |
| 27 | 26,1–4 | 195 | 2:06 |  |
| 28 | 26,5–8 | 258 | 2:47 |  |
| 29 | 27,1–6 + 28,1 | 370 | 4:00 |  |

Gesamt: 29 Teile, etwa 77 Minuten.
