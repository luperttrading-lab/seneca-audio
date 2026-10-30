"""Einen Satz nachbessern: satz.py <kapitel> "<Satzanfang>" <ordner> [--fassungen 3]   dann   satz.py ... --nimm <n>

Befund 29.10. (PLAN.md, Prüfliste Ton, Punkt 4): falsche Akzente kommen vom Folgesatz im selben Text; allein und ohne
Zusammenhang erzeugt war derselbe Satz 6 von 6 richtig betont. <ordner> ist der Ausordner von kapitel.py.
1. Ohne --nimm: den Satz allein und ohne Zusammenhang in mehreren Fassungen erzeugen (kostet Credits, je etwa 0,43 je
   Zeichen; vorhandene Fassungen werden wiederverwendet), jede prüfen (Worttreue, Betonungsfilter, Stimme per
   Fingerabdruck, falls `WESPEAKER_ONNX` gesetzt ist) und Hörproben wie im Kapitel bearbeiten (Tempo 0,96, −18 LUFS):
   <ordner>/satz/<name>_aN.mp3 und <name>.json für die Prüfseite.
2. Mit --nimm n: Fassung n an den Satzpausen in die Rohaufnahme des Kapitels einsetzen (Schnitt in der Mitte der Pausen,
   der neue Satz mit 50 ms Rand davor und 100 ms danach, 10 ms Blenden, Pegel wie der alte Satz). Die bisherige
   Rohaufnahme bleibt als .vorherN.mp3; danach läuft kapitel.py ohne neue Credits: Worttreue, Wortzeiten und Pausen neu.
   Mehrere Sätze: alle außer dem letzten mit --ohne-kette einsetzen (die Wortzeiten werden dann nur verschoben).
"""
import json, os, re, subprocess, sys, urllib.request, wave
import numpy as np

HIER = os.path.dirname(os.path.abspath(__file__)); R = os.path.dirname(HIER); sys.path.insert(0, HIER)
import stellen, betonung
from kette import STIMME, MODELL, TEMPO, SR, RAUSCH, ff, py, lufs, lade, sprache, pegel

args = sys.argv[1:]
nimm = int(args[args.index("--nimm") + 1]) if "--nimm" in args else None
anzahl = int(args[args.index("--fassungen") + 1]) if "--fassungen" in args else 3
kap, anfang, aus = int(args[0]), args[1], args[2]
b = os.path.join(aus, f"kapitel{kap:02d}"); ordner = os.path.join(aus, "satz"); os.makedirs(ordner, exist_ok=True)
norm = lambda s: re.sub(r"[^a-zäöüß0-9 ]", "", s.lower().replace("-", " ")).split()

text = stellen.rein(open(f"{R}/texte/kapitel{kap:02d}.txt", encoding="utf-8").read())
teile = lambda t: [s.strip() for absatz in re.split(r"\n\s*\n", t) for s in re.split(r"(?<=[.!?…])[“”»«\"]?\s+", absatz) if s.strip()]
saetze = teile(text)
treffer = [s for s in saetze if norm(s)[:len(norm(anfang))] == norm(anfang)]
if len(treffer) != 1: sys.exit(f"Satzanfang passt auf {len(treffer)} Sätze: {[t[:50] for t in treffer]}")
satz = treffer[0].strip("„“»«\"")
import hashlib   # Wortlaut im Namen, damit eine neue Fassung desselben Satzes nicht alte Aufnahmen wiederverwendet
name = f"k{kap:02d}_" + "_".join(norm(satz)[:3]) + "_" + hashlib.md5(satz.encode()).hexdigest()[:5]
datei = lambda n, e: os.path.join(ordner, f"{name}_a{n}{e}")
open(os.path.join(ordner, name + ".text.txt"), "w", encoding="utf-8").write(satz + "\n")


