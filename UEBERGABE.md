# Übergabe – Stand 28.10.2026, abends

## Links

- Öffentliche Hörbuch-Seite (Teil 1 und 2): https://luperttrading-lab.github.io/seneca-audio/
- **Private Vorschau mit Modellvergleich vom 28.10.** (Teil 1 und 2 plus 7 Proben Ralf/Lupert; Quelle:
  `seite/bau_hoerbuch.py seite/karaoke.json <ordner> --artifact --vergleich messung/stimmen/vergleich_modelle.json`):
  https://claude.ai/artifact/Mj5fSGP6WhXq3iSCjZCqxt
- **Stimmen-Duell** (privat, Speicher `duelle` mit `{a, b, w: "a"|"b"|"=", t}`; Quelle `seite/duell.html`, Stimmen in
  `messung/stimmen/duell_stimmen.json`, Ton nur im Artifact): https://claude.ai/artifact/SMVhWQ4Qcto92tmNYbE6fM
- **Kapitel 1 · Vorschau** (privat, 29.10.; Video 720p und Tonspur von Kapitel 1 mit neuem 1 (3); Quelle
  `seite/vorschau_kapitel01.html`): https://claude.ai/artifact/Pa3cLB5TEbA2WvmnNQiVy9
- **Kapitel 1 · Prüfstellen** (privat, 29.10.; zwei verdächtige Stellen in 1 (3) zum Anhören mit Mitlesen; Quelle
  `seite/pruefstellen.html`): https://claude.ai/artifact/9oVZgpKioSQuSDG4DCfBJE
- **Stimmenprobe** (privat; drei Reiter: alle sieben Helmut-Fassungen mit Teil 1, Absatz 1–2 und Absatz 3–4, dazu
  Helmut, Alexander, Marko, Marcus mit Absatz 1–2; bearbeitet wie im Hörbuch, mit Mitlesen und Temporad; Quelle `seite/stimmenprobe.html`): https://claude.ai/artifact/G9tMfCirpybCFyQYne2d6L
- **Lupert tiefer** (privat, vier Fassungen umschaltbar an derselben Stelle; Quelle `seite/lupert_tiefer.html`):
  https://claude.ai/artifact/4Bx1FXUbjvxuH9n4UDmaWE
- Ältere private Vorschau mit dem Stimmenvergleich vom 27.10. (Lupert, Christian, Brian, Ralf, Robert, alle v4):
  https://claude.ai/artifact/Mi3DHEtyiHRPXEYfwj5XA9
- Ältere private Vergleichsseite zu Teil 1 (Lupert, Christian, Gemini): https://claude.ai/artifact/RfZhGX4jPHk6ZFfHaLhjVr

## Stand

**Seit 29.10. zählen wir nur noch nach Senecas 28 Kapiteln** (Nutzer: die eigenen „Teile“ verwirren mehr, als sie
bringen). Bisher Teil 1+2 → Kapitel 1, Teil 3 → Kapitel 2, Teil 4 → Kapitel 3. Weiter unten in dieser Datei meint „Teil“ noch
die alte Zählung. Gliederung: `GLIEDERUNG.md`; Kapiteltabelle: `PLAN.md`.

| Kapitel | Text | Aufnahme |
|---|---|---|
| 1 | fertig, am 29.10. nachgebessert (`texte/kapitel01.txt`, Marken 1,1–1,5) | **neu mit Helmut erzeugt (29.10.)**; Nutzer fand in 1 (3) zwei holprige Schnitte (Komma-Pausen ohne echte Sprechpause,
 behoben: `komma_ab` 0,15 in `werkzeuge/kette.py`) und eine sinnwidrige Betonung (Stelle offen). 1 (3) neu gesprochen mit
 `werkzeuge/paragraf.py 1 3 <ordner>` (200 Credits, wortgetreu), liegt auf der Prüfseite neben der alten Fassung; in Kapitel 1 eingesetzt (Ränder 50/100 ms, Pegel −0,5 dB), Kapitel
 neu bearbeitet: wortgetreu, 39 statt 58 Pausen, 3:53, Video im Scratchpad `kapitel01_neu/` (Full HD, 64 MB). Offen: Feinschliff
 „die vor uns hergeht“ (Varianten A/B auf der Prüfseite, Wahl des Nutzers). Nutzer hat den ersten Satz von 1 (3) selbst in der
 App mit Helmut erzeugt (gleiche Stimme, Fingerabdruck 0,95; App-Einstellungen: Stability 0,5, Similarity 0,81, die API
 nimmt ohne Angabe den Standardwert): dort Betonung auf „HERgeht“ statt „VOR“; liegt bearbeitet auf der Prüfseite;
 **Versuch (29.10.):** derselbe Satz sechsmal einzeln erzeugt (je 2× ohne Similarity, mit 0,81, mit 0,81 und Satz davor/danach):
 alle 6 und die App-Aufnahme betonen „hergeht“ (mit Fall von 10–15 HT wie am Satzende), beide Fassungen aus langem Text
 „vor“ (`messung/stimmen/versuch_vor_uns_hergeht.json`). Ursache ist also, ob der Satz allein oder im längeren Text steht,
 nicht Similarity oder Zusammenhang. Stimm-Standard laut API: similarity 0,75, style 0,55, speaker boost an; `werkzeuge/kapitel.py 1 <ordner>`, 1.321 Credits, Rohaufnahme wortgetreu (499/499), 58 Pausen verlängert, Tempo 0,96, −18 LUFS, Video 3:57 (1920 × 1080, 66 MB). Liegt nur im Scratchpad, Urteil des Nutzers offen; öffentlich noch Lupert als „Teil 1“ und „Teil 2“ |
| 2 | fertig (`texte/kapitel02.txt`), mit Stewart und Forbiger abgeglichen; Nutzer will Stellen überarbeiten | fehlt |
| 3 | Entwurf (`texte/kapitel03.txt`), mit Stewart und Forbiger abgeglichen, Freigabe offen | – |
| 4–28 | Latein in `texte/latein/kapitelNN.txt` | – |

