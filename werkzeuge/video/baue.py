"""Video eines Teils bauen: baue.py <daten.json> <ton.wav> <ausgabe.mp4> [fps] [--von s --bis s]

daten.json: {"w": Wörter, "t": Startzeiten im fertigen Ton (s), "p": Absatz je Wort, "stelle": lat. Stelle je Wort ("1,2",
aus werkzeuge/stellen.py liste), "text_ab": Text blendet ein, "start_ende": nur Kapitel 1, Startseite bis hier, "ende": Dauer}.
Rendert jedes Bild mit bild.html (vier Prozesse parallel) und setzt es mit dem Ton zu H.264/AAC zusammen.
--von/--bis: nur ein Ausschnitt, etwa für Probevideos (Bild und Ton ab --von).
"""
import os, subprocess, sys, tempfile

args = sys.argv[1:]; ab = []
if "--von" in args: i = args.index("--von"); ab = [args[i + 1], args[args.index("--bis") + 1]]; del args[i:i + 2]; j = args.index("--bis"); del args[j:j + 2]
daten, ton, aus = args[:3]; fps = args[3] if len(args) > 3 else "25"; n = 4
hier = os.path.dirname(os.path.abspath(__file__))
with tempfile.TemporaryDirectory(dir=os.path.dirname(os.path.abspath(aus))) as bilder:
    prozesse = [subprocess.Popen(["node", os.path.join(hier, "render.js"), daten, bilder, fps, str(k), str(n), *ab]) for k in range(n)]
    if any(p.wait() for p in prozesse): sys.exit("Rendern fehlgeschlagen")
    subprocess.run(["ffmpeg", "-nostdin", "-y", "-loglevel", "error", "-framerate", fps, "-i", os.path.join(bilder, "%06d.jpg"),
                    *(["-ss", ab[0], "-t", str(float(ab[1]) - float(ab[0]))] if ab else []), "-i", ton,
                    "-map", "0:v", "-map", "1:a", "-c:v", "libx264", "-preset", "slow", "-crf", "20", "-pix_fmt", "yuv420p",
                    "-af", "aresample=48000:resampler=soxr", "-ac", "2", "-c:a", "aac", "-b:a", "384k",   # YouTube-Empfehlung: AAC-LC, Stereo, 48 kHz
                    "-movflags", "+faststart", "-shortest", aus], check=True)
print("fertig:", aus)
