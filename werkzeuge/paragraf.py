"""Einen Paragrafen neu sprechen lassen und wie das Kapitel bearbeiten: paragraf.py <kapitel> <paragraf> <ausordner> [--neu] [--saetze]

Für Nachbesserungen einzelner Stellen (29.10.): gleiche Stimme und Einstellungen wie werkzeuge/kapitel.py, Satz davor und
danach gehen als Zusammenhang mit (previous_text/next_text), damit der Paragraf nicht wie ein Anfang klingt. Danach
Worttreue (Whisper), Rauschunterdrückung, Wortzeiten, Pausen, Tempo 0,96, −18 LUFS. Ergebnis: kNN_pP.mp3 (Tonspur zum
Anhören) und kNN_pP.json (Wörter und Zeiten für das Mitlesen). Die Rohaufnahme wird zwischengespeichert, --neu erzeugt
eine weitere Fassung (kostet Credits); jede Fassung bekommt eine eigene Nummer.

--saetze: jeder Satz als eigene Anfrage, Satz davor und danach nur als Zusammenhang (Versuch 29.10.: steht der Folgesatz
im gesprochenen Text, verschiebt das Modell Akzente im Satz davor; als next_text schadet er nicht). Die Sätze werden mit
ihrer eigenen Rand-Stille aneinandergesetzt, auf gleichen Sprachpegel gebracht und dann wie eine Aufnahme bearbeitet.
"""
import glob, json, os, re, subprocess, sys, urllib.error, urllib.request, wave
import numpy as np

HIER = os.path.dirname(os.path.abspath(__file__)); R = os.path.dirname(HIER); sys.path.insert(0, HIER)
import stellen
from kette import RAUSCH, PAUSEN, STIMME, MODELL, TEMPO, SR, ff, py, lufs, lade, sprache, pegel   # dieselbe Kette wie im Kapitel

kap, par, aus = int(sys.argv[1]), int(sys.argv[2]), sys.argv[3]; os.makedirs(aus, exist_ok=True)
markiert = open(f"{R}/texte/kapitel{kap:02d}.txt", encoding="utf-8").read()
teile = re.split(r"(\[\d+,\d+\])", markiert)
nr = [i for i, t in enumerate(teile) if t == f"[{kap},{par}]"][0]
text = stellen.rein(teile[nr + 1]).strip()
vorher = stellen.rein("".join(teile[:nr])).strip(); nachher = stellen.rein("".join(teile[nr + 2:])).strip()
satz = lambda s: re.split(r"(?<=[.!?])\s+", s)
kontext = {"previous_text": satz(vorher)[-1] if vorher else None, "next_text": satz(nachher)[0] if nachher else None}

saetze = "--saetze" in sys.argv; art = "s" if saetze else "f"
fassungen = sorted(glob.glob(os.path.join(aus, f"k{kap:02d}_p{par}_{art}[0-9].roh.mp3")))
f = len(fassungen) + 1 if ("--neu" in sys.argv or not fassungen) else len(fassungen)
b = os.path.join(aus, f"k{kap:02d}_p{par}_{art}{f}"); rein = b + ".text.txt"; open(rein, "w", encoding="utf-8").write(text + "\n")

def sprich(text, kontext, ziel):
    daten = {"text": text, "model_id": MODELL, "voice_settings": {"stability": 0.5}, **{k: v for k, v in kontext.items() if v}}
    req = urllib.request.Request(f"https://api.elevenlabs.io/v1/text-to-speech/{STIMME}?output_format=mp3_44100_128", data=json.dumps(daten).encode(),
                                 headers={"xi-api-key": os.environ["ELEVENLABS_API_KEY"], "Content-Type": "application/json"})
    try: r = urllib.request.urlopen(req, timeout=600)
    except urllib.error.HTTPError as e:   # falls das Modell den Zusammenhang nicht annimmt: ohne ihn
        print("Zusammenhang abgelehnt:", e.code, e.read()[:200], flush=True)
        req.data = json.dumps({k: v for k, v in daten.items() if k not in kontext}).encode(); r = urllib.request.urlopen(req, timeout=600)
    open(ziel, "wb").write(r.read()); return int(r.headers.get("character-cost") or 0)

