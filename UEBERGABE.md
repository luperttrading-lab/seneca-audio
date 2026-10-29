# Übergabe – Stand 28.10.2026, abends

## Links

- Öffentliche Hörbuch-Seite (Teil 1 und 2): https://luperttrading-lab.github.io/seneca-audio/
- **Private Vorschau mit Modellvergleich vom 28.10.** (Teil 1 und 2 plus 7 Proben Ralf/Lupert; Quelle:
  `seite/bau_hoerbuch.py seite/karaoke.json <ordner> --artifact --vergleich messung/stimmen/vergleich_modelle.json`):
  https://claude.ai/artifact/Mj5fSGP6WhXq3iSCjZCqxt
- **Stimmen-Duell** (privat, Speicher `duelle` mit `{a, b, w: "a"|"b"|"=", t}`; Quelle `seite/duell.html`, Stimmen in
  `messung/stimmen/duell_stimmen.json`, Ton nur im Artifact): https://claude.ai/artifact/SMVhWQ4Qcto92tmNYbE6fM
- **Lupert tiefer** (privat, vier Fassungen umschaltbar an derselben Stelle; Quelle `seite/lupert_tiefer.html`):
  https://claude.ai/artifact/4Bx1FXUbjvxuH9n4UDmaWE
- Ältere private Vorschau mit dem Stimmenvergleich vom 27.10. (Lupert, Christian, Brian, Ralf, Robert, alle v4):
  https://claude.ai/artifact/Mi3DHEtyiHRPXEYfwj5XA9
- Ältere private Vergleichsseite zu Teil 1 (Lupert, Christian, Gemini): https://claude.ai/artifact/RfZhGX4jPHk6ZFfHaLhjVr

## Stand

| Teil | Text | Aufnahme |
|---|---|---|
| 1 (Kap. 1,1–2) | fertig | Lupert, Pausen „ruhig“, öffentlich (`audio/teil01.m4a`) |
| 2 (Kap. 1,3–5) | fertig, zweimal überarbeitet | Lupert, neue Kommaregel, öffentlich (`audio/teil02.m4a`) |
| 3 (Kap. 2) | fertig (`texte/teil03.txt`), mit Stewart und Forbiger abgeglichen | fehlt, wartet auf die Stimmenwahl |
| 4 (Kap. 3) | Entwurf (`texte/teil04.txt`), mit Stewart und Forbiger abgeglichen, Freigabe offen | – |
| 5–29 | Latein in `texte/latein/` | – |

## ElevenLabs-Schlüssel

Eingerichtet als Umgebungsvariable `ELEVENLABS_API_KEY` (eingeschränkt: Text zu Sprache, Stimmen lesen, Modelle,
Verlauf lesen, Benutzer; Abschalten bei Leak an). Stimmen schreiben ist bewusst gesperrt (könnte den Lupert-Klon löschen):
Bibliotheksstimmen lassen sich trotzdem direkt per API sprechen lassen (am 28.10. mit Otto geprüft), ohne sie hinzuzufügen. `api.elevenlabs.io` ist erreichbar.
`/v1/user` und `/v1/user/subscription` antworten mit 401, das Kontingent ist also nicht abfragbar.

Seit 28.10. ist der **neue Schlüssel (30.000 Credits Grenze)** aktiv. Eine API-Anfrage kostet laut Kopfzeile
`character-cost` 336–337 Credits für Absatz 1–2 (785 Zeichen), also etwa **0,43 Credits je Zeichen**, bei v4, v2 und
Storytel gleich. Die App hat für dieselben 785 Zeichen 766 Credits berechnet. Am 28.10. verbraucht: 7 Anfragen, 2.356
Credits; Rest also höchstens etwa 27.600. Dazu Stimmen-Duell 1.757 Credits (25 × 70 plus Test) und Runde 2 1.200 Credits, Stand abends
also etwa 5.300 verbraucht und höchstens etwa 24.700 übrig. **Das reicht nicht für das ganze Werk:** etwa 67.000 Zeichen (9,1 Zeichen je
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

## Offen, in dieser Reihenfolge

1. **Runde 2 läuft** (vom Nutzer freigegeben, 1.200 Credits; Speicher `duelle2`, Stimmen in
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
   Ursprünglicher Plan: neuer Abschnitt Teil 2, Absatz 3 („Nun aber steht das Volk …“, 350 Zeichen,
   etwa 150 Credits je Stimme) mit Alexander, Leo Liest, Robert, Gottfried, Marcus, Marko, Helmut Stieglbauer und Lupert,
   dazu Lupert um 2,5 HT abgesenkt (formanterhaltend, `rubberband` ist in ffmpeg vorhanden, kostenlos) als Test der
   Tonlagen-These. Zusammen etwa 1.200 Credits. Tempo 0,95, zweite Duellrunde.
   Teil 3 erst erzeugen, wenn der Nutzer seine Textstellen überarbeitet hat und die Stimme feststeht.
2. Mit der gewählten Stimme und dem gewählten Modell Teil 1 und 2 neu erzeugen, Teil 3 und 4 aufnehmen, alles neu
   verarbeiten.
3. Teil 4 freigeben lassen. Entscheidungen im Entwurf, die der Nutzer prüfen sollte:
   - Lücke und Crux in 3,4 sind geglättet wie bei Stewart und Forbiger (beide glätten): „an die Stelle der Lüste und
     all dessen, was klein und zerbrechlich ist und schon durch seine Schändlichkeit schadet, tritt …“.
   - Senatsbild in 3,2 beibehalten: „meine Stimme abgeben“, *sententiam dividere* als „dass über seinen Antrag Punkt
     für Punkt abgestimmt wird“, *hoc amplius censeo* als „Ich beantrage noch etwas dazu.“
   - *fortuna* als „Schicksal“, nicht „Glück“, damit „glücklich“ für *beatus* reserviert bleibt.
   - *voluptas* als „Lust“ (Plural „Lüste“) – Leitbegriff ab Kapitel 4, bitte früh festlegen; *gaudium* als „Freude“.
   - *solidum* als „fest und gediegen“ (Bild vom reinen Erz, passt zu *eruamus*, „ausgraben“).
4. Teil 5 (Kapitel 4) übersetzen.

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
