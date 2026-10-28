# Seneca-Hörbuch (De vita beata)

Eigene Übersetzung und Vertonung von Senecas *De vita beata* in 29 Teilen. Plan, Stilregeln und Ablauf je Teil:
`PLAN.md`. Stand, Links und offene Punkte: `UEBERGABE.md` (zu Beginn einer neuen Sitzung zuerst lesen).

## Regeln

- Das Repo ist öffentlich, GitHub Pages zeigt `index.html` (https://luperttrading-lab.github.io/seneca-audio/).
  Aufnahmen mit dem Stimmklon „Lupert“ oder eigene Aufnahmen des Nutzers nur nach ausdrücklicher Zustimmung committen.
- API-Schlüssel nie in Dateien, Commits oder Chat. Der ElevenLabs-Schlüssel kommt, wenn eingerichtet, als
  Umgebungsvariable `ELEVENLABS_API_KEY` aus den Einstellungen der Cloud-Umgebung.
- Jede Internetadresse als klickbarer Markdown-Link. Wurde eine Seite oder ein Artifact veröffentlicht oder
  aktualisiert: den Link als letzte Zeile vor der Kostenzeile wiederholen (`**Link:** [Name](URL)`).
- Kostenzeile am Ende jeder Antwort: `python3 tools/kosten.py` im Repo ausführen, Ausgabe wörtlich übernehmen.
- Seiten vor dem Veröffentlichen im Browser testen (Playwright, Handygröße 390 × 844). Playwright-Chromium spielt kein
  AAC: für Tests MP3-Kopien verwenden; `seite/rangeserver.py` liefert Bereichsanfragen wie GitHub Pages.
- Claude-Artifacts liefern keine `.m4a` aus: dort MP3 verwenden.
