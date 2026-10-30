"""Ein Kapitel vom Text bis zum Video: kapitel.py <nr> <ausordner> [--neu] [--ohne-video] [--trotz-abweichung]

Schritte (am 29.10. mit dem Nutzer festgelegt):
1. Text ohne Stellenmarken (stellen.py) an ElevenLabs: Helmut Stieglbauer – Deep and Dynamic, eleven v4, Stability 0,5.
   Die Rohaufnahme wird zwischengespeichert und nur mit --neu wieder erzeugt (kostet Credits).
2. Worttreue der Rohaufnahme mit Whisper (pruef.py); bei Abweichungen auch in der Gegenprobe Abbruch vor der
   Weiterverarbeitung. --trotz-abweichung überspringt die Prüfung und rechnet weiter, damit die gemeldeten Stellen
   auf der Hörprobe (seite/hoerprobe.py) angehört werden können.
3. Rauschunterdrückung, Wortzeiten (karaoke_daten.py), Pausen wie in Teil 1 („ruhig“, pausen2.py), an Kommas nur, wo
   Helmut schon pausiert (kette.py).
4. Tempo 0,96 nachträglich (ffmpeg atempo, Tonhöhe bleibt), so wie in der Stimmenprobe gewählt; −18 LUFS.
   Kapitel 1 beginnt mit der Startseite und dem gesprochenen „Seneca. Vom glücklichen Leben.“
5. daten.json für das Video (Wörter, Zeiten, Absätze, Stelle je Wort) und das Video selbst (video/baue.py).
Ergebnis im Ausordner: kapitelNN.mp3 (160 kbit/s), kapitelNN.wav, kapitelNN.daten.json, kapitelNN.mp4.
"""
import json, os, re, subprocess, sys, urllib.request, wave
import numpy as np

HIER = os.path.dirname(os.path.abspath(__file__)); R = os.path.dirname(HIER); sys.path.insert(0, HIER)
import stellen

nr, aus = int(sys.argv[1]), sys.argv[2]; neu = "--neu" in sys.argv
from kette import STIMME, MODELL, TEMPO, SR, RAUSCH, PAUSEN, ff, py, lufs, lade, sprache, pegel
os.makedirs(aus, exist_ok=True); b = os.path.join(aus, f"kapitel{nr:02d}")

def tts(text, ziel):
    if os.path.exists(ziel) and not neu: return 0
    req = urllib.request.Request(f"https://api.elevenlabs.io/v1/text-to-speech/{STIMME}?output_format=mp3_44100_128",
                                 data=json.dumps({"text": text, "model_id": MODELL, "voice_settings": {"stability": 0.5}}).encode(),
                                 headers={"xi-api-key": os.environ["ELEVENLABS_API_KEY"], "Content-Type": "application/json"})
    r = urllib.request.urlopen(req, timeout=600); open(ziel, "wb").write(r.read()); return int(r.headers.get("character-cost") or 0)

# 1. Text ohne Marken, Rohaufnahme
markiert = open(f"{R}/texte/kapitel{nr:02d}.txt", encoding="utf-8").read()
rein = b + ".text.txt"; open(rein, "w", encoding="utf-8").write(stellen.rein(markiert))
text = open(rein, encoding="utf-8").read().strip()
credits = tts(text, b + ".roh.mp3")
if nr == 1: credits += tts("Seneca. Vom glücklichen Leben.", os.path.join(aus, "start.roh.mp3"))
print(f"Kapitel {nr}: {len(text)} Zeichen, {credits} Credits", flush=True)
fertig = credits == 0 and not neu and os.path.exists(b + ".pausen.stellen.json")   # Schritte 2–3 schon gelaufen
# 2. Worttreue
trotz = "--trotz-abweichung" in sys.argv   # Worttreue schon geprüft, Abweichungen sollen auf die Hörprobe (Auftraggeber hört)
if not fertig and not trotz: p = py(f"{HIER}/pruef.py", "large-v3-turbo", rein, b + ".roh.mp3", capture_output=True, text=True)
if trotz and not fertig: print("Worttreue übersprungen (--trotz-abweichung): gemeldete Stellen auf der Hörprobe anhören", flush=True)
if not fertig:
    zeile = "wortgetreu" if trotz else [l for l in p.stdout.splitlines() if "large-v3-turbo" in l][-1]
    if not trotz: print(zeile, flush=True)
    if "wortgetreu" not in zeile:   # Gegenprobe mit dem großen Modell: turbo verhört sich gelegentlich („Wahlen“ → „Walen“)
        p = py(f"{HIER}/pruef.py", "large-v3", rein, b + ".roh.mp3", capture_output=True, text=True)
        zeile = [l for l in p.stdout.splitlines() if "large-v3" in l][-1]; print("Gegenprobe:", zeile, flush=True)
        if "wortgetreu" not in zeile: sys.exit("Abweichungen in der Rohaufnahme – bitte anhören, bevor weiterverarbeitet wird")
    # 3. Rauschunterdrückung, Wortzeiten, Pausen
    ff("-i", b + ".roh.mp3", "-ac", "1", "-ar", str(SR), "-af", RAUSCH, b + ".ru.wav")
    k = py(f"{R}/seite/karaoke_daten.py", "--einzeln", b + ".ru.wav", rein, b + ".woerter.json", capture_output=True, text=True)
    print([l for l in k.stdout.splitlines() if "Wörter" in l][-1].split(",", 1)[-1].strip(), flush=True)
    p = py(f"{HIER}/pausen2.py", b + ".ru.wav", b + ".woerter.json", b + ".pausen.mp3", json.dumps(PAUSEN), rein, capture_output=True, text=True)
    print(p.stdout.strip().splitlines()[-1], flush=True); os.remove(b + ".ru.wav")
