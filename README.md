# Seneca, Vom glücklichen Leben – neue Übersetzung als Hörbuch

Eigene Übersetzung von Senecas *De vita beata* aus dem Lateinischen, vertont als Hörbuch und als YouTube-Video mit
mitlaufendem Text. Eingeteilt wird nur nach Senecas 28 Kapiteln und ihren Paragrafen; im Video stehen die Stellen als
„1 (2)“ im Text und in der Kopfzeile. Sprecher ist die KI-Stimme Helmut Stieglbauer (ElevenLabs, eleven v4).

Stand: Kapitel 1 ist übersetzt, vertont und als Video fertig; Kapitel 2 und 3 sind übersetzt, aber noch nicht
freigegeben. Die öffentliche Seite https://luperttrading-lab.github.io/seneca-audio/ zeigt noch die erste Fassung von
Kapitel 1 in zwei Teilen mit einer anderen Stimme und älterem Wortlaut.

## Inhalt

| Ordner | Was |
|---|---|
| `texte/` | Übersetzung je Kapitel (`kapitelNN.txt`, mit Stellenmarken „[1,2]“, die nicht gesprochen werden), Latein in `latein/kapitelNN.txt` ([The Latin Library](https://www.thelatinlibrary.com/sen/sen.vita.shtml)) |
| `werkzeuge/` | `kapitel.py` macht aus einem Kapiteltext Ton und Video: Stimme, Prüfung der Worttreue mit Whisper, Rauschunterdrückung, Wortzeiten, Pausen, Tempo, Lautheit (Bausteine in `kette.py`); `paragraf.py` spricht einzelne Paragrafen neu; `stellen.py` behandelt die Stellenmarken; `pausen2.py` verlängert Pausen an Satzzeichen mit nachgebildetem Raumton; `prosodie.py` und `fingerabdruck.py` messen Satzmelodie und Stimme |
| `werkzeuge/video/` | `bild.html` (ein Videobild: Startseite, fließender Text mit Band in der Mitte, Wortfärbung, Kopfzeile), `render.js` und `baue.py` rendern Bild für Bild und setzen das Video zusammen (1920 × 1080, 25 Bilder/s); `miniatur.html`/`.js` für das YouTube-Miniaturbild |
| `seite/` | die öffentliche Hörbuch-Seite (`hoerbuch_vorlage.html`, `bau_hoerbuch.py`), Vorlagen für Prüf- und Vergleichsseiten, Playwright-Tests, Testserver mit Bereichsanfragen |
| `audio/` | veröffentlichte Tonfassungen der ersten Arbeitsphase |
| `messung/` | Messwerte aus Stimmenwahl und Versuchen (Prosodie, Wortzeiten, Pausenstellen, Stimmvergleiche) |

## Regeln und Stand

- `PLAN.md`: Stil der Übersetzung, Begriffsliste, Ablauf je Kapitel, Prüfliste für den Ton, Kapiteltabelle.
- `UEBERGABE.md`: aktueller Stand und nächste Schritte.
- `PROTOKOLL.md`: Verlauf mit Versuchen und Messungen.
- `GLIEDERUNG.md`: die 28 Kapitel mit Paragrafen und geschätzter Hördauer (gesamt etwa 81 Minuten).

## Ein Kapitel bauen

```
python3 werkzeuge/kapitel.py 1 <ordner>            # Ton und Video; braucht ELEVENLABS_API_KEY
python3 werkzeuge/kapitel.py 1 <ordner> --ohne-video
python3 werkzeuge/video/baue.py <daten.json> <ton.wav> <video.mp4>
```

Voraussetzungen: ffmpeg, Python mit `numpy`, `faster-whisper` und `praat-parselmouth`, Node mit Playwright. Die
Rohaufnahme wird im Ausgabeordner zwischengespeichert; liegt sie dort schon, kostet ein neuer Lauf keine Credits.
`seite/karaoke_daten.py` und `seite/bau.py` enthalten noch Pfade aus der ersten Arbeitsphase.
