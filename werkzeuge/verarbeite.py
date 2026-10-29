"""Rohaufnahme von ElevenLabs zur Hörbuchfassung verarbeiten (vom Nutzer am 29.10. gewählt: Lupert v4, tiefer, entrauscht).
Aufruf: verarbeite.py <roh.mp3> <text.txt> <ausordner> <name>
Schritte: Tonlage per PSOLA auf Median 100 Hz (Klangfarbe bleibt), Rauschunterdrückung, Wortzeiten (Whisper), Pausen
mit pausen2.py, Lautheit −18 LUFS. Ergebnis im Ausordner: <name>.mp3 (Artifact, Limiter 0,84), <name>.m4a (öffentlich,
AAC 64 kbit/s mono, Limiter 0,72), <name>.karaoke.json (Wortzeiten der fertigen Fassung für seite/karaoke.json)."""
import json, os, re, subprocess, sys, numpy as np, parselmouth
from parselmouth.praat import call
roh, text, aus, name = sys.argv[1:5]
HIER = os.path.dirname(os.path.abspath(__file__)); R = os.path.dirname(HIER); SR = 44100
ZIEL_HZ = 100
RAUSCH = ("highpass=f=60,anlmdn=s=0.0007,agate=threshold=0.01:ratio=3:range=0.15:attack=5:release=200:knee=6:detection=rms,"
          "atrim=start_sample=353,apad=pad_len=353")   # anlmdn verzögert um 8 ms (353 Samples), hier ausgeglichen
PAUSEN = {".": 0.9, "absatz": 1.3, ":": 0.55, ";": 0.55, "–": 0.45, ",": 0.30, "komma_ab": 0.15}
os.makedirs(aus, exist_ok=True); b = os.path.join(aus, name)
ff = lambda *a: subprocess.run(["ffmpeg", "-y", "-loglevel", "error", *a], check=True)
def lufs(f):
    o = subprocess.run(["ffmpeg", "-hide_banner", "-i", f, "-af", "ebur128", "-f", "null", "-"], capture_output=True, text=True).stderr
    return float(re.findall(r"I:\s+(-?[\d.]+) LUFS", o)[-1])

# 1. Tonlage: Median auf 100 Hz, Formanten unverändert (Praat „Change gender“, Tonhöhenerkennung 80–220 Hz)
x = np.frombuffer(subprocess.run(["ffmpeg", "-loglevel", "error", "-i", roh, "-ac", "1", "-ar", str(SR), "-f", "s16le", "-"],
                                 capture_output=True, check=True).stdout, np.int16).astype(np.float64) / 32768
snd = parselmouth.Sound(x, SR)
f0 = snd.to_pitch(time_step=0.01, pitch_floor=80, pitch_ceiling=220).selected_array["frequency"]; med = float(np.median(f0[f0 > 0]))
tief = call(snd, "Change gender", 80, 220, 1.0, ZIEL_HZ, 1.0, 1.0)
tief.save(b + ".tief.wav", "WAV")
print(f"Tonlage {med:.1f} → {ZIEL_HZ} Hz ({12 * np.log2(ZIEL_HZ / med):+.2f} Halbtöne)", flush=True)
# 2. Rauschunterdrückung, vor den Pausen, damit der eingefügte Raumton zum entrauschten Ton passt
ff("-i", b + ".tief.wav", "-af", RAUSCH, b + ".ru.wav")
# 3. Wortzeiten der Fassung ohne Pausen
subprocess.run([sys.executable, f"{R}/seite/karaoke_daten.py", "--einzeln", b + ".ru.wav", text, b + ".woerter.json"], check=True)
# 4. Pausen
subprocess.run([sys.executable, f"{HIER}/pausen2.py", b + ".ru.wav", b + ".woerter.json", b + ".pausen.mp3", json.dumps(PAUSEN), text], check=True)
# 5. Lautheit −18 LUFS (zwei Durchgänge, weil der Limiter etwas Pegel nimmt)
def laut(ziel, limit, codec):
    g = -18 - lufs(b + ".pausen.mp3")
    for _ in range(2):
        ff("-i", b + ".pausen.mp3", "-af", f"volume={g:.2f}dB,alimiter=limit={limit}:level=disabled", "-ac", "1", *codec, ziel)
        g += -18 - lufs(ziel)
    print(f"{os.path.basename(ziel)}: {lufs(ziel):.1f} LUFS", flush=True)
laut(b + ".mp3", 0.84, ["-b:a", "160k"])
laut(b + ".m4a", 0.72, ["-c:a", "aac", "-b:a", "64k", "-movflags", "+faststart"])
# 6. Wortzeiten der fertigen Fassung: um die eingefügten Pausen verschieben (exakt, ohne zweites Whisper)
W = json.load(open(b + ".woerter.json")); E = json.load(open(b + ".pausen.stellen.json"))
schieb = lambda t: t + sum(e["L"] for e in E if e["orig"] < t)
dauer = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", b + ".mp3"],
                             capture_output=True, text=True).stdout)
json.dump({"w": [w["w"] for w in W], "t": [round(schieb(w["s"]), 2) for w in W], "p": [w["p"] for w in W], "ende": round(dauer, 2)},
          open(b + ".karaoke.json", "w"), ensure_ascii=False)
for f in (".tief.wav", ".ru.wav"): os.remove(b + f)
print(f"fertig: {len(W)} Wörter, {dauer:.1f} s", flush=True)