else: print("Prüfung, Wortzeiten und Pausen schon vorhanden", flush=True)
W = json.load(open(b + ".woerter.json")); E = json.load(open(b + ".pausen.stellen.json"))
schieb = lambda t: t + sum(e["L"] for e in E if e["orig"] < t)
# 4. Zusammensetzen (bei Tempo 1), dann Tempo 0,96 und −18 LUFS
x = lade(b + ".pausen.mp3"); a0, a1 = sprache(x); x = x[max(0, a0 - 2205):a1 + 4410]; kopf = max(0, a0 - 2205) / SR
teile, o = [], 0.5
if nr == 1:
    ff("-i", os.path.join(aus, "start.roh.mp3"), "-ac", "1", "-ar", str(SR), "-af", RAUSCH, os.path.join(aus, "start.ru.wav"))
    s = lade(os.path.join(aus, "start.ru.wav")); s0, s1 = sprache(s); s = s[s0:s1 + 2205]
    teile.append((s * pegel(x) / pegel(s), 0.6)); o = 0.6 + len(s) / SR + 1.6
teile.append((x, o)); ende = o + len(x) / SR + 1.5
y = np.zeros(int(ende * SR) + 1)
for z, t0 in teile: i = int(round(t0 * SR)); y[i:i + len(z)] += z
with wave.open(b + ".tempo1.wav", "wb") as w: w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((np.clip(y, -1, 1) * 32767).astype(np.int16).tobytes())
ff("-i", b + ".tempo1.wav", "-af", f"atempo={TEMPO}", b + ".langsam.wav")
g = -18 - lufs(b + ".langsam.wav")
for _ in range(2):
    ff("-i", b + ".langsam.wav", "-af", f"volume={g:.2f}dB,alimiter=limit=0.84:level=disabled", b + ".wav"); g += -18 - lufs(b + ".wav")
ff("-i", b + ".wav", "-b:a", "160k", b + ".mp3")
# 5. Daten für das Video und Video
T = [round((schieb(w["s"]) - kopf + o) / TEMPO, 3) for w in W]; ST = stellen.liste(markiert)
assert len(ST) == len(W), (len(ST), len(W))
D = {"w": [w["w"] for w in W], "t": T, "p": [w["p"] for w in W], "stelle": ST, "ende": round(len(y) / SR / TEMPO, 3)}
if nr == 1: D["start_ende"] = round(T[0] - 1.3, 3); D["text_ab"] = round(D["start_ende"] + 0.55, 3)
json.dump(D, open(b + ".daten.json", "w"), ensure_ascii=False)
print(f"Ton: {lufs(b + '.wav'):.1f} LUFS, {D['ende']:.1f} s; erstes Wort bei {T[0]:.2f} s", flush=True)
for f in (".tempo1.wav", ".langsam.wav"): os.remove(b + f)
if "--ohne-video" not in sys.argv: py(f"{HIER}/video/baue.py", b + ".daten.json", b + ".wav", b + ".mp4")
