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
| `audio/` | Fassungen auf −18 LUFS: ElevenLabs Christian, Gemini-Montage, und die Hörbuch-Teile in Luperts Stimme (`teilNN.m4a`, auf Wunsch veröffentlicht). Weitere Lupert-Dateien nur nach Absprache, das Repo ist öffentlich |

## Startseite: das Hörbuch

`index.html` ist die öffentliche Seite unter https://luperttrading-lab.github.io/seneca-audio/: alle fertigen Teile mit
Liste, großem Play-Knopf, Lesemodus mit durchlaufendem Text und nahtlosem Weiterspielen; Tempo 0,95, immer dunkel.
Erzeugt mit `python3 seite/bau_hoerbuch.py seite/karaoke.json .` aus `seite/hoerbuch_vorlage.html`; neue Teile werden
in der Liste `TEILE` in `seite/bau_hoerbuch.py` eingetragen. Ton je Teil in `audio/teilNN.m4a` (AAC 64 kbit/s, −18 LUFS).
Seit 29.10. gilt nur noch Senecas Einteilung in 28 Kapitel (`GLIEDERUNG.md`); Texte in `texte/kapitelNN.txt`, Latein in
`texte/latein/kapitelNN.txt`. Die öffentliche Seite zeigt bis zur Neuvertonung von Kapitel 1 noch die alten Teile 1 und 2.

## Bauen

`bau.py` und `karaoke_daten.py` enthalten noch absolute Pfade aus der Arbeitssitzung (Arbeitsordner und das Repo
`fragen-allgemein` mit Text und Takes); vor dem nächsten Bauen auf Pfade in diesem Repo umstellen.
Der Text der Neufassung liegt in `fragen-allgemein/audio/seneca_neufassung_v2/text.txt`.
