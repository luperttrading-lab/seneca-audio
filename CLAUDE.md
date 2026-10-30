# Seneca-Hörbuch (De vita beata)

Eigene Übersetzung und Vertonung von Senecas *De vita beata*, eingeteilt nach Senecas 28 Kapiteln.

- `UEBERGABE.md`: Stand, nächste Schritte, aktuelle Links – zu Beginn jeder Sitzung zuerst lesen.
- `PLAN.md`: die gültigen Regeln – Stil, Begriffsliste, Festlegungen des Nutzers, Ablauf je Kapitel, Prüfliste Ton.
  Vor jeder Arbeit an einer Übersetzung oder Aufnahme lesen und danach arbeiten.
- `PROTOKOLL.md`: Verlauf, Versuche und Messungen (Belege, teils überholt); neue Befunde dort anhängen, nicht in die
  Übergabe. Ändert ein Befund eine Regel, die Regel in `PLAN.md` anpassen.

## Regeln

- Das Repo ist öffentlich, GitHub Pages zeigt `index.html` (https://luperttrading-lab.github.io/seneca-audio/).
  Aufnahmen mit dem Stimmklon „Lupert“ oder eigene Aufnahmen des Nutzers nur nach ausdrücklicher Zustimmung committen.
- API-Schlüssel nie in Dateien, Commits oder Chat. Der ElevenLabs-Schlüssel kommt, wenn eingerichtet, als
  Umgebungsvariable `ELEVENLABS_API_KEY` aus den Einstellungen der Cloud-Umgebung.
- Wird ein Kapiteltext vorgelegt (Entwurf, Überarbeitung, Freigabe), steht der ganze Text zum Kopieren als Codeblock
  **am Schluss** der Antwort, nach den Erläuterungen; danach nur noch Link und Kostenzeile (Nutzer, 30.10.).
- Jede Internetadresse als klickbarer Markdown-Link. Am Ende **jeder** Antwort, direkt über der Kostenzeile, **nur der
  Link der Seite, an der gerade gearbeitet wird** (fett); die übrigen Links nicht mehr aufzählen (Nutzer, 29.10.).
- **Hörproben und Videos nie als Datei zum Herunterladen schicken**, sondern als Seite zum direkten Anhören bzw.
  Ansehen (Artifact mit Abspielknopf und mitlaufendem Text, MP3; je Datei höchstens 15 MB, Videos dafür verkleinern).
  Der Nutzer hört am Handy und will nicht erst herunterladen und mit einem anderen Programm öffnen.
  Ausnahme: die fertige Full-HD-Datei für den YouTube-Upload als Datei schicken (Nutzer, 30.10.).
- Der Container wird gelöscht: abgenommene Aufnahmen sofort sichern (privates Vorschau-Artifact, Ordner `quelle/`;
  `PLAN.md`, Prüfliste Ton, Punkt 6). ElevenLabs: höchstens 5 Anfragen gleichzeitig; verbrauchte Credits in `UEBERGABE.md`
  nachtragen.
- Kostenzeile am Ende jeder Antwort: `python3 tools/kosten.py` im Repo ausführen, Ausgabe wörtlich übernehmen.
- Seiten vor dem Veröffentlichen im Browser testen (Playwright, Handygröße 390 × 844). Playwright-Chromium spielt kein
  AAC: für Tests MP3-Kopien verwenden; `seite/rangeserver.py` liefert Bereichsanfragen wie GitHub Pages.
- Claude-Artifacts liefern keine `.m4a` aus: dort MP3 verwenden.
