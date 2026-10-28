# Übergabe – Stand 28.10.2026, nachmittags

## Links

- Öffentliche Hörbuch-Seite (Teil 1 und 2): https://luperttrading-lab.github.io/seneca-audio/
- Private Vorschau mit Stimmenvergleich (Claude-Artifact, Quelle mit `seite/bau_hoerbuch.py … --artifact --vergleich`):
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
Bibliotheksstimmen fügt der Nutzer in der App selbst zu seinen Stimmen hinzu. `api.elevenlabs.io` ist erreichbar.
Der erste Schlüssel hatte nur 30 Credits Kontingent (Fehlermeldung `quota_exceeded`). Am 28.10. hat der Nutzer einen
**neuen Schlüssel mit 30.000 Credits** erzeugt; er muss als `ELEVENLABS_API_KEY` in den Einstellungen der
Cloud-Umgebung stehen und gilt erst in einer neuen Sitzung. Zu Beginn prüfen, ohne ihn anzuzeigen: Eine Anfrage mit
Absatz 1–2 (785 Zeichen) braucht laut API 337 Credits; kommt wieder „quota of 30“, ist noch der alte Schlüssel
eingetragen. Der alte Schlüssel war am 28.10. noch gültig und sollte gelöscht werden. `/v1/user` und
`/v1/user/subscription` antworten mit 401.

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

## Offen, in dieser Reihenfolge

1. **Modellprüfung mit dem neuen Schlüssel**, angepasst an die Befunde (Empfehlung: 1.2 zuerst, dann 1.1):
   1. Ralf Benz, Absatz 1–2, je eine Anfrage: `eleven_v4` mit Stability 1,0; `eleven_multilingual_v2` mit Stability
      0,75, Style 0; `eleven_storytel_v2` (Hörbuchmodell, Zugang ungeprüft). Je etwa 340 Credits laut Fehlermeldung.
      `werkzeuge/erzeuge_varianten.py <text> <ordner>` (enthält auch 1.2); Text = Absatz 1–2 aus Teil 1, wie er im
      Verlauf steht (`GET /v1/history`, Feld `dialogue[0].text`). Messen: Wortzeiten mit
      `seite/karaoke_daten.py --einzeln`, dann `werkzeuge/messen_abstand.py <aus.json> <mp3 …>`.
   2. Lupert mit denselben Einstellungen wie 05:23 (Absatz 1–2 allein, Similarity Standard) noch einmal: klärt, ob
      10,5 HT reproduzierbar ist. Wenn ja, ist Lupert mit v4 der beste Kandidat für die Melodie, und die Pausen lassen
      sich mit `pausen2.py` verbessern (aber nur verlängern, wo Lupert schon pausiert).
   3. Bei Melodie unter etwa 12 HT: A/B-Vergleich mit dem Nutzer. Wegen der Take-Streuung nur Unterschiede über
      etwa 1 HT ernst nehmen, beim Abfall nur Mittel aus mehreren Takes.
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