Die öffentliche Seite (`seite/bau_hoerbuch.py`, Liste `TEILE`) zeigt bis zur Neuvertonung von Kapitel 1 weiter die alten
Teile 1 und 2; umgestellt wird erst mit Freigabe des Nutzers. `seite/karaoke_daten.py` verweist für `a-teil02` noch auf
`texte/teil02.txt` (gelöscht; der alte Text steht in der Git-Historie).

## ElevenLabs-Schlüssel

Eingerichtet als Umgebungsvariable `ELEVENLABS_API_KEY` (eingeschränkt: Text zu Sprache, Stimmen lesen, Modelle,
Verlauf lesen, Benutzer; Abschalten bei Leak an). Stimmen schreiben ist bewusst gesperrt (könnte den Lupert-Klon löschen):
Bibliotheksstimmen lassen sich trotzdem direkt per API sprechen lassen (am 28.10. mit Otto geprüft), ohne sie hinzuzufügen. `api.elevenlabs.io` ist erreichbar.
`/v1/user` und `/v1/user/subscription` antworten mit 401, das Kontingent ist also nicht abfragbar.

Seit 28.10. ist der **neue Schlüssel (30.000 Credits Grenze)** aktiv. Eine API-Anfrage kostet laut Kopfzeile
`character-cost` 336–337 Credits für Absatz 1–2 (785 Zeichen), also etwa **0,43 Credits je Zeichen**, bei v4, v2 und
Storytel gleich. Die App hat für dieselben 785 Zeichen 766 Credits berechnet. Am 28.10. verbraucht: 7 Anfragen, 2.356
Credits; Rest also höchstens etwa 27.600. Dazu Stimmen-Duell 1.757 Credits (25 × 70 plus Test), Runde 2 1.200 Credits und am 29.10. die
Stimmenprobe 1.348 Credits (4 × 337) und 602 (2 × 301) und 1.505 (5 × 301) und 2.022 (6 × 337), Probefilm 24 (Titel und Startsatz),
Kapitel 1 mit Helmut 1.321, Paragraf 1 (3) neu 200, Versuch „vor uns hergeht“ 438: zusammen etwa 12.780 verbraucht,
höchstens etwa 17.220 übrig. **Das reicht nicht für das ganze Werk:** etwa 67.000 Zeichen (9,1 Zeichen je
lateinisches Wort aus Teil 1–4, 7.395 Wörter) kosten etwa 28.800 Credits für einen einzigen Durchgang ohne Neuversuche.
Der Nutzer muss die Grenze des Schlüssels erhöhen, sofern das Konto die Credits hat. Der alte Schlüssel sollte gelöscht
werden, falls noch nicht geschehen.

## Befunde vom 28.10. (Messung der Takes aus dem Verlauf)

Werte in `messung/stimmen/takes_verlauf.json`, gemessen mit `werkzeuge/messen_abstand.py` (gleiche Merkmale wie
`prosodie.py`, Abstand wie im alten Vergleich; Robert, Brian und Ralf Take A treffen die alten Werte exakt).

- Alle v4-Proben liefen mit Stability 0,5, Similarity 0,75–0,81 oder Standard. Höhere Stability ist also ungeprüft.
- Jede Erzeugung in der App liefert zwei Takes. Streuung zwischen den beiden Takes einer Anfrage (σ je Take):
  Melodie 0,32 HT, Abfall 0,63 HT/s, Pausenanteil 0,8 %, Abstand 0,82. Zwischen den Stimmen (Absatz 1–2): Melodie
  1,68 HT, Abfall 0,71 HT/s. Melodie ist eine verlässliche Stimmeigenschaft, der Abfall nicht (Zuverlässigkeit einer
  einzelnen Messung etwa 0,4). Ralfs Bestwert 1,30 war Glück: Take B hat 2,69.
- Gottfried (27.10.): Melodie 14,2 / 13,7 HT, Abstand 4,63 / 1,93; gleiches Muster wie die anderen Bibliotheksstimmen.
- **Lupert widerspricht der Modell-These teilweise:** gleiche Stimme, gleiches Modell v4, Melodie 10,7 / 10,3 HT
  (05:23, Absatz 1–2 allein, Similarity Standard), 13,0 / 13,05 HT (07:32, ganz Teil 1, Similarity 0,75; daraus stammt
  der Wert 13,0 im alten Vergleich, Take mit `eleven_v4_exp`), 11,4 / 11,0 und 11,4 / 12,1 HT (Teil 2). v4 kann also
  ruhig klingen. Der Sprung 10,5 → 13,0 bei Lupert liegt weit über der Take-Streuung; Ursache offen (Similarity,
  längerer Text im Auftrag oder Streuung zwischen Anfragen, die größer ist als zwischen Takes einer Anfrage).
- Luperts Schwäche ist das Phrasieren: Pausenanteil 9–11 % statt 13–20 %, 10–11 Wörter je Phrase statt 4–7. Die eigene
  Lesung des Nutzers (`mensch_nutzer` in `messung/merkmale.json`): Melodie 8,6 HT, Abfall −0,41, Pausen 22 %.
- Bibliotheksstimmen: Hörprobe gegen v4 (5 Stimmen, Mittel beider Takes): r = 0,80, Steigung 0,28 (p ≈ 0,1, n = 5).
  Hörproben streuen 8,3–15,4 HT, dieselben Stimmen in v4 nur 13,4–15,9 HT. v4 drückt Bibliotheksstimmen offenbar auf
  13 HT und mehr; eine Suche über Hörproben findet so keine Stimme unter 12 HT. Hörproben sind zudem nur 4–10 s lang.
  Screening von 189 Stimmen (Erzählung/Bildung, nicht jung) mit `werkzeuge/bib_screening.py`: 47 gemessen, Werte in
  `messung/stimmen/screening_hoerproben.json`; abgebrochen, weil Hörproben wenig vorhersagen.

## Befunde der Modellprüfung vom 28.10. (API, Absatz 1–2)

Werte in `messung/stimmen/modellpruefung_api.json` (alle Merkmale, Modell, Einstellungen) und
`messung/stimmen/vergleich_modelle.json` (Auszug für die Vorschau). Je Anfrage liefert die API nur einen Take. Proben
liegen nur im Artifact (`audio/v_*.mp3`, −18 LUFS, Limiter 0,84), nicht im Repo.

