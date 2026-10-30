# Übergabe – Stand 30.10.2026

Zu Beginn jeder Sitzung lesen. Hier stehen nur Stand und nächste Schritte; die Regeln (Stil, Begriffe, Ablauf, Prüfliste
Ton) stehen in `PLAN.md`, Verlauf, Versuche und Messungen in `PROTOKOLL.md`.

## Stand je Kapitel

| Kapitel | Text | Ton und Video |
|---|---|---|
| 1 | fertig, freigegeben (`texte/kapitel01.txt`, Marken 1,1–1,5) | **fertig (Fassung v3):** Helmut, wortgetreu (499/499), 38 Pausen, 3:53; erster Satz von 1 (3) einzeln erzeugt eingesetzt („die vor uns hergeht“). Full-HD-Datei am 30.10. dem Auftraggeber für YouTube geschickt, dazu Miniaturbilder mit und ohne „Kapitel 1“. Gesichert (siehe unten) |
| 2 | fertig, freigegeben (30.10.; nach den Regeln in `PLAN.md` überarbeitet, 2,1 „offenbar die Mehrheit“) | **Ton erzeugt (30.10.)**, 989 Credits; Betonungsfilter: 0 markiert. „Bekränzten“ und „Beredsamkeit“ vom Auftraggeber als richtig gehört (`texte/verhoerer.txt`); 2,3 „dem Geschossen“ war ein echter Sprechfehler: Satz mit `satz.py` dreimal allein erzeugt (159 Credits), Fassung 3 eingesetzt, jetzt wortgetreu, 40 Pausen, 2:52. **Auftraggeber hört die neue Fassung**; gesichert im Hörprobe-Artifact unter `quelle/`. Video erst nach Abnahme |
| 3 | Entwurf (`texte/kapitel03.txt`), mit Stewart und Forbiger abgeglichen; **Freigabe offen** (Entscheidungen unten) | – |
| 4–28 | Latein in `texte/latein/kapitelNN.txt` | – |

Die öffentliche Seite zeigt noch Luperts alte „Teile 1 und 2“ mit altem Wortlaut; umgestellt wird nur mit Freigabe.

## Nächste Schritte

1. **Auftraggeber:** Hörprobe Kapitel 2 anhören (Paragraf 2 (3) mit dem neuen Satz); Kapitel 3 freigeben.
2. **Auftraggeber:** YouTube – einzelne Videos je Kapitel (Playlist) oder ein Gesamtvideo? Bis dahin Kapitel 1 am besten
   „Nicht gelistet“ hochladen und die Lesbarkeit am Handy prüfen.
3. **Auftraggeber:** Credit-Grenze des Schlüssels anheben (reicht noch für etwa 12 bis 14 Kapitel).
4. **Auftraggeber:** Leseband wählen (Seite „Lesebänder im Vergleich“); danach den Stil als Standard in `bild.html`
   setzen und Kapitel 1 neu rendern (ohne Credits).
5. **Claude:** nach Abnahme von Kapitel 2 das Video bauen (Prüfliste Ton, Punkt 5) und die Full-HD-Datei schicken.
5. Kapitel 4 übersetzen.
6. Später: öffentliche Seite auf Kapitel mit Helmut umstellen (Freigabe); Weg der Gesamtdatei zu YouTube klären (etwa
   1,3 GB in Full HD, zu groß für Artifacts; etwa über einen Ordner auf dem Rechner des Auftraggebers oder Google Drive).
   Kostenlos, aber offen: Helmut in der App unter „Meine Stimmen“ aufnehmen.

## Kapitel 3: Entscheidungen zur Freigabe

- Lücke und Crux in 3,4 sind geglättet wie bei Stewart und Forbiger (beide glätten): „an die Stelle der Lüste und all
  dessen, was klein und zerbrechlich ist und schon durch seine Schändlichkeit schadet, tritt …“.
- Senatsbild in 3,2 beibehalten: „meine Stimme abgeben“, *sententiam dividere* als „dass über seinen Antrag Punkt für
  Punkt abgestimmt wird“, *hoc amplius censeo* als „Ich beantrage noch etwas dazu.“
- *solidum* als „fest und gediegen“ (Bild vom reinen Erz, passt zu *eruamus*, „ausgraben“).
- *fortuna* „Schicksal“, *voluptas* „Lust“, *gaudium* „Freude“: inzwischen in der Begriffsliste (`PLAN.md`).

## Sicherung

Kapitel 1, Fassung v3: im privaten Artifact „Kapitel 1 · Vorschau“ unter `quelle/` (Rohaufnahme mit eingesetztem Satz,
Startsatz, Pausenfassung, Wortzeiten, Pausenstellen, `daten.json`, Text). Wiederherstellen: die Dateien mit dem
Artifact-Werkzeug (`read` mit `path`) in einen Ordner holen, dann `python3 werkzeuge/kapitel.py 1 <ordner>` – baut Ton und
Video ohne Credits neu. Jedes weitere Kapitel nach der Abnahme genauso sichern.

## YouTube

