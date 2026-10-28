"""Misst MP3s wie werkzeuge/prosodie.py und berechnet den Abstand wie seite/bau.py (6 Werte, Zielbereich 2. bis 6. Wert der 7 Vorleser)."""
import sys, json, os, subprocess, numpy as np
R = "/home/user/seneca-audio"
src = open(f"{R}/werkzeuge/prosodie.py").read().split("W = sys.argv[1]")[0]
exec(src)
M0 = json.load(open(f"{R}/messung/merkmale.json"))
refs = sorted(k for k in M0 if k.startswith("ref_"))
F = ["Tempo W/s", "Pausenanteil %", "Wörter/Phrase", "Pausen-Schwankung", "Melodie-Spannweite HT", "Abfall HT/s"]
lo = {f: sorted(M0[r][f] for r in refs)[1] for f in F}; hi = {f: sorted(M0[r][f] for r in refs)[-2] for f in F}
lo["Tempo W/s"], hi["Tempo W/s"] = 2.6, 3.0
def abstand(m):
    d = 0.0
    for f in F:
        a, b = lo[f], hi[f]; w = b - a; x = m[f]; eps = 0.01 * w
        if x < a - eps: d += (a - x) / w
        elif x > b + eps: d += (x - b) / w
    return d
out = json.load(open(sys.argv[1])) if os.path.exists(sys.argv[1]) else {}
for mp3 in sys.argv[2:]:
    base = mp3[:-4]; wav = base + ".wav"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", mp3, "-ac", "1", "-ar", "16000", wav], check=True)
    m = merkmale(wav); m["Abstand"] = abstand(m); m["Dauer"] = len(lade(wav)) / 16000
    out[os.path.basename(base)] = m
    print(f"{os.path.basename(base):24}" + " ".join(f"{k.split()[0][:8]}={m[k]:.2f}" for k in F + ["Abstand"]), flush=True)
json.dump(out, open(sys.argv[1], "w"), ensure_ascii=False, indent=1)