| Probe | Melodie HT | Abfall HT/s | Pausen % | Wörter/Phrase | Tempo W/s | Abstand |
|---|---|---|---|---|---|---|
| Ralf, Multilingual v2, Stab. 0,75, Probe 1 | 9,42 | −1,51 | 14,2 | 7,9 | 3,14 | 1,01 |
| Ralf, Multilingual v2, Stab. 0,75, Probe 2 | 10,03 | −0,58 | 16,1 | 7,4 | 3,26 | 0,66 |
| Ralf, v4, Stab. 1,0 | 13,59 | −2,03 | 13,5 | 7,4 | 2,97 | 1,95 |
| Ralf, Storytel v2, Stab. 0,75 | 6,90 | −2,97 | 20,9 | 6,1 | 2,68 | 3,60 |
| Lupert, v4, Stab. 0,5 (wie 27.10. 05:23), Probe 1 | 12,84 | −2,56 | 8,6 | 9,5 | 3,03 | 3,86 |
| Lupert, v4, wie oben, Probe 2 | 13,42 | −2,53 | 9,4 | 9,0 | 3,03 | 4,22 |
| Lupert, Multilingual v2, Stab. 0,75 | 7,92 | −1,99 | 3,9 | 12,5 | 3,21 | 7,08 |

Zielbereich echter Vorleser: Melodie 10,0–11,7 HT, Abfall −1,58 bis −0,51, Pausen 13,4–20,2 %, 4,4–7,4 Wörter je
Phrase; Tempo-Wunsch 2,6–3,0 W/s.

- **Das Modell ist der Hebel für die Melodie, nicht die Stability.** Ralf mit v4 bleibt auch bei Stability 1,0 bei
  13,6 HT. Mit Multilingual v2 kommt er auf 9,4 und 10,0 HT; der Unterschied zwischen den beiden Anfragen (0,6 HT) ist
  klein gegen den Modellunterschied (etwa 3,9 HT). Ralf v2 hat die besten Abstände bisher (0,66 und 1,01). Er ist
  etwas zu schnell (3,1–3,3 W/s); v2 kennt `voice_settings.speed` (Brian lief im April mit 0,92), ungeprüft für Ralf.
- **Luperts 10,5 HT vom 27.10. lassen sich per API nicht wiederholen:** gleicher Text, gleiche Einstellungen, 12,8 und
  13,4 HT. Ursache offen: Die App schickt vielleicht andere Standardwerte als die API (Similarity „Standard“), oder die
  Streuung zwischen Anfragen ist groß. Mit v2 hetzt Lupert (3,9 % Pausen, 12,5 Wörter je Phrase); als
  Hörbuchstimme mit v2 also unbrauchbar, mit v4 bleibt die Phrasierung die Schwäche.
- **Lupert hat zwei Proben** (`GET /v1/voices/xoLW9SizYThZnEEVer1q`, Instant-Klon, angelegt 27.10. 05:23 UTC):
  `recording-1793078461.mp3` (30 s, im Browser aufgenommen 27.10. 05:21 UTC) und `Seneca.mp3` (55 s, Datum nicht
  abfragbar; vermutlich die eigene Seneca-Lesung des Nutzers, nachträglich hinzugefügt). Der Nutzer nennt die Stimme
  seit dem zusätzlichen Text „Katastrophe“. Naheliegende Erklärung für den Sprung 10,5 → 13 HT zwischen 05:23 und 07:32:
  nicht das Modell, sondern der veränderte Klon. Prüfung: `Seneca.mp3` in der App entfernen (der Schlüssel darf keine
  Stimmen schreiben; API-Weg wäre `DELETE /v1/voices/{voice_id}/samples/{sample_id}`), dann zwei Proben Lupert v4 wie
  05:23 erzeugen und messen. Geht das Entfernen in der App nicht: die 30-s-Aufnahme per API laden
  (`GET /v1/voices/{voice_id}/samples/{sample_id}/audio`) und daraus einen neuen Instant-Klon anlegen lassen.
- Inhalt der beiden Lupert-Proben (per API geladen, nur im Sitzungsordner, nicht im Repo): `Seneca.mp3` ist die
  eigene Lesung des Nutzers von Absatz 1–2, akustisch identisch mit `mensch_nutzer` (alle 12 Merkmale gleich), also
  keine neue Aufnahme von heute. `recording-….mp3` ist der Mustertext von ElevenLabs („Ich erinnere mich noch gut an das
  erste Mal …“), schnell und mit langen Phrasen gelesen (Pausen 11,6 %, 13,3 Wörter je Phrase, Melodie 6,4 HT).
  Wann `Seneca.mp3` hinzukam, liefert die API nicht. Klangfarbe (Langzeitspektrum und MFCC, `klang.py`-Ansatz: Lage auf
  der Achse Aufnahme → Seneca): 05:23 −0,24 / −0,20, gestern 07:32–11:38 −0,04 bis +0,34, heute per API +0,74 / +0,56
  (gleicher Text wie 05:23). Also wahrscheinlich am 27.10. zwischen 05:23 und 07:32 UTC hinzugefügt.
- **Lupert spricht 2,5 HT höher als der Nutzer:** Grundfrequenz 116–120 Hz, der Nutzer 99 Hz (Mustertext) und 104 Hz
  (Seneca). Gestern wurde die Tonhöhe nicht bearbeitet: Teil 1 hat 117,7 Hz wie der rohe Take, Teil 2 116,2 Hz; die
  Seite spielt mit Tempo 0,95 bei festgehaltener Tonhöhe (`preservesPitch`). Bearbeitet wurden nur Pausen und Lautheit.
- Storytel v2 ist zugänglich, macht Ralf aber sehr flach (6,9 HT) und langsam; Whisper hört „Ziel“ als „Seel“ und
  „entgegen“ verschliffen. Die anderen sechs Proben sind wortgetreu (`pruef.py large-v3-turbo`).
- Grenze der Messung: n = 2 Proben für Ralf v2, n = 1 für die übrigen; der Abfall streut stark (−1,51 / −0,58).

## Pausentest vom 28.10.: warum Teil 1 gut klingt