if not os.path.exists(b + ".roh.mp3") and not saetze:
    print(f"Fassung {f}: {len(text)} Zeichen, {sprich(text, kontext, b + '.roh.mp3')} Credits", flush=True)
elif not os.path.exists(b + ".roh.mp3"):
    S = satz(text); credits = 0; stuecke = []
    for j, s in enumerate(S):
        k = {"previous_text": S[j - 1] if j else kontext["previous_text"], "next_text": S[j + 1] if j + 1 < len(S) else kontext["next_text"]}
        z = f"{b}.satz{j + 1}.mp3"
        if not os.path.exists(z): credits += sprich(s, k, z)
        y = lade(z); a0, a1 = sprache(y); y = y[max(0, a0 - 4410):a1 + 6615].copy()   # eigene Stille: 100 ms davor, 150 ms danach
        n = int(0.005 * SR); y[:n] *= np.linspace(0, 1, n); y[-n:] *= np.linspace(1, 0, n); stuecke.append(y)   # gegen Knacken
    ziel = np.median([pegel(y) for y in stuecke])
    print(f"Fassung {f}: {len(S)} Sätze, {len(text)} Zeichen, {credits} Credits; Pegel angeglichen um "
          + ", ".join(f"{20 * np.log10(ziel / pegel(y)):+.1f}" for y in stuecke) + " dB", flush=True)
    y = np.concatenate([y * ziel / pegel(y) for y in stuecke])
    with wave.open(b + ".roh.wav", "wb") as w: w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((np.clip(y, -1, 1) * 32767).astype(np.int16).tobytes())
    ff("-i", b + ".roh.wav", "-b:a", "192k", b + ".roh.mp3"); os.remove(b + ".roh.wav")
p = py(f"{HIER}/pruef.py", "large-v3-turbo", rein, b + ".roh.mp3", capture_output=True, text=True)
print([l for l in p.stdout.splitlines() if "large-v3-turbo" in l][-1], flush=True)
ff("-i", b + ".roh.mp3", "-ac", "1", "-ar", str(SR), "-af", RAUSCH, b + ".ru.wav")
py(f"{R}/seite/karaoke_daten.py", "--einzeln", b + ".ru.wav", rein, b + ".woerter.json", capture_output=True, text=True)
p = py(f"{HIER}/pausen2.py", b + ".ru.wav", b + ".woerter.json", b + ".pausen.mp3", json.dumps(PAUSEN), rein, capture_output=True, text=True)
print(p.stdout.strip().splitlines()[-1], flush=True)
W = json.load(open(b + ".woerter.json")); E = json.load(open(b + ".pausen.stellen.json"))
schieb = lambda t: t + sum(e["L"] for e in E if e["orig"] < t)
x = lade(b + ".pausen.mp3"); a0, a1 = sprache(x); kopf = max(0, a0 - 2205); x = x[kopf:a1 + 4410]
y = np.concatenate([np.zeros(int(0.3 * SR)), x, np.zeros(int(0.5 * SR))])
with wave.open(b + ".t1.wav", "wb") as w: w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((np.clip(y, -1, 1) * 32767).astype(np.int16).tobytes())
ff("-i", b + ".t1.wav", "-af", f"atempo={TEMPO}", b + ".langsam.wav")
g = -18 - lufs(b + ".langsam.wav")
for _ in range(2):
    ff("-i", b + ".langsam.wav", "-af", f"volume={g:.2f}dB,alimiter=limit=0.84:level=disabled", b + ".wav"); g += -18 - lufs(b + ".wav")
ff("-i", b + ".wav", "-b:a", "160k", b + ".mp3")
o = 0.3 - kopf / SR
json.dump({"w": [w["w"] for w in W], "t": [round((schieb(w["s"]) + o) / TEMPO, 3) for w in W], "dauer": round(len(y) / SR / TEMPO, 3)},
          open(b + ".json", "w"), ensure_ascii=False)
for e in (".ru.wav", ".t1.wav", ".langsam.wav"): os.remove(b + e)
print(f"{os.path.basename(b)}.mp3: {lufs(b + '.wav'):.1f} LUFS, {len(y) / SR / TEMPO:.1f} s", flush=True)
