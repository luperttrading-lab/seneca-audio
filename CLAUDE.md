# Seneca-Hörbuch (De vita beata)

Eigene Übersetzung und Vertonung von Senecas *De vita beata*, eingeteilt nach Senecas 28 Kapiteln. Plan, Stilregeln und Ablauf je Kapitel:
`PLAN.md`. Stand, Links und offene Punkte: `UEBERGABE.md` (zu Beginn einer neuen Sitzung zuerst lesen).

## Regeln

- Das Repo ist öffentlich, GitHub Pages zeigt `index.html` (https://luperttrading-lab.github.io/seneca-audio/).
  Aufnahmen mit dem Stimmklon „Lupert“ oder eigene Aufnahmen des Nutzers nur nach ausdrücklicher Zustimmung committen.
- API-Schlüssel nie in Dateien, Commits oder Chat. Der ElevenLabs-Schlüssel kommt, wenn eingerichtet, als
  Umgebungsvariable `ELEVENLABS_API_KEY` aus den Einstellungen der Cloud-Umgebung.
- Jede Internetadresse als klickbarer Markdown-Link. Am Ende **jeder** Antwort, direkt über der Kostenzeile, ein kurzer
  Linkblock mit den aktuellen Seiten des Projekts: zuerst die Seite, an der gerade gearbeitet wird (fett), dann die
  übrigen gültigen Links aus `UEBERGABE.md` (öffentliche Hörbuch-Seite, private Vorschauen). Überholte Links weglassen.
- Kostenzeile am Ende jeder Antwort: `python3 tools/kosten.py` im Repo ausführen, Ausgabe wörtlich übernehmen.
- Seiten vor dem Veröffentlichen im Browser testen (Playwright, Handygröße 390 × 844). Playwright-Chromium spielt kein
  AAC: für Tests MP3-Kopien verwenden; `seite/rangeserver.py` liefert Bereichsanfragen wie GitHub Pages.
- Claude-Artifacts liefern keine `.m4a` aus: dort MP3 verwenden.