Der Nutzer findet Teil 1 „richtig gut“ und Luperts API-Probe von heute „Katastrophe“. Herkunft der öffentlichen Teile:
Teil 1 = Take von 07:32 UTC mit `eleven_v4_exp` (App, 91,44 s, identisch mit `a-lupert_exp` und dem alten `v_lupert`)
plus 10,0 s Pausen („ruhig“: Satzende 0,9, Absatz 1,3, Doppelpunkt 0,55, Gedankenstrich 0,45, Komma 0,35 s, wo schon
abgesetzt wird); Teil 2 = Take von 11:38 UTC (94,75 s) plus 10,2 s Pausen. Messung Absatz 1–2:

| Fassung | Melodie HT | Pausen % | Wörter/Phrase | Abstand |
|---|---|---|---|---|
| Teil 1 roh (App, v4 exp) | 13,00 | 8,4 | 11,2 | 5,34 |
| Teil 1 bearbeitet (öffentlich) | 13,22 | 16,6 | 9,2 | 2,98 |
| heute roh (API, v4) | 12,84 | 8,6 | 9,5 | 3,86 |
| heute bearbeitet wie Teil 1 | 12,73 | 16,1 | 9,2 | 2,40 |
| Ralf v2 Probe 2 bearbeitet wie Teil 1 | 10,06 | 25,0 | 6,0 | 1,97 |

- Roh ist Teil 1 nicht besser als die heutige Probe. Der Unterschied liegt in der Nachbearbeitung (Pausen verdoppelt) und
  im Abspieltempo 0,95. Das gilt als wahrscheinlich, bis der Nutzer „heute bearbeitet“ gehört hat.
- **Korrektur:** Die Melodie von 13 HT stört den Nutzer offenbar nicht, denn Teil 1 hat sie auch. Der Zielbereich 10–11,7 HT
  aus den Vorlesern ist also kein Maß für seine Vorliebe. `Seneca.mp3` vorerst **nicht** löschen; Teil 1 entstand
  wahrscheinlich schon mit beiden Proben.
- Vergleiche zwischen Stimmen nur noch bearbeitet und mit Tempo 0,95 anbieten; die Vorschau hat dafür den Abschnitt
  „Teil 1 gegen heute: Pausen“ (`PAUSENTEST` in `seite/bau_hoerbuch.py`). Ralf v2 pausiert schon roh genug; mit dem
  Teil-1-Profil kommt er auf 25 % Pausen, für ihn wäre ein schwächeres Profil richtig.

Hörurteil des Nutzers dazu: zwischen den vier Lupert-v4-Fassungen (Teil 1 roh/bearbeitet, heute roh/bearbeitet) „keine
großen Unterschiede“. Lupert v4 per API klingt also wie in der App, und die Pausenbearbeitung ist für ihn kein großer
Faktor. Die „Katastrophe“ ist Lupert mit Multilingual v2 (vom Nutzer am 28.10. bestätigt). Lupert also nur mit v4 erzeugen. Tempo 0,5 hat er
nicht in ElevenLabs eingestellt (kein Verlaufseintrag mit `speed` 0,5, alle Takes 2,9–3,1 W/s), sondern vermutlich am
Temporad der alten Hörseite (`seite/vorlage.html`, 0,5–1,5, nur Abspielen, Tonhöhe bleibt, im Browser gespeichert).

Tempo-Vorliebe aus der Sitzung „Allgemeine Fragen“ (Bildschirmfoto des Nutzers): Christian gefiel ihm am Temporad bei
0,93 (128 Wörter/min, eigene Lesung 139); empfohlener Startwert dort 0,92 (2,66 W/s Sprechtempo). Die öffentliche Seite
spielt mit 0,95. Seit 28.10. spielt die Vorschau alle Vergleichsproben mit 0,95; vorher lief der Stimmenvergleich mit 1,0,
was schnelle Proben (Lupert v2: 3,21 W/s) noch gehetzter klingen ließ. Die parallele Sitzung „Seneca Hörspiel“ empfahl
einen zweiten Klon aus der 30-s-Aufnahme; das ist nach dem Pausentest überholt (Teil 1 entstand schon mit `Seneca.mp3`).

## Stimmensuche vom 28.10. abends

Nutzerurteil: Ralf gefällt ihm auch mit v2 nicht; Teil 3 noch nicht erzeugen, er will erst Textstellen überarbeiten.
Weil die Messwerte seinen Geschmack nicht vorhersagen (Teil 1 mit 13 HT gefällt), entscheidet sein Ohr per Paarvergleich.
Stufe 1: 25 Stimmen sprechen dieselben zwei Sätze („Glücklich leben … ist ihr Blick getrübt.“, 164 Zeichen) mit v4,
Stability 0,5; −18 LUFS; alle wortgetreu. 20 neue deutsche Muttersprachler aus 990 Bibliotheksstimmen (Erzählung/Bildung,
Standarddeutsch, nicht jung, ruhige Beschreibungen, Rate 1,0, nach Nutzung) und 5 bekannte Anker (Lupert, Christian,
Ralf, Robert, Gottfried). Das Duell paart blind und adaptiv (wenig gehörte Stimmen zuerst, ähnliche Stärke), schätzt
Bradley-Terry mit einem gedachten Sieg und einer Niederlage je Stimme. Prüfstein: Landen Lupert und Christian oben und
Ralf unten, misst das Duell seinen Geschmack. Stufe 2: die 3 bis 5 Besten mit Absatz 1–2 (je etwa 340 Credits),
bearbeitet wie Teil 1, gegen Lupert.

