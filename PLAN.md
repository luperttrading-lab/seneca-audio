# Plan: De vita beata vollständig übersetzen und vertonen

Seneca, *De vita beata* (an Gallio), 28 Kapitel, rund 7.260 lateinische Wörter; das Werk bricht in Kapitel 28 mitten im
Satz ab. Lateinischer Text: [The Latin Library](https://www.thelatinlibrary.com/sen/sen.vita.shtml), je Kapitel in
`texte/latein/kapitelNN.txt`. Eigene Übersetzung je Kapitel in `texte/kapitelNN.txt`, mit Stellenmarken „[1,2]“ vor dem
Satz, mit dem der lateinische Paragraf beginnt (nie gesprochen; `werkzeuge/stellen.py` entfernt sie vor Stimme, Prüfung
und Wortzeiten und liefert je Wort die Stelle für das Video). Endprodukt: ein YouTube-Video mit mitlaufendem Text.

## Stil der Übersetzung

Festgelegt an Kapitel 1 nach den Rückmeldungen des Auftraggebers:

- Nah am Latein: Senecas Bilder, Gedankengang und Satzbau bleiben erkennbar, man soll merken, dass es ein antiker Text ist.
- Zugleich heutiges, flüssiges Deutsch zum Zuhören: nicht gestelzt, nicht flapsig, keine modernen Redensarten
  („tappen im Nebel“ geht nicht; „ist ihr Blick getrübt“ trifft es).
- Römische Begriffe bleiben (Prätor, Wahlen statt „Komitien“); Senecas Ansprache an den Leser als „du“.
- Für das Vorlesen gesetzt: Satzzeichen markieren Pausen, Gedankenstriche sparsam, keine Klammern.
- Kein „als wie“; Einschübe zwischen Gedankenstrichen lieber umstellen (die Stimme stockt sonst mitten im Satz);
  lange Kommaketten in zwei Sätze teilen. Bildhafte Wörter nur, wenn sie natürlich klingen (kein „Knäuel von Menschen“).
- Erster Satz ohne „zu“: „Glücklich leben, mein Bruder Gallio, das wollen alle.“

## Ablauf je Kapitel

1. Übersetzung aus dem Latein, gegen den lateinischen Text geprüft und mit zwei freien Übersetzungen abgeglichen:
   Aubrey Stewart, englisch 1900 ([Project Gutenberg 64576](https://www.gutenberg.org/ebooks/64576), „Of a Happy Life“)
   und Albert Forbiger, deutsch 1867 (nur als [LibriVox-Lesung](https://archive.org/details/vom_glueckseligen_leben_rr_librivox),
   per Whisper abgeschrieben; zeno.org sperrt automatische Abrufe). Freigabe durch den Auftraggeber.
2. Vertonung in ElevenLabs mit der Stimme Lupert (eleven v4), Datei hochladen.
3. Prüfung auf Worttreue (Whisper), Pausen auf natürliche Länge (`werkzeuge/pausen2.py`: Satzende 0,9 s, Absatz 1,3 s,
   Doppelpunkt/Semikolon 0,55 s, Gedankenstrich 0,45 s, Komma 0,30 s nur dort, wo die Stimme schon mindestens 0,15 s pausiert),
   Lautheit −18 LUFS, Wortzeiten für den Lesemodus.
4. In `seite/bau_hoerbuch.py` eintragen und die Hörbuch-Seite neu bauen (Kapitel-Liste, Lesemodus, nahtloses Weiterspielen).

Umfang für ElevenLabs: Kapitel 1,1–2 hat 1.486 Zeichen bei 162 lateinischen Wörtern; hochgerechnet etwa 66.000 Zeichen für das
ganze Werk, ohne Neuversuche.

## Abschnitte und gesprochene Titel

**Verworfen am 29.10.** (Nutzer): Abschnitte und ihre Namen sind unsere eigene Einteilung und entfallen, wie die Teile.
Im Video gibt es nur die Startseite („Seneca. Vom glücklichen Leben.“ gesprochen), danach Kapitel für Kapitel ohne
Titelkarte. Die Analyse bleibt als Hintergrund:

Titel werden nur dort gesprochen, wo bei Seneca ein neuer Gedankengang beginnt, ohne Nummer, als eigener kurzer
Clip vor dem Kapitel (fällt ohne Neuaufnahme weg, falls er stört). Kapitel, Paragraf und Abschnitt stehen nur
geschrieben im Bild. Die Grenzen am Latein geprüft (29.10.); Titel aus Senecas eigenen Worten, Vorschlag, Freigabe offen:

| Abschnitt | Kapitel | Dauer | Titel (Vorschlag) | Beleg |
|---|---|---|---|---|
| 1 | 1–2 | 6:40 | Wohin und auf welchem Weg | 1,2 decernatur et quo tendamus et qua |
| 2 | 3–6 | 8:58 | Im Einklang mit der Natur | 3,3 vita conveniens naturae suae; 6,2 fasst zusammen |
| 3 | 7–16 | 28:00 | Tugend und Lust | 7,1 Epikureer: Lust nicht von der Tugend zu trennen; 16,1 ergo … vera felicitas schließt |
| 4 | 17–20 | 10:56 | Du redest anders, als du lebst | 17,1 quare ergo tu fortius loqueris quam vivis; 18,1 aliter loqueris, aliter vivis |
| 5 | 21–28 | 26:19 | Der Weise und der Reichtum | 21,1 quare … tam dives vitam agit |

Kapitel 16 ist kein eigener Abschnitt (169 Wörter, beginnt mit ergo und schließt Abschnitt 3); 17–28 zerfällt in die
Antwort auf den Vorwurf der Heuchelei (17–20) und die Frage nach dem Reichtum (21–28). Möglicher sechster Titel:
Sokrates’ Rede ab 27,1 (Kapitel 27, 3:17), offen.

## Kapitel

Seit 29.10. ist Senecas Kapitel die einzige Einheit (vorher 29 „Teile“ nach Hörlänge: Kapitel 1 geteilt, 5+6 und 27+28
zusammengelegt, 25 und 26 halbiert). Bisherige Teile: 1+2 → Kapitel 1, 3 → 2, 4 → 3, 5 → 4; ab Teil 7 ist Teil = Kapitel bis 24.
Wörter gezählt im lateinischen Text ohne Paragrafennummern; Hördauer geschätzt mit 0,669 s je Wort (Helmut, Tempo 0,96,
gemessen an 1,1–2). Ein Kapitel geht als eine Anfrage an ElevenLabs; das längste (25) hat deutsch etwa 4.300 Zeichen.

| Kapitel | Paragrafen | lat. Wörter | Hördauer (geschätzt) | Stand |
|---|---|---|---|---|
| 1 | 5 | 348 | 3:53 | übersetzt, Text am 29.10. nachgebessert; öffentlich noch Lupert als „Teil 1 und 2“ (alter Wortlaut) |
| 2 | 4 | 250 | 2:47 | übersetzt, Überarbeitung durch den Auftraggeber offen |
| 3 | 4 | 231 | 2:34 | Entwurf, Freigabe offen |
| 4 | 5 | 313 | 3:29 |  |
| 5 | 4 | 164 | 1:50 |  |
| 6 | 2 | 97 | 1:05 |  |
| 7 | 4 | 289 | 3:13 |  |
| 8 | 6 | 332 | 3:42 |  |
| 9 | 4 | 208 | 2:19 |  |
| 10 | 3 | 166 | 1:51 |  |
| 11 | 4 | 234 | 2:36 |  |
| 12 | 5 | 248 | 2:46 |  |
| 13 | 5 | 302 | 3:22 |  |
| 14 | 3 | 182 | 2:02 |  |
| 15 | 7 | 383 | 4:16 |  |
| 16 | 3 | 169 | 1:53 |  |
| 17 | 4 | 251 | 2:48 |  |
| 18 | 3 | 155 | 1:44 |  |
| 19 | 3 | 209 | 2:20 |  |
| 20 | 6 | 366 | 4:05 |  |
| 21 | 4 | 190 | 2:07 |  |
| 22 | 5 | 237 | 2:38 |  |
| 23 | 5 | 294 | 3:17 |  |
| 24 | 5 | 337 | 3:45 |  |
| 25 | 8 | 468 | 5:13 |  |
| 26 | 8 | 461 | 5:08 |  |
| 27 | 6 | 295 | 3:17 |  |
| 28 | 1 | 79 | 0:53 |  |

Gesamt: 28 Kapitel, 126 Paragrafen, 7.258 lateinische Wörter, Text etwa 80:53 min.

## Stimmensuche (offen)

Mit Lupert, Christian, Brian, Ralf Benz und Robert Ranger ist der Auftraggeber nicht zufrieden (Vergleich in
`messung/stimmen/vergleich_kap1_absatz12.json`; bester Messwert roh: Ralf Benz, Abstand 1,30, natürlicher Abfall am
Satzende −1,1 HT/s). Kapitel 1 (bisher Teil 1 und 2) wird mit der gewählten Stimme neu erzeugt.

Modellprüfung vom 28.10. (Einzelheiten in `UEBERGABE.md`): Das Modell bestimmt die Satzmelodie. Ralf Benz mit
Multilingual v2 (Stability 0,75) liegt bei 9,4 und 10,0 HT statt 13–14 HT mit v4 und hat den besten Abstand bisher
(0,66 und 1,01). Lupert taugt mit v2 nicht (kaum Pausen). Entscheidung per Hörvergleich steht aus.

Vorgehen, sobald ein ElevenLabs-API-Schlüssel als Umgebungsvariable `ELEVENLABS_API_KEY` vorliegt (ohne Anmeldung
liefert die Stimmenbibliothek nur 3 Stimmen und keine Filter):

1. Bibliothek abfragen (`GET /v1/shared-voices`, Sprache Deutsch, nur Männerstimmen, Einsatz Erzählung/Hörbuch, nach Nutzung sortiert),
   Hörproben (`preview_url`) laden; das kostet keine Credits.
2. Jede Probe messen wie in `werkzeuge/prosodie.py`: Tempo, Pausen, Melodie-Spannweite, Abfall am Satzende, Tonlage,
   Stimmqualität (HNR); Sprache per Whisper prüfen. Satzmelodie und Abfall zählen am meisten, weil sie sich nachträglich
   nicht korrigieren lassen; Pausen und Tempo schon.
3. Die besten 8 bis 10 mit ihren Hörproben in die Vorschau-App. Der Auftraggeber kann nicht benennen, was ihn stört;
   darum Vorliebe aus Paarvergleichen ermitteln (A/B-Duelle, Bradley-Terry-Schätzung) und gegen die Messwerte legen,
   um gezielt weiterzusuchen. Erste Stufe: Rangfolge der fünf bisherigen Stimmen.
4. Die 2 bis 3 Favoriten mit Kapitel 1, Absatz 1–2 erzeugen (je etwa 800 Credits) und wie oben vergleichen.
