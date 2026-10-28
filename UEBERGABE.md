# Übergabe – Stand 28.10.2026

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
| 4–29 | Latein in `texte/latein/` | – |

## Offen, in dieser Reihenfolge

1. **Stimmensuche** (siehe `PLAN.md`, Abschnitt Stimmensuche): Der Nutzer ist mit Lupert, Christian, Brian, Ralf Benz
   und Robert Ranger nicht zufrieden, kann aber nicht benennen warum. Nur Männerstimmen. Vorgehen: ElevenLabs-Bibliothek
   per API durchsuchen, Hörproben messen, Vorliebe per A/B-Duell (Bradley-Terry) ermitteln. Zusätzlich vorgeschlagen:
   Ralf Benz mit anderem Modell bzw. höherer Stability testen, ob es am Modell eleven v4 liegt.
2. Mit der gewählten Stimme Teil 1 und 2 neu erzeugen, Teil 3 aufnehmen, alles neu verarbeiten.
3. Teil 4 (Kapitel 3) übersetzen.

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