Ergebnis Runde 1 (52 Duelle, 9 unentschieden, 17:18–17:49 UTC, Median 26 s je Duell; Rohdaten
`messung/stimmen/duell_ergebnis_runde1.json`). Bradley-Terry, Gewinnchance gegen den Durchschnitt (80-%-Bootstrap-Band):
Alexander – Deep TV Narrator 81 % (65–86), Leo Liest – Deep and calm 81 % (64–87), Robert Ranger 78 %, Gottfried 73 %,
Marcus – Emphatic and Reflective 69 %, Marko – Gentle and Quiet 68 %, Helmut Stieglbauer 67 %; ganz unten Otto 26 %,
**Lupert 24 % (1 Sieg, 4 Niederlagen)**, Ralf 18 %, Daniel 11 %. **Die Tonlage erklärt die Wahl:** Spearman Stärke ~ F0
ρ = −0,72 (Permutations-p < 0,001); in entschiedenen Duellen mit mehr als 3 Hz Unterschied gewinnt die tiefere Stimme 25
von 33 (76 %, einseitig p = 0,002). Satzmelodie ρ = −0,20 (p = 0,33), also bedeutungslos. Die ersten sieben liegen bei
93–110 Hz, die letzten fünf bei 116–135 Hz. Lupert (116 Hz) liegt 2,5 HT über der echten Stimme des Nutzers.

Was der Nutzer selbst nennt (nach Runde 1): gut war ein klarer Klang der ganzen Aufnahme, nicht nur der Stimme; störend
ein leichtes Lachen in der Betonung am Ende des ersten Satzes („das wollen alle“). Nächste Proben deshalb mit einem
anderen Abschnitt, nicht wieder mit dem Anfang. Gemessen (25 Proben): Klarheitsmaße erklären über die Tonlage hinaus
nichts (HNR, CPPS, Präsenz 2–5 kHz, Luft 5–11 kHz, Grundrauschen: alle |ρ| ≤ 0,08 ohne Tonlage, p ≥ 0,7). Ende von
„alle“: schwächer fallende Enden schneiden etwas besser ab (ρ = +0,33, p = 0,11, nicht gesichert). Ein Lachen erkennt
die Messung nicht; das bleibt Sache des Ohrs.

Gesamtgliederung (Abschnitte, Kapitel, 126 Paragrafen, geschätzte Dauer): `GLIEDERUNG.md`.

## Offen, in dieser Reihenfolge