def sprich(ziel):   # allein, ohne previous_text/next_text
    req = urllib.request.Request(f"https://api.elevenlabs.io/v1/text-to-speech/{STIMME}?output_format=mp3_44100_128",
                                 data=json.dumps({"text": satz, "model_id": MODELL, "voice_settings": {"stability": 0.5}}).encode(),
                                 headers={"xi-api-key": os.environ["ELEVENLABS_API_KEY"], "Content-Type": "application/json"})
    r = urllib.request.urlopen(req, timeout=300); open(ziel, "wb").write(r.read()); return int(r.headers.get("character-cost") or 0)


def schreibe(y, ziel):
    with wave.open(ziel, "wb") as w: w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((np.clip(y, -1, 1) * 32767).astype(np.int16).tobytes())


def stelle_im_kapitel(W, satz):   # Wortindizes des Satzes in woerter.json des Kapitels
    soll = norm(satz); ist = [" ".join(norm(w["w"])) for w in W]; L = len(soll)
    for i in range(len(W)):
        if " ".join(ist[i:i + L]).split() == soll: return i, i + L - 1
    sys.exit("Satz nicht in den Wortzeiten des Kapitels gefunden")


if nimm is None:
    credits, erg = 0, []
    fp = None
    if os.environ.get("WESPEAKER_ONNX") and os.path.exists(os.environ["WESPEAKER_ONNX"]):
        import fingerabdruck as fp; ref = fp.emb(b + ".roh.mp3")
    for n in range(1, anzahl + 1):
        if not os.path.exists(datei(n, ".roh.mp3")): credits += sprich(datei(n, ".roh.mp3"))
        ff("-i", datei(n, ".roh.mp3"), "-ac", "1", "-ar", str(SR), "-af", RAUSCH, datei(n, ".ru.wav"))
        py(f"{R}/seite/karaoke_daten.py", "--einzeln", datei(n, ".ru.wav"), os.path.join(ordner, name + ".text.txt"), datei(n, ".woerter.json"), capture_output=True, text=True)
        p = py(f"{HIER}/pruef.py", "large-v3-turbo", os.path.join(ordner, name + ".text.txt"), datei(n, ".roh.mp3"), capture_output=True, text=True)
        treu = "wortgetreu" in p.stdout
        W = json.load(open(datei(n, ".woerter.json"), encoding="utf-8"))
        E = betonung.pruefe(datei(n, ".ru.wav"), W); m = [e for e in E if e["markiert"]]
        x = lade(datei(n, ".ru.wav")); a0, a1 = sprache(x); x = x[max(0, a0 - 4410):a1 + 6615]
        schreibe(np.concatenate([np.zeros(int(0.3 * SR)), x, np.zeros(int(0.4 * SR))]), datei(n, ".t1.wav"))
        ff("-i", datei(n, ".t1.wav"), "-af", f"atempo={TEMPO}", datei(n, ".langsam.wav"))
        ff("-i", datei(n, ".langsam.wav"), "-af", f"volume={-18 - lufs(datei(n, '.langsam.wav')):.2f}dB,alimiter=limit=0.84:level=disabled", "-b:a", "128k", datei(n, ".mp3"))
        versatz = 0.3 - max(0, a0 - 4410) / SR
        erg.append({"n": n, "datei": os.path.basename(datei(n, ".mp3")), "wortgetreu": treu, "betonung": [e["betont"] for e in m],
                    "stimme": round(float(fp.emb(datei(n, ".roh.mp3")) @ ref), 3) if fp else None,
                    "w": [{"w": w["w"], "t": round((w["s"] + versatz) / TEMPO, 3)} for w in W]})
        for e in (".ru.wav", ".t1.wav", ".langsam.wav"): os.remove(datei(n, e))
        z = erg[-1]; print(f"Fassung {n}: {'wortgetreu' if treu else 'ABWEICHUNG: ' + p.stdout.strip().splitlines()[-1]} · Betonung "
                          f"{'markiert: ' + ', '.join(z['betonung']) if z['betonung'] else 'unauffällig'} · Stimme {z['stimme']}", flush=True)
    json.dump({"satz": satz, "fassungen": erg}, open(os.path.join(ordner, name + ".json"), "w"), ensure_ascii=False)
    print(f"{name}: {len(satz)} Zeichen, {credits} Credits; einsetzen mit --nimm <n>")
