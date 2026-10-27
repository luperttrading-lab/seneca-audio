# Seneca, Vom glücklichen Leben – Hörfassungen

Hörseite zu Seneca, *De vita beata* 1,1–1,2 in einer Neufassung der Übersetzung: mehrere Sprechfassungen,
Tempo-Drehrad (0,50–1,50), Lesemodus mit fließend durchlaufendem Text und Natürlichkeitsmessung gegen sieben
LibriVox-Vorleser.

## Inhalt

| Ordner | Was |
|---|---|
| `seite/` | `vorlage.html` (Layout, Drehrad, Lesemodus), `bau.py` erzeugt daraus `index.html`; `karaoke_daten.py` legt Whisper-Wortzeiten auf den Text (`karaoke.json`); Playwright-Tests und ein Testserver mit Range-Unterstützung |
| `werkzeuge/` | `pausen2.py` verlängert Pausen an Satzzeichen mit nachgebildetem Raumton (ohne Schleife, kein Knattern); `prosodie.py` misst Tempo, Pausen, Melodie; `pruef.py` prüft Worttreue mit Whisper; `knatter_pruef.py` misst eingefügte Pausen |
| `messung/` | `merkmale.json` (Prosodie aller Fassungen und Referenzen), Wortzeiten, Einfügestellen der Pausen |
| `audio/` | Fassungen auf −18 LUFS: ElevenLabs Christian, Gemini-Montage, und als einzige Lupert-Fassung (Stimmklon) `lupert_ruhig.m4a` für die Startseite. Weitere Lupert-Dateien nur nach Absprache, das Repo ist öffentlich |

## Startseite zum Teilen

`index.html` ist die Seite für Empfänger: eine Fassung („Lupert, ruhig“, Tempo 0,95), großer Play-Knopf, Lesemodus mit
durchlaufendem Text. Erzeugt mit `python3 seite/bau_teilen.py` aus `seite/teilen_vorlage.html` und `seite/karaoke.json`.
Datenmenge beim Öffnen: etwa 0,9 MB (Seite 32 kB, Ton 0,84 MB als AAC 64 kbit/s).

## Bauen

`bau.py` und `karaoke_daten.py` enthalten noch absolute Pfade aus der Arbeitssitzung (Arbeitsordner und das Repo
`fragen-allgemein` mit Text und Takes); vor dem nächsten Bauen auf Pfade in diesem Repo umstellen.
Der Text der Neufassung liegt in `fragen-allgemein/audio/seneca_neufassung_v2/text.txt`.
