# Plan: De vita beata vollständig übersetzen und vertonen

Seneca, *De vita beata* (an Gallio), 28 Kapitel, rund 7.260 lateinische Wörter; das Werk bricht in Kapitel 28 mitten im
Satz ab. Lateinischer Text: [The Latin Library](https://www.thelatinlibrary.com/sen/sen.vita.shtml), je Kapitel in
`texte/latein/kapitelNN.txt`. Eigene Übersetzung je Kapitel in `texte/kapitelNN.txt`, mit Stellenmarken „[1,2]“ vor dem
Satz, mit dem der lateinische Paragraf beginnt (nie gesprochen; `werkzeuge/stellen.py` entfernt sie vor Stimme, Prüfung
und Wortzeiten und liefert je Wort die Stelle für das Video). Endprodukt: ein YouTube-Video mit mitlaufendem Text.

Diese Datei enthält die gültigen Regeln (Stand 30.10.). Wie sie entstanden sind, mit Versuchen und Messungen: `PROTOKOLL.md`.

## Stil der Übersetzung

Festgelegt an Kapitel 1 nach den Rückmeldungen des Auftraggebers:

- Nah am Latein: Senecas Bilder, Gedankengang und Satzbau bleiben erkennbar, man soll merken, dass es ein antiker Text ist.
- Zugleich heutiges, flüssiges Deutsch zum Zuhören: nicht gestelzt, nicht flapsig, keine modernen Redensarten
  („tappen im Nebel“ geht nicht; „ist ihr Blick getrübt“ trifft es).
- Römische Begriffe bleiben (Prätor, Wahlen statt „Komitien“); Senecas Ansprache an den Leser als „du“.
- Für das Vorlesen gesetzt: Satzzeichen markieren Pausen, Gedankenstriche sparsam, keine Klammern.
- Kein „als wie“; Einschübe zwischen Gedankenstrichen lieber umstellen (die Stimme stockt sonst mitten im Satz);
  lange Kommaketten in zwei Sätze teilen. Bildhafte Wörter nur, wenn sie natürlich klingen (kein „Knäuel von Menschen“).

Gelernt aus den Korrekturen an Kapitel 1 (29.10.):

- **Verbindungswörter nach ihrer Funktion im Gedankengang**, nicht nach dem Wörterbuch: *atqui* in 1,3 führt die
  Begründung weiter („Denn nichts verstrickt uns …“), „Und doch“ hätte einen Gegensatz behauptet, den es nicht gibt.
  Gilt ebenso für *ergo*, *enim*, *autem*, *tamen*, *nam*, *quidem*.
- **Begriffe nach dem lateinischen Wort**, nicht nach dem, was im Deutschen gut klingt: *bona mens* ist „klarer Verstand“,
  nicht „Vernunft“ (das wäre *ratio*). Leitbegriffe stehen in der Begriffsliste unten und gelten im ganzen Werk.
- **Senecas Bilder durchhalten**, auch über Sätze hinweg: *sanabimur* ist „Geheilt werden wir“ – Seneca spricht von
  Krankheit und Heilung; „gesund werden“ verlor das Bild, und man fragt sich, woran wir krank sind.
- **Bezüge müssen beim Zuhören eindeutig sein**, man kann nicht zurücklesen: *ab ea … ad illam* ist „davon … darauf“,
  nicht „ihm“, wenn das Bezugswort weit zurückliegt.
- **Änderungen an vorgelegtem Text nur als Vorschlag**: alt → neu, mit dem lateinischen Grund; der Auftraggeber gibt
  frei, danach den ganzen Text noch einmal vorlegen.

## Begriffsliste

Gilt im ganzen Werk. Abweichen nur, wenn der Zusammenhang es verlangt, und dann dem Auftraggeber nennen. Neue
Leitbegriffe beim ersten Auftreten eintragen und vorlegen.

| Latein | Deutsch | Stand |
|---|---|---|
| *beatus*, *beata vita* | glücklich, glückliches Leben | festgelegt (Titel) |
| *bona mens* | klarer Verstand | festgelegt 29.10. (1,2) |
| *fortuna* | Schicksal (nicht „Glück“: „glücklich“ bleibt für *beatus*) | angenommen 30.10. |
| *voluptas* | Lust, Plural Lüste; Leitbegriff ab Kapitel 4 | angenommen 30.10. |
| *gaudium* | Freude | angenommen 30.10. |
| *virtus* | Tugend | angenommen 30.10. |
| *ratio* | Vernunft | angenommen 30.10. |
| *sapiens* | der Weise | angenommen 30.10. |
| *felicitas* | Glück (passt zu *beatus* → glücklich) | angenommen 30.10. (2,2) |
| *bonum*, *summum bonum* | das Gut, das höchste Gut (stoisches Fachwort, nicht umschreiben) | angenommen 30.10. (2,2) |
| *animus* | Geist | angenommen 30.10. (2,2) |
| *turba*, *vulgus*, *multitudo*, *coetus* | die Menge (bei Seneca hier gleichbedeutend) | angenommen 30.10. (1,4; 2,1–3) |

## Vom Auftraggeber festgelegt (nicht mehr ändern)

- 1,1 „Glücklich leben, mein Bruder Gallio, das wollen alle.“ (ohne „zu“)
- 1,1 „… je hastiger er darauf zustrebt“ (gewählt aus Varianten, 29.10.)
- 1,1 „… wird gerade die Eile zur Ursache einer noch größeren Entfernung.“
- 1,4 „Am Beispiel der anderen gehen wir zugrunde.“

## Ablauf je Kapitel

1. **Übersetzen** nach Stil und Begriffsliste, gegen den lateinischen Text prüfen und mit zwei freien Übersetzungen
   abgleichen: Aubrey Stewart, englisch 1900 ([Project Gutenberg 64576](https://www.gutenberg.org/ebooks/64576),
   „Of a Happy Life“), und Albert Forbiger, deutsch 1867 (nur als
   [LibriVox-Lesung](https://archive.org/details/vom_glueckseligen_leben_rr_librivox), per Whisper abgeschrieben;
   zeno.org sperrt automatische Abrufe). Stellenmarken setzen. **Textprüfung:** `python3 werkzeuge/textpruef.py N`
   (unbekannte und fremdsprachige Wörter, doppelte Wörter, Vorleseregeln, LanguageTool); jeden Hinweis klären, richtige
   seltene Wörter in `texte/woerter_ok.txt` eintragen. Nötig, weil die Worttreue-Prüfung einen Tippfehler im Text nicht
   findet: Er wird mitgesprochen und gilt dann als wortgetreu. Den ganzen Text vorlegen; Freigabe durch den Auftraggeber;
   vor der Aufnahme die Textprüfung noch einmal laufen lassen.
2. **Ton erzeugen:** `python3 werkzeuge/kapitel.py N <ordner> --ohne-video`. Das ganze Kapitel geht als **eine** Anfrage an
   ElevenLabs (Stimme und Einstellungen unten), die Rohaufnahme wird zwischengespeichert (`--neu` erzeugt neu und kostet
   Credits, etwa 0,43 je Zeichen). Danach automatisch: Worttreue (Whisper), Rauschunterdrückung, Wortzeiten, Pausen,
   Tempo 0,96, −18 LUFS (`werkzeuge/kette.py`: Satzende 0,9 s, Absatz 1,3 s, Doppelpunkt/Semikolon 0,55 s,
   Gedankenstrich 0,45 s, Komma 0,35 s – an Kommas nur dort, wo die Stimme schon mindestens 0,15 s absetzt, sonst wird
   mitten in den Sprechfluss geschnitten).
3. **Prüfliste Ton** (unten) abarbeiten, dann dem Auftraggeber als Seite zum Anhören schicken (Artifact mit Abspielknopf
   und Mitlesen, verdächtige Stellen anklickbar; nie als Datei).
4. **Nachbessern**, was der Auftraggeber meldet (Prüfliste, Punkt 4), bis zur Abnahme des Kapitels.
5. **Sichern**, sofort nach der Abnahme (Prüfliste, Punkt 6).
6. **Video:** `python3 werkzeuge/video/baue.py <daten.json> <ton.wav> <aus.mp4>` (oder `kapitel.py` ohne `--ohne-video`);
   Endkontrolle (Prüfliste, Punkt 5); Vorschau in 720p ins Artifact (höchstens 15 MB je Datei); die Full-HD-Datei für
   YouTube als Datei schicken; Miniaturbild mit `node werkzeuge/video/miniatur.js N <aus.png>`.
7. `UEBERGABE.md` (Stand, Credits) und `PROTOKOLL.md` (Versuche, Befunde) nachtragen, committen, pushen.

## Prüfliste Ton

Vor jedem Schicken an den Auftraggeber, in dieser Reihenfolge:

1. **Worttreue:** `werkzeuge/pruef.py large-v3-turbo`; bei Abweichung Gegenprobe mit `large-v3` (macht `kapitel.py`
   selbst). Bekannte Scheinfehler: „Walen“ statt „Wahlen“, „dem“ statt „den“ vor V. Erst wenn auch die Gegenprobe
   abweicht, die Stelle anhören bzw. vorlegen.
2. **Schnitte:** keine eingefügte Pause, wo die Stimme durchspricht (Regel `komma_ab` in Schritt 2). Bei jeder Änderung an
   den Pausenregeln die Stellen auf die Prüfseite legen.
3. **Betonung:** Whisper hört sie nicht; bisher findet sie nur der Auftraggeber. Befund vom 29.10.: Falsche Akzente kommen
   vor allem vom **Folgesatz im selben Text** („die vor uns hergeht“ richtig: ohne Folgesatz 6 von 6, Folgesatz nur als
   Zusammenhang 2 von 4, Folgesatz mitgesprochen 0 von 3; exakter Trendtest p = 0,005), und sie streuen stark zwischen zwei
   Erzeugungen (8 von 15 Sprechabschnitten anders). Das ganze Kapitel neu erzeugen hilft darum nicht. Vorfilter:
   `python3 werkzeuge/betonung.py <roh.mp3> <woerter.json>` markiert Sprechabschnitte, deren Tonhöhengipfel auf einem
   kleinen Wort liegt (Artikel, Pronomen, Präposition, Konjunktion, Hilfsverb). Die markierten Stellen kommen zuerst auf
   die Prüfseite; der Filter ersetzt das Ohr des Auftraggebers nicht. Test an Kapitel 1 (30.10.): echter Fehler 2 von 2
   markiert (+9,9 und +9,3 HT), richtige Fassungen derselben Stelle 0 von 8, abgenommene Fassung 7 von 79 Abschnitten
   (höchstens +4,7 HT), die der Auftraggeber alle als in Ordnung hörte. **Schwelle daher 5 HT** (Auftraggeber, 30.10.).
   Gestützt auf einen einzigen echten Fehler: Jeden weiteren Fehler, den der Auftraggeber findet, mit dem Abstand
   vergleichen, den der Filter dort misst (er zählt die Abschnitte zwischen 3 und 5 HT mit), und die Schwelle anpassen.
4. **Nachbessern einzelner Sätze:** den Satz **allein und ohne Zusammenhang** erzeugen, zwei bis drei Fassungen; die beste
   an den Satzpausen einsetzen (Rand 50/100 ms, Blende 10 ms, Pegel an den Satz davor angleichen), Stimme per
   Fingerabdruck prüfen (`werkzeuge/fingerabdruck.py`, mindestens 0,95 zur Kapitelaufnahme), dann die Kette neu und die
   Worttreue erneut prüfen. Alternative: den Satz ans Ende einer Anfrage stellen und zurückschneiden (Rückwärts-Test).
   Nicht bewährt: Satz für Satz mit Zusammenhang (`paragraf.py --saetze`, zweimal falsch). Werkzeug für das Einsetzen
   fehlt noch (bisher Handarbeit, siehe `PROTOKOLL.md`), vor Kapitel 2 bauen.
5. **Endkontrolle der Dateien:** Tonspur vorhanden, Stereo, 48 kHz, AAC-LC (YouTube-Empfehlung; eine Mono-Datei kam am
   Handy stumm an), −18 LUFS; Dauer gleich `ende` in `daten.json`; Stichbilder am Anfang (Startseite), in der Mitte und am
   Ende ansehen; Seiten im Browser in Handygröße testen (`CLAUDE.md`).
6. **Sichern:** Der Container wird gelöscht. Abgenommene Rohaufnahmen (Rohaufnahme mit eingesetzten Sätzen, Startsatz,
   Pausenfassung, Wortzeiten, Pausenstellen, `daten.json`) sofort ins private Vorschau-Artifact unter `quelle/`;
   daraus baut `kapitel.py` Ton und Video ohne Credits neu. Eine Neuerzeugung brächte andere Betonungen.

## Stimme

Helmut Stieglbauer – Deep and Dynamic (`JiW03c2Gt43XNUQAumRP`, in ElevenLabs ein Professional Voice Clone, also ein echter
Sprecher), Modell eleven v4, Stability 0,5, übrige Einstellungen wie die Stimme; Tempo 0,96 nachträglich mit ffmpeg
(Tonhöhe bleibt). Gewählt am 29.10. nach zwei Duellrunden und der Stimmenprobe; Lupert und die übrigen Stimmen sind
raus (Verlauf in `PROTOKOLL.md`). Bei YouTube „Verwendung von KI“ mit Ja beantworten.

Umfang: etwa 67.000 Zeichen für das ganze Werk, also etwa 28.800 Credits für einen Durchgang ohne Nachbesserungen.

## Kapitel

Seit 29.10. ist Senecas Kapitel die einzige Einheit (vorher 29 „Teile“ nach Hörlänge: Kapitel 1 geteilt, 5+6 und 27+28
zusammengelegt, 25 und 26 halbiert). Bisherige Teile: 1+2 → Kapitel 1, 3 → 2, 4 → 3, 5 → 4; ab Teil 7 ist Teil = Kapitel bis 24.
Wörter gezählt im lateinischen Text ohne Paragrafennummern; Hördauer geschätzt mit 0,669 s je Wort (Helmut, Tempo 0,96,
gemessen an 1,1–2). Ein Kapitel geht als eine Anfrage an ElevenLabs; das längste (25) hat deutsch etwa 4.300 Zeichen.

| Kapitel | Paragrafen | lat. Wörter | Hördauer (geschätzt) | Stand |
|---|---|---|---|---|
| 1 | 5 | 348 | 3:53 | **fertig:** Text freigegeben, Ton und Video mit Helmut (30.10.); öffentliche Seite noch Lupert |
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
