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

## ElevenLabs-Schlüssel

Eingerichtet als Umgebungsvariable `ELEVENLABS_API_KEY` (eingeschränkt: Text zu Sprache, Stimmen lesen, Modelle,
Verlauf lesen, Benutzer; Limit 30.000 Credits je Abrechnungszeitraum; Abschalten bei Leak an). Zu Beginn prüfen, ob er
ankommt, ohne ihn anzuzeigen. Stimmen schreiben ist bewusst gesperrt (könnte den Lupert-Klon löschen): Bibliotheksstimmen
fügt der Nutzer in der App selbst zu seinen Stimmen hinzu. `api.elevenlabs.io` ist aus der Cloud-Umgebung erreichbar.

## Offen, in dieser Reihenfolge

1. **Erst das Modell prüfen, dann die Stimme suchen.** Geht dem Abschnitt Stimmensuche in `PLAN.md` vor. Befund aus
   `messung/stimmen/vergleich_kap1_absatz12.json`: Alle fünf Stimmen (Lupert, Christian, Brian, Ralf Benz, Robert
   Ranger) weichen in dieselbe Richtung ab – Satzmelodie 13,0–16,0 Halbtöne statt 10,0–11,7, Schwankung der
   Pausenlängen 0,30–0,50 statt 0,62–0,89, Pausenanteil bei vier von fünf zu niedrig, Abfall am Phrasenende bei vier von
   fünf zu stark. Gemeinsam sind nur Modell (eleven v4) und Text. Verdacht: Das Modell erzeugt den Vorlese-Singsang,
   der den Nutzer stört; eine Bibliothekssuche mit demselben Modell fände nur weitere Stimmen mit demselben Fehler.
   Melodie und Abfall lassen sich nachträglich nicht korrigieren, Pausen schon (`pausen2.py`).
   1. Im Verlauf (History) nachsehen, mit welchem Modell und welchen Einstellungen die bisherigen Proben erzeugt wurden,
      auch die Stimme Gottfried vom 27.10. (taucht oben noch nicht auf; falls auch zu lebhaft, stützt das den Verdacht).
   2. Verfügbare Modelle abfragen (`GET /v1/models`), welche Deutsch können.
   3. Ralf Benz (bester Messwert, Abstand 1,30) mit Kapitel 1, Absatz 1–2 in 2–3 Varianten erzeugen (anderes Modell,
      höhere Stability; je etwa 800 Credits) und messen. Fällt die Melodie unter etwa 12 Halbtöne: A/B-Vergleich gegen
      die v4-Fassung.
   4. Erst wenn das nichts bringt: Bibliothekssuche wie in `PLAN.md` (A/B-Duelle, Bradley-Terry).
2. Mit der gewählten Stimme und dem gewählten Modell Teil 1 und 2 neu erzeugen, Teil 3 aufnehmen, alles neu verarbeiten.
3. Teil 4 (Kapitel 3) übersetzen, unabhängig von der Stimme, kann parallel laufen. In 3,4 hat der lateinische Text eine
   Lücke (`nam uoluptatibus et * * *`) und eine Crux (`~ipsis flagitiis noxia~`): mit dem Nutzer klären, ob die
   Hörfassung glättet (wie vermutlich Stewart) oder die Lücke hörbar macht.

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