1. **Stimme gewählt: Helmut Stieglbauer – Deep and Dynamic** (`JiW03c2Gt43XNUQAumRP`, 29.10., nach der Stimmenprobe:
   „definitiv die erste Stimme“; auf der Probe stellte er Tempo 0,96 ein, 134 W/min). Noch offen: Stimme in der App unter
   „Meine Stimmen“ aufnehmen (Kündigungsfrist 730 Tage gilt vermutlich nur dann).
   **Suche nach ähnlichen Stimmen** (kostenlos, Hörproben): Sprecher-Fingerabdruck WeSpeaker ResNet34 (ONNX,
   `werkzeuge/fingerabdruck.py`, Modellpfad in `WESPEAKER_ONNX`). Geprüft an Runde 1: Hörprobe → v4-Probe derselben
   Stimme auf Platz 1 bei 23 von 24; gleiche Stimme Kosinus Median 0,79, fremde 0,24 (95-%-Quantil 0,45). Ergebnis
   (`messung/stimmen/aehnlich_helmut.json`): 0,82 „Helmut – Warm, Gentle and Soothing“ (gleicher Besitzer,
   Märchenerzähler), 0,81 „Helmut – Clear and Confident“ und 0,79 „German Narration … Helmut Clark“ (anderer Besitzer,
   klingt wie derselbe Sprecher), dann erst 0,57 Thomas Schendel, 0,54 „Christian – Velvet Close-Up“. Derselbe Besitzer
   hat noch „Helmut – Natural & Engaging“ (Gespräch) und „Helmut – German Epic Trailer Voice“ (Werbung). Nächster
   Schritt (Credits, Freigabe offen): 2–4 davon mit Absatz 1–2 auf die Stimmenprobe.
   Alle Helmut-Stimmen der Bibliothek (`messung/stimmen/helmut_stimmen.json`): sieben Stimmen auf zwei Konten
   (46b55935…, 2cf3785c…) liegen bei 0,77–0,82 zu Stieglbauer, also vermutlich derselbe Sprecher; drei weitere „Helmut“
   (0,26–0,46) sind andere Männer. Nutzer: „Helmut – Distinctive and Authentic“ klingt zu sehr nach Märchenerzähler;
   „German Narration … Helmut Clark“ und Stieglbauer gut. Neue Probe Teil 1, Absatz 3–4 (700 Zeichen, je 301 Credits)
   mit beiden, auf der Stimmenprobe als zweiter Reiter. Laut ElevenLabs-Hilfe belegen gespeicherte Bibliotheksstimmen
   keine eigenen Stimmplätze; die Kündigungsfrist gilt ab der ersten Nutzung auch ohne Speichern.
   Auf Wunsch alle sieben Helmut-Fassungen mit Absatz 3–4 auf der Stimmenprobe (5 × 301 Credits zusätzlich).
   Unterschiede (Rohaufnahmen, `messung/stimmen/helmut_unterschiede.json`): Fingerabdruck untereinander 0,81–0,94,
   also derselbe Sprecher. Ausreißer ist Nr. 5 „Distinctive and Authentic“: geringste Ähnlichkeit (Mittel 0,86), tiefster
   Grundton (103 Hz, die anderen 114–130), deutlich hellerer Klang (Spektralschwerpunkt 964 Hz statt 600–700), rauer
   (HNR 8,8 statt 10–11). Zweiter Ausreißer Nr. 7 Trailer (hell, rau, am langsamsten). **Nutzer bestätigt: Nr. 5 ist die,
   die er als anders hört.** Auf Wunsch alle sieben auch mit Absatz 1–2 (6 × 337 Credits, Stieglbauer aus der ersten
   Probe), auf der Stimmenprobe als erster Reiter, gleiche Nummern. Gegenprobe an diesem Text
   (`messung/stimmen/helmut_unterschiede_absatz12.json`): wieder Nr. 5 am fernsten (0,85), tief (105 Hz), hell (1.146 Hz),
   rau (HNR 8,6); Nr. 7 wieder zweiter. Dieselbe Fassung an beiden Texten 0,96–0,97, verschiedene Fassungen 0,88; jede
   Aufnahme findet ihre eigene Fassung wieder (7 von 7). Die Fassungen unterscheiden sich also beständig, nicht zufällig.
   **Kosten laut Nutzer:** 1.000 Credits ≈ 0,10 € im Sparabo, sonst 0,20 €. Das ganze Werk (~29.000 Credits) kostet
   also 3–6 €; die Kosten dieser Claude-Sitzung sind um ein Vielfaches höher. Sparen lohnt bei der Arbeit, nicht bei
   den Credits; die Grenze des Schlüssels (30.000) bleibt aber ein hartes Limit.
   Davor: **Runde 2b** (29.10.): Nutzer wählte auf der Hörseite „Lupert tiefer“ die Fassung PSOLA −3,3 HT mit Pausen und
   Rauschunterdrückung und will sie **im Duell** gegen die anderen hören, **nicht** schon für Teil 1 und 2. Damit der
   Vergleich fair ist, bekamen alle neun Proben dieselbe Bearbeitung (Rauschunterdrückung, dann Pausen wie Teil 1,
   −18 LUFS): 7 Bibliotheksstimmen, Lupert, Lupert tiefer. Speicher `duelle2b`, Stimmen in
   `messung/stimmen/duell_stimmen_runde2b.json`. Die eine Wahl in `duelle2` (mit der kaputten Fassung) ist verworfen.
   Vorbereitet, aber nicht angewendet: `werkzeuge/verarbeite.py` (Rohaufnahme → Hörbuchfassung mit Tonlage 100 Hz,
   Rauschunterdrückung, Pausen nach PLAN-Regel, −18 LUFS, AAC und MP3, Wortzeiten). Teil 1 und 2 damit testweise
   gerechnet (nur im Sitzungsordner, nicht veröffentlicht; Whisper hört in Teil 1 „anderem Reisen“, ungeprüft).
   **Ergebnis Runde 2b** (28 Duelle, 6 unentschieden, `messung/stimmen/duell_ergebnis_runde2b.json`): Helmut Stieglbauer
   72 % (Top 3 in 88 % der Bootstrap-Ziehungen), Alexander 71 % (88 %), Marko 69 % (72 %), Marcus 56 %, Gottfried 47 %,
   Leo Liest 42 %, Robert 35 %, **Lupert 34 %, Lupert tiefer 24 %** (1 Sieg, 5 Niederlagen; im direkten Duell gewann
   Lupert unverändert). Tonlage erklärt diesmal nichts (ρ = +0,35, p = 0,36; die tiefere Stimme gewinnt 7 von 20).
   Rangkorrelation Runde 1 ↔ 2b für dieselben 8 Stimmen ρ = +0,05: oben sind die Stimmen für ihn fast gleich gut.
   Stabil über beide Runden: Alexander, Helmut, Marko oben; Lupert unten. Alle drei: Kündigungsfrist 730 Tage, Rate 1,0
   (gilt vermutlich nur, wenn die Stimme in „Meine Stimmen“ aufgenommen ist). Nächster Schritt mit dem Nutzer
   besprechen, nichts bauen, bevor er zustimmt.
   Vorher: **Runde 2** (vom Nutzer freigegeben, 1.200 Credits; Speicher `duelle2`, Stimmen in
   `messung/stimmen/duell_stimmen_runde2.json`, Seite `seite/duell.html` jetzt Runde 2). Lupert wurde mit Rubber Band
   formanterhaltend um 3,3 HT auf 100 Hz gesenkt (er sprach den Abschnitt mit 121 Hz). In diesem Abschnitt liegen alle
   Stimmen höher als in Runde 1 (Alexander 99 → 114 Hz). Whisper: „Wahlen“ als „Walen“ (Scheinfehler), bei Marcus
   „Prätor“ als „Präter“ (vielleicht falsch ausgesprochen). Auswerten mit `ArtifactData list duelle2`.
   Der mit Rubber Band abgesenkte Lupert (r2_09) klang laut Nutzer „ganz schlecht“; gemessen: CPPS 7,49 → 5,73, HNR
   10,3 → 8,9, Spektralhülle 2,2 dB vom Original entfernt. Aus dem Duell genommen (Duelle mit r2_09 beim Auswerten
   weglassen). Bessere Verfahren: Praat PSOLA („Change gender“, Formantfaktor 1,0) −3,3 HT: CPPS 6,90, Abstand 0,46 dB;
   WORLD-Vocoder (`pyworld`) −3,3 HT: CPPS 9,52 (Vocoder glättet), Abstand 0,52 dB; PSOLA −2,0 HT: CPPS 7,05, 0,40 dB.
   Hörproben an den Nutzer geschickt; die gewählte Fassung kommt als neuer Eintrag ins Duell.
   Nutzer (29.10.): auch PSOLA/WORLD klingen „etwas unsauber“ (Verarbeitungsartefakte). Neu gerechnet mit engerer
   Tonhöhenerkennung (80–220 Hz statt 60–300; im Original 11 Oktavfehler, 30 Rahmen unter 80 Hz). Wahrscheinliche
   Hauptursache: die knarrenden Phrasenenden werden mit abgesenkt und rutschen unter 70 Hz (PSOLA −3,3 HT: 41 Rahmen,
   −2 HT: 7). Nächster möglicher Schritt: nur die Mitte der Tonhöhe absenken, die Tiefen weniger (nichtlineare
   Abbildung über Praat-Manipulation). Die Hörseite spielt beim Umschalten jetzt von vorn; Schalter für „an derselben Stelle“.
   Nutzer: WORLD klingt „komprimiert, knisterig“. Neu gerechnet mit 1-ms-Raster, StoneMask, D4C-Schwelle 0,75,
   FFT 4096, MP3 160 kbit/s. Nutzer: klingt weiter komisch, **WORLD ist raus**. Die Hörseite markiert das gesprochene Wort.
   **Rauschunterdrückung** („wie Dolby“, als Schalter auf der Hörseite): `highpass=f=60,anlmdn=s=0.0007,agate=threshold=
   0.01:ratio=3:range=0.15:attack=5:release=200:knee=6:detection=rms,atrim=start_sample=353,apad=pad_len=353` (44,1 kHz).
   Grundrauschen −59 → −82 dBFS, leisestes Fünftel −52 → −65 dBFS, Sprache unverändert, kein Versatz. Vorsicht:
   `afftdn` verzögert um 25 ms, `anlmdn` um 8 ms (hier ausgeglichen); Messungen über eine fremde Pausenmaske sind dann
   falsch. PSOLA-Fassungen haben 2 dB mehr Grundrauschen als das Original (passt zum Höreindruck des Nutzers). In der
   Verarbeitung gehört die Rauschunterdrückung vor `pausen2.py`, damit der eingefügte Raumton zum entrauschten Ton passt.
   **Tempo:** Temporad 0,80–1,10 auf der Hörseite. Gemessen (Wörter je Minute über die ganze Dauer, Silben grob gezählt):
   Teil 1 öffentlich 134 W/min (3,7 Silben/s), Teil 2 141, eigene Lesung des Nutzers 138, Lupert roh bei 0,95 156 (ohne
   eingefügte Pausen), Runde-2-Stimmen bei 0,95 144–159. Richtwert Hörbuch englisch 150–160 W/min (ACX: 9.300 Wörter je
   Stunde ≈ 155, Sekundärquellen); deutsche Wörter haben etwa 1,64 Silben, englische etwa 1,45 (Schätzung), also
   entsprechen 155 englische etwa 135–140 deutschen W/min. Teil 1 und 2 liegen genau dort.
   **Pausen-Schalter** (Standard an): alle sechs Fassungen mit `pausen2.py` und dem Profil von Teil 1 bearbeitet
   (7 Stellen, +2,4 s, Rauschunterdrückung jeweils vorher). Mit Pausen bei Tempo 0,95: 140 W/min. Die Seite rechnet beim
   Umschalten über die Einfügestellen (`stellen.json`) auf dieselbe Textstelle um; das Mitlesen bleibt synchron.
   Ursprünglicher Plan: neuer Abschnitt Teil 2, Absatz 3 („Nun aber steht das Volk …“, 350 Zeichen,
   etwa 150 Credits je Stimme) mit Alexander, Leo Liest, Robert, Gottfried, Marcus, Marko, Helmut Stieglbauer und Lupert,
   dazu Lupert um 2,5 HT abgesenkt (formanterhaltend, `rubberband` ist in ffmpeg vorhanden, kostenlos) als Test der
   Tonlagen-These. Zusammen etwa 1.200 Credits. Tempo 0,95, zweite Duellrunde.
   Teil 3 erst erzeugen, wenn der Nutzer seine Textstellen überarbeitet hat und die Stimme feststeht.