- Datei: H.264 1920 × 1080, 25 Bilder/s; Ton AAC-LC Stereo 48 kHz (`werkzeuge/video/baue.py`, seit 30.10.).
- „Verwendung von KI“: **Ja.** Helmut ist laut API `category: professional`, ein Stimmklon eines echten Sprechers;
  YouTube nimmt nur das Klonen der eigenen Stimme aus. Das Label erscheint bei Ton ohne Musik in der erweiterten
  Beschreibung und schränkt Reichweite und Monetarisierung nicht ein
  ([YouTube-Hilfe](https://support.google.com/youtube/answer/14328491?hl=de)).
- Vorschlag Titel: „Seneca – Vom glücklichen Leben (De vita beata) · Kapitel 1 · Hörbuch mit Text“; Beschreibung: „Aus
  dem Lateinischen neu übersetzt. Stimme: Helmut Stieglbauer (ElevenLabs, KI-Stimme).“
- Miniaturbild: `node werkzeuge/video/miniatur.js <kapitel|-> <aus.png>` (1920 × 1080; „-“ ergibt nur „Hörbuch“).
- Beim Gesamtvideo Kapitelmarken in die Beschreibung (erste Marke 0:00, mindestens drei, je mindestens 10 s).

## ElevenLabs

- Schlüssel als Umgebungsvariable `ELEVENLABS_API_KEY` (Text zu Sprache, Stimmen lesen, Modelle, Verlauf lesen, Benutzer;
  Stimmen schreiben bewusst gesperrt). Kontingent nicht abfragbar (`/v1/user` antwortet 401).
- Grenze des Schlüssels 30.000 Credits; verbraucht etwa 14.530, übrig etwa 15.470 (Stand 30.10., nach Kapitel 2 und einem nachgebesserten Satz). Etwa 0,43 Credits je
  Zeichen, ein Kapitel etwa 1.100–1.300. Das ganze Werk braucht etwa 28.800, die Grenze muss also steigen.
- Kosten laut Auftraggeber: 1.000 Credits ≈ 0,10 € im Sparabo, sonst 0,20 €.
- Höchstens 5 Anfragen gleichzeitig, sonst Fehler 429.

## Links (aktuell)

- Öffentliche Hörbuch-Seite: https://luperttrading-lab.github.io/seneca-audio/
- Kapitel 1 · Vorschau (privat; Video 720p, Ton, `quelle/`; Quelle `seite/vorschau_kapitel01.html`):
  https://claude.ai/artifact/Pa3cLB5TEbA2WvmnNQiVy9
- Kapitel 1 · Prüfstellen (privat; Betonungsversuche zu 1 (3); Quelle `seite/pruefstellen.html`):
  https://claude.ai/artifact/9oVZgpKioSQuSDG4DCfBJE
- **Lesebänder im Vergleich** (privat; Runde 2: vier Probevideos aus Kapitel 1, 4,4–34,4 s, alle kräftig: A fließend,
  C ruhend 0,9 s, C2 ruhend 1,6 s, C3 gemischt; Quelle `seite/bandvergleich.html`, Videos nur im Artifact): https://claude.ai/artifact/4MbuGh3bSWx4GvcRBhhAcp
- **Kapitel 2 · Hörprobe** (privat; ganzes Kapitel, Paragrafen, von Whisper gemeldete Wörter; `quelle/` mit Rohaufnahme;
  Quelle `seite/hoerprobe_kapitel02.html`, gebaut mit `seite/hoerprobe.py`): https://claude.ai/artifact/P2UJeKRMty5sWxpKoMvZ2h
- Kapitel 1 · Betonungsfilter (privat; Test des Filters, sechs markierte Stellen zum Anhören; Quelle
  `seite/betonungstest.html`, Ausschnitte nur im Artifact): https://claude.ai/artifact/FKbKXf7ynMhVhg5xydrTpQ
- Stimmenprobe (privat; Quelle `seite/stimmenprobe.html`): https://claude.ai/artifact/G9tMfCirpybCFyQYne2d6L
- Ältere Seiten (Duelle, Modellvergleich, Lupert tiefer): `PROTOKOLL.md`.

## Technik

- Im neuen Container fehlen meist `faster-whisper`, `praat-parselmouth` und `pyspellchecker` (für `textpruef.py`) (für `pruef.py`, `prosodie.py`,
  `karaoke_daten.py`); pip ist erreichbar. Fingerabdruck: Modellpfad in `WESPEAKER_ONNX`.
- Stolpersteine: Schriften vor der Zeilenberechnung laden (`bereit()` in `bild.html`), sonst bricht der Text anders um;
  Testseiten brauchen `<meta charset="utf-8">`, sonst kaputte Umlaute; `anlmdn` verzögert um 8 ms (in `kette.py`
  ausgeglichen), `afftdn` um 25 ms; Playwright-Chromium spielt kein AAC; `pkill -f <muster>` trifft den eigenen Befehl
  mit (Abbruch 144), Testserver stattdessen auf neuem Port starten.
- `seite/karaoke_daten.py` und `seite/bau.py` enthalten noch Pfade aus der alten Arbeitssitzung.

## Nicht im Repo (privat)

- Rohaufnahmen aus ElevenLabs (Lupert Teil 1 und 2, Stimmproben): im ElevenLabs-Verlauf des Auftraggebers; die
  Vergleichsproben zusätzlich im Modellvergleichs-Artifact unter `audio/v_*.mp3`.
- Die eigene Sprachaufnahme des Auftraggebers (Seneca-Memo): nur beim Auftraggeber.
