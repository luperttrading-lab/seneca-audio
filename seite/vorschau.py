"""Vorschauseite je Kapitel: vorschau.py <kapitel> <ordner mit daten.json/mp3/mp4> <seitenordner> "<lead>" "<geprüft>"

Vorlage ist seite/vorschau_kapitel01.html. Das Video wird auf 720p verkleinert (zweipassig, etwa 13,5 MB, unter der
Grenze von 15 MB je Datei in Artifacts), dazu Tonspur und Standbild. Danach den Seitenordner als Artifact veröffentlichen.
"""
import json, os, subprocess, sys
HIER = os.path.dirname(os.path.abspath(__file__))
kap, ordner, aus, lead, geprueft = int(sys.argv[1]), sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5]
b = os.path.join(ordner, f"kapitel{kap:02d}"); D = json.load(open(b + ".daten.json", encoding="utf-8"))
os.makedirs(f"{aus}/video", exist_ok=True); os.makedirs(f"{aus}/audio", exist_ok=True)
mm = lambda s: f"{int(s // 60)}:{int(s % 60):02d}"
ab = []
for i, st in enumerate(D["stelle"]):
    if i == 0 or st != D["stelle"][i - 1]: ab.append(f"{st.split(',')[0]} ({st.split(',')[1]}) ab {mm(D['t'][i])}")
# 720p, zweipassig auf etwa 13,5 MB
dauer = D["ende"]; v = int(13.5e6 * 8 / dauer / 1000) - 140
ziel = f"{aus}/video/kapitel{kap:02d}.mp4"
for pas in (1, 2):
    subprocess.run(["ffmpeg", "-nostdin", "-y", "-loglevel", "error", "-i", b + ".mp4", "-vf", "scale=1280:720", "-c:v", "libx264", "-preset", "slow",
                    "-b:v", f"{v}k", "-pass", str(pas), "-passlogfile", f"{aus}/pass", *(["-an", "-f", "null", "/dev/null"] if pas == 1 else
                    ["-c:a", "aac", "-b:a", "128k", "-movflags", "+faststart", ziel])], check=True, cwd=aus)
for f in os.listdir(aus):
    if f.startswith("pass"): os.remove(os.path.join(aus, f))
subprocess.run(["cp", b + ".mp3", f"{aus}/audio/kapitel{kap:02d}.mp3"], check=True)
subprocess.run(["ffmpeg", "-nostdin", "-y", "-loglevel", "error", "-ss", str(min(D["t"][0] + 3, dauer / 3)), "-i", b + ".mp4", "-frames:v", "1", "-vf", "scale=1280:-1", "-q:v", "4", f"{aus}/poster.jpg"], check=True)
mb = os.path.getsize(ziel) / 1e6
s = open(os.path.join(HIER, "vorschau_kapitel01.html"), encoding="utf-8").read()
alt_lead = s[s.index('<p class="lead">') + 16:s.index("</p>", s.index('<p class="lead">'))]
s = (s.replace("Kapitel 1 · Vorschau", f"Kapitel {kap} · Vorschau").replace("<h1>Kapitel 1</h1>", f"<h1>Kapitel {kap}</h1>")
     .replace(alt_lead, lead).replace("video/kapitel01.mp4", f"video/kapitel{kap:02d}.mp4").replace("audio/kapitel01.mp3", f"audio/kapitel{kap:02d}.mp3")
     .replace("Kapitel 1 von De vita beata", f"Kapitel {kap} von De vita beata"))
i = s.index("<dt>Dauer</dt>"); j = s.index("</dl>")
s = s[:i] + (f"<dt>Dauer</dt><dd>{mm(dauer)}</dd>\n    <dt>Paragrafen</dt><dd>{' · '.join(ab)}</dd>\n"
             f"    <dt>Stimme</dt><dd>Helmut Stieglbauer, eleven v4, Tempo 0,96, −18 LUFS</dd>\n    <dt>Geprüft</dt><dd>{geprueft}</dd>\n  ") + s[j:]
i = s.index('<p class="hinweis">'); j = s.index("</p>", i) + 4
s = s[:i] + f'<p class="hinweis">Für die Vorschau auf 720p verkleinert ({mb:.1f} MB). Das fertige Video für YouTube hat Full HD.</p>'.replace(".", ",", 1) + s[j:]
open(f"{aus}/index.html", "w", encoding="utf-8").write(s)
print(ziel, f"{mb:.1f} MB", ab)