2. Mit der gewählten Stimme Kapitel 1 neu erzeugen (bisher Teil 1 und 2, jetzt ein Stück), Kapitel 2 und 3 aufnehmen, alles
   neu verarbeiten. Vorher `werkzeuge/verarbeite.py` anpassen: keine PSOLA-Absenkung mehr (Helmut), Text ohne Marken an
   Stimme, Whisper und Pausen (`werkzeuge/stellen.py rein`), Stellen je Wort für das Video (`stellen.py liste`), Tempo 0,96
   direkt bei ElevenLabs.
   **Text von Teil 1 und 2 am 29.10. sprachlich nachgebessert** (vom Nutzer freigegeben, er liest noch einmal gegen):
   Teil 1 „wird gerade die Eile zur Ursache einer noch größeren Entfernung“ bleibt ausdrücklich so (Nutzer); Teil 2
   „Denn nichts verstrickt uns …“ statt „Und doch …“ (atqui ist hier kein Gegensatz) und „jeder ist auch Ursache und
   Urheber des Irrtums anderer“ statt „… auch fremden Irrtums“. „Am Beispiel der anderen gehen wir zugrunde“ bleibt
   ausdrücklich so (Nutzer). Danach, ebenfalls freigegeben: Teil 1 „… zwischen Irrwegen aufreiben. Dabei wäre es selbst
   dann kurz, wenn wir uns Tag und Nacht um einen klaren Verstand bemühten.“ (bona mens, nicht ratio) und Teil 2 „Geheilt
   werden wir, wenn wir uns nur von der Menge lösen.“ (sanabimur); dazu 1,1 „je hastiger er darauf zustrebt“ statt „ihm zustrebt“
   (ab ea … ad illam: davon … darauf). Damit ist Kapitel 1 laut Nutzer fertig. Die öffentlichen Aufnahmen haben noch den alten
   Wortlaut, bis zur Neuvertonung.
   **Titel (Nutzer: ja, aber nur an echten Wendepunkten, ohne Teilnummer):** fünf Abschnitte, am Latein geprüft, Tabelle
   in `PLAN.md` (Abschnitte und gesprochene Titel). Für Kapitel 1–3: gesprochen nur „Wohin und auf welchem Weg“ vor Kapitel 1
   und „Im Einklang mit der Natur“ vor Kapitel 3. Titel als eigener Clip, nicht in `texte/kapitelNN.txt`.
   **Idee des Nutzers:** Stellenangaben (Kapitel,Paragraf wie 1,4) sichtbar im Text, auf der Seite und später im Video,
   mit Sprungmöglichkeit; nicht gesprochen. **Endprodukt ist ein YouTube-Video** (Nutzer, 29.10.): also nichts zum
   Ein- und Ausblenden, die Darstellung muss vorher feststehen. Nutzer will Marken im Text **und** in der Ecke (siehe
   Probefilm); ursprünglicher Vorschlag war nur die Ecke („Kapitel 1,4“), Titelkarte an den fünf Abschnittsanfängen, YouTube-Kapitelmarken je
   lateinischem Kapitel in der Beschreibung (Regeln: erste Marke 0:00, mindestens drei, je mindestens 10 s).
   Unsichtbare Marken „[1,2]“ in `texte/kapitelNN.txt` liefern die Zeiten (eingetragen für Kapitel 1–3; `werkzeuge/stellen.py`).
   Im Video als „1 (2)“ in Textgröße und bronze im Text, dazu „Kapitel 1 (2)“ in der Kopfzeile. Kopfzeile: vier Varianten
   gezeigt (29.10.), Wahl offen; „Teil x von 29“ entfällt.
   **Abschnitte entfallen** (Nutzer, 29.10.): keine fünf Namen, keine Titelkarten, keine gesprochenen Abschnittstitel; nur
   die Startseite. **Kopfzeile gewählt (Variante 4, ganz in Bronze):** links „SENECA“ / „De vita beata“, rechts
   „KAPITEL 1 VON 28“ / „Paragraf 2“, beide Seiten gleich gebaut. Bronze heißt im Bild „wo bin ich“ (Kopfzeile, Marken),
   Weiß/Grau ist Senecas Text. Titelkarte aus `bild.html` entfernt; daten.json: `text_ab`, `start_ende` (nur Kapitel 1).
   **Schriftgrößen (Nutzer: im Hochformat am Handy unlesbar):** kleinste Schrift im Video jetzt 40 px (vorher 26). Startseite:
   Autor 46, Titel 150, deutscher Titel 80, Zusatz 44 px in zwei Zeilen; Kopfzeile 40/46 px. Ein 1920er-Bild erscheint im
   Hochformat mit etwa 0,2-facher Größe, 40 px also wie 8 pt.
   **Probefilm Teil 1 (29.10., nicht veröffentlicht):** Stieglbauer aus den vorhandenen Proben (Absatz 1–2 und 3–4, also
   noch alter Wortlaut beim „kurzen Leben“), gesprochener Titel (11 Credits), Tempo 0,96 per atempo, −18 LUFS, 1920 × 1080.
   Fassung 1 (ein Absatz je Bild, Wort im Kasten) gefiel dem Nutzer weniger; **gewünscht ist der Lesemodus der App:**
   fließender Text, gesprochene Zeile im Band in der Mitte, Wort färbt sich fließend ein, dazu Stellenmarken im Text
   wie im Buch, aber immer mit Kapitel („1 (1)“, „1 (2)“), und gleichzeitig „Kapitel 1 (2)“ in der Ecke. Fassung 2 so
   gebaut: `werkzeuge/video/baue.py <daten.json> <ton.wav> <aus.mp4>` (bild.html, render.js; 25 Bilder/s, vier Prozesse,
   1:55 Film in 2:47 min, also das ganze Werk in etwa 2 Stunden; 32 MB). Band: Stützstellen an den Zeilenanfängen bei
   (k − ½) Zeilen, gesprochene Zeile höchstens eine halbe Zeile neben der Mitte (Lesemodus der Seite: bis 0,65).
   Schriften vor der Zeilenberechnung laden (`bereit()`), sonst bricht der Text mit der Ersatzschrift anders um.
   **Probefilm 3 (Nutzer freigegeben):** Marken in Textgröße und Literata, bronze; Startseite als Titelblatt („Lucius
   Annaeus Seneca“ / „De vita beata“ / „Vom glücklichen Leben“ / „An seinen Bruder Gallio · aus dem Lateinischen neu
   übersetzt“), nur „Seneca. Vom glücklichen Leben.“ gesprochen (13 Credits); dann Titelkarte mit gesprochenem Titel, dann
   Text. In daten.json `start_ende` (nur Teil 1) und `titel_ende`. 1:59, Render 3:10 min.
