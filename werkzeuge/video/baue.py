"""Video eines Teils bauen: baue.py <daten.json> <ton.wav> <ausgabe.mp4> [fps]

daten.json: {"w": Wörter, "t": Startzeiten im fertigen Ton (s), "p": Absatz je Wort, "stelle": lat. Stelle je Wort ("1,2",
aus werkzeuge/stellen.py liste), "text_ab": Text blendet ein, "start_ende": nur Kapitel 1, Startseite bis hier, "ende": Dauer}.
Rendert jedes Bild mit bild.html (vier Prozesse parallel) und setzt es mit dem Ton zu H.264/AAC zusammen.
"""
import os, subprocess, sys, tempfile

daten, ton, aus = sys.argv[1:4]; fps = sys.argv[4] if len(sys.argv) > 4 else "25"; n = 4
hier = os.path.dirname(os.path.abspath(__file__))
with tempfile.TemporaryDirectory(dir=os.path.dirname(os.path.abspath(aus))) as bilder:
    prozesse = [subprocess.Popen(["node", os.path.join(hier, "render.js"), daten, bilder, fps, str(k), str(n)]) for k in range(n)]
    if any(p.wait() for p in prozesse): sys.exit("Rendern fehlgeschlagen")
    subprocess.run(["ffmpeg", "-nostdin", "-y", "-loglevel", "error", "-framerate", fps, "-i", os.path.join(bilder, "%06d.jpg"), "-i", ton,
                    "-map", "0:v", "-map", "1:a", "-c:v", "libx264", "-preset", "slow", "-crf", "20", "-pix_fmt", "yuv420p",
                    "-af", "aresample=48000:resampler=soxr", "-ac", "2", "-c:a", "aac", "-b:a", "384k",   # YouTube-Empfehlung: AAC-LC, Stereo, 48 kHz
                    "-movflags", "+faststart", "-shortest", aus], check=True)
print("fertig:", aus)