else:
    W = json.load(open(b + ".woerter.json", encoding="utf-8"))
    # Wurde der Satz im Text geändert, steht in der Aufnahme noch der alte: über seine Nummer im Text der Aufnahme finden
    alt = teile(open(b + ".text.txt", encoding="utf-8").read()); nr = saetze.index(treffer[0])
    if len(alt) != len(saetze): sys.exit("Satzzahl der Aufnahme und des Textes verschieden: Satz nicht eindeutig zuzuordnen")
    if norm(alt[nr]) != norm(satz): print("Satz geändert, ersetzt in der Aufnahme:", alt[nr], flush=True)
    i0, i1 = stelle_im_kapitel(W, alt[nr].strip("„“»«\""))
    y = lade(b + ".roh.mp3"); s = lade(datei(nimm, ".roh.mp3"))
    a = int((W[i0 - 1]["e"] + W[i0]["s"]) / 2 * SR) if i0 else int(max(0, W[i0]["s"] - 0.3) * SR)
    e = int((W[i1]["e"] + W[i1 + 1]["s"]) / 2 * SR) if i1 + 1 < len(W) else len(y)
    s0, s1 = sprache(s); s = s[max(0, s0 - int(0.05 * SR)):s1 + int(0.10 * SR)].copy()
    s *= pegel(y[a:e]) / pegel(s)
    k = int(0.01 * SR); s[:k] *= np.linspace(0, 1, k); s[-k:] *= np.linspace(1, 0, k)
    vor, nach = y[:a].copy(), y[e:].copy(); vor[-k:] *= np.linspace(1, 0, k); nach[:k] *= np.linspace(0, 1, k)
    n = 1
    while os.path.exists(f"{b}.roh.vorher{n}.mp3"): n += 1
    os.rename(b + ".roh.mp3", f"{b}.roh.vorher{n}.mp3")
    schreibe(np.concatenate([vor, s, nach]), b + ".roh.wav"); ff("-i", b + ".roh.wav", "-b:a", "192k", b + ".roh.mp3"); os.remove(b + ".roh.wav")
    kette = "--ohne-kette" not in args
    for x in ((".woerter.json",) if kette else ()) + (".pausen.stellen.json", ".pausen.mp3"):
        if os.path.exists(b + x): os.remove(b + x)
    if not kette:   # Wortzeiten hinter dem Schnitt verschieben, damit der nächste Satz seinen Platz findet
        d = (len(s) - (e - a)) / SR
        for w in W[i1 + 1:]: w["s"] = round(w["s"] + d, 3); w["e"] = round(w["e"] + d, 3)
        json.dump(W, open(b + ".woerter.json", "w", encoding="utf-8"), ensure_ascii=False)
    j = os.path.join(ordner, name + ".json"); d = json.load(open(j, encoding="utf-8")); d["eingesetzt"] = nimm
    json.dump(d, open(j, "w", encoding="utf-8"), ensure_ascii=False)   # für die Hörprobe
    print(f"Fassung {nimm} eingesetzt ({W[i0]['w']} … {W[i1]['w']}, {(e - a) / SR:.2f} s ersetzt durch {len(s) / SR:.2f} s); "
          f"alte Rohaufnahme: {os.path.basename(b)}.roh.vorher{n}.mp3", flush=True)
    if kette:
        r = subprocess.run([sys.executable, f"{HIER}/kapitel.py", str(kap), aus, "--ohne-video"], capture_output=True, text=True, stdin=subprocess.DEVNULL)
        print(r.stdout.strip()); print(r.stderr.strip().splitlines()[-1] if r.returncode else "")
    else: print("Kette nicht gerechnet (--ohne-kette): nächsten Satz einsetzen, beim letzten ohne --ohne-kette")