3. Kapitel 3 (bisher Teil 4) freigeben lassen. Entscheidungen im Entwurf, die der Nutzer prüfen sollte:
   - Lücke und Crux in 3,4 sind geglättet wie bei Stewart und Forbiger (beide glätten): „an die Stelle der Lüste und
     all dessen, was klein und zerbrechlich ist und schon durch seine Schändlichkeit schadet, tritt …“.
   - Senatsbild in 3,2 beibehalten: „meine Stimme abgeben“, *sententiam dividere* als „dass über seinen Antrag Punkt
     für Punkt abgestimmt wird“, *hoc amplius censeo* als „Ich beantrage noch etwas dazu.“
   - *fortuna* als „Schicksal“, nicht „Glück“, damit „glücklich“ für *beatus* reserviert bleibt.
   - *voluptas* als „Lust“ (Plural „Lüste“) – Leitbegriff ab Kapitel 4, bitte früh festlegen; *gaudium* als „Freude“.
   - *solidum* als „fest und gediegen“ (Bild vom reinen Erz, passt zu *eruamus*, „ausgraben“).
4. Kapitel 4 übersetzen.

Im Container fehlen `faster-whisper` und `praat-parselmouth` (für `pruef.py`, `prosodie.py`, `karaoke_daten.py`);
pip ist erreichbar, vor den Messungen installieren.

## Verarbeitung einer Aufnahme (bewährt)

1. Worttreue: `werkzeuge/pruef.py large-v3-turbo <text> <mp3>`; bei Abweichungen mit `medium` und `large-v3`
   gegenprüfen. Bekannte Scheinfehler: „Walen“ statt „Wahlen“ (gleich klingend), „dem“ statt „den“ vor V (Angleichung).
2. Wortzeiten: `seite/karaoke_daten.py --einzeln <mp3> <text> <aus.json>`.
3. Pausen: `werkzeuge/pausen2.py <mp3> <wörter.json> <aus.mp3> '{".": 0.9, "absatz": 1.3, ":": 0.55, ";": 0.55,
   "–": 0.45, ",": 0.30, "komma_ab": 0.15}' <text>`. Kommas nur dort verlängern, wo die Stimme schon pausiert,
   sonst stockt es mitten im Satz.
4. Lautheit −18 LUFS, Limiter 0,72 (AAC) bzw. 0,84 (MP3); öffentlich AAC 64 kbit/s mono mit `+faststart`.
5. Wortzeiten der bearbeiteten Fassung für den Lesemodus in `seite/karaoke.json` (Schlüssel `a-teilNN`), Teil in
   `TEILE` in `seite/bau_hoerbuch.py` eintragen, `python3 seite/bau_hoerbuch.py seite/karaoke.json .` bauen.

## Nicht im Repo (privat)

- Rohaufnahmen aus ElevenLabs (Lupert Teil 1 und 2, Stimmproben): im ElevenLabs-Verlauf des Nutzers; die
  Vergleichsproben zusätzlich im Vorschau-Artifact unter `audio/v_*.mp3`.
- Die eigene Sprachaufnahme des Nutzers (Seneca-Memo): nur beim Nutzer.
- `seite/karaoke_daten.py` und `seite/bau.py` enthalten noch Pfade aus der alten Arbeitssitzung; vor Gebrauch anpassen.
