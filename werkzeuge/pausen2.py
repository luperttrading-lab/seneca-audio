"""Pausen einer durchgehenden Aufnahme auf natürliche Länge bringen, ohne Schleifen-Knattern.
Eingefügt wird nicht wiederholter Raumton: Rauschen mit Spektrum und Pegel der jeweiligen Pause, mit gleichleistungs-Überblendung."""
import sys, json, subprocess, numpy as np
src, words_json, out = sys.argv[1], sys.argv[2], sys.argv[3]
ZIEL = {".": 0.70, "?": 0.70, "!": 0.70, ":": 0.45, ";": 0.45, "–": 0.40, ",": 0.24, "absatz": 0.70}
if len(sys.argv) > 4: ZIEL.update(json.loads(sys.argv[4]))     # z. B. '{".": 0.9, "absatz": 1.3, ",": 0.35}'
ABSATZ = set()   # Wortnummern am Absatzende (aus der Textdatei, 5. Argument; Gedankenstriche zählen nicht als Wort)
if len(sys.argv) > 5:
    k = -1
    for para in open(sys.argv[5], encoding="utf-8").read().strip().split("\n\n"):
        k += sum(1 for t in para.split() if t != "–"); ABSATZ.add(k)
SR = 44100   # Überblendung je Pause bis 25 ms, ganz innerhalb der Pause
rng = np.random.default_rng(1)
x = np.frombuffer(subprocess.run(["ffmpeg","-loglevel","error","-i",src,"-ac","1","-ar",str(SR),"-f","s16le","-"],capture_output=True,check=True).stdout, np.int16).astype(np.float64)/32768
n = int(SR*0.01); fr = x[:len(x)//n*n].reshape(-1,n); db = 10*np.log10((fr**2).mean(1)+1e-12)
still = db < max(np.percentile(db,95)-35, np.percentile(db,10)+6)
print(f"Stille-Schwelle {max(np.percentile(db,95)-35, np.percentile(db,10)+6):.1f} dB, Sprache p95 {np.percentile(db,95):.1f} dB")
NF = 2048
def spektrum(seg):
    """mittleres Betragsspektrum (Welch, Hann) eines Pausenstücks"""
    w = np.hanning(NF); h = NF // 4
    if len(seg) < NF: seg = np.concatenate([seg, seg[::-1]] * (NF // max(len(seg), 1) + 1))[:NF]
    fr = [np.abs(np.fft.rfft(seg[i:i+NF]*w)) for i in range(0, len(seg)-NF+1, h)]
    return np.sqrt(np.mean(np.square(fr), 0))
alle = np.concatenate([x[i*n:(i+1)*n] for i in np.flatnonzero(still)])   # Rückfall, falls die Pause zu kurz ist
SP_ALL = spektrum(alle)
def rauschen(L, sp, rms):
    """Gauß-Rauschen der Länge L, im Frequenzbereich auf das Pausenspektrum geformt, auf rms skaliert"""
    w = rng.standard_normal(L + NF); W = np.fft.rfft(w)
    form = np.interp(np.linspace(0, 1, len(W)), np.linspace(0, 1, len(sp)), sp)
    y = np.fft.irfft(W * form, len(w))[NF//2:NF//2+L]
    return y * rms / (np.sqrt(np.mean(y**2)) + 1e-20)
W = json.load(open(words_json, encoding="utf-8"))
einfueg = []
for i, w in enumerate(W[:-1]):
    z = w["w"].rstrip("»«“\"'")
    zeichen = next((c for c in ["–", ".", "?", "!", ":", ";", ","] if z.endswith(c)), None)
    if not zeichen: continue
    a0, a1 = int((w["s"] + 0.5*(W[i+1]["s"]-w["s"])) / 0.01), int(W[i+1]["s"] / 0.01) + 5
    a0 = max(int(w["s"]/0.01), a0 - 40)
    best, cur, beststart, start = 0, 0, None, None
    for f in range(a0, min(a1, len(still))):
        if still[f]:
            if cur == 0: start = f
            cur += 1
            if cur > best: best, beststart = cur, start
        else: cur = 0
    lang = best * 0.01
    if lang < 0.06 or beststart is None: continue
    soll = ZIEL["absatz"] if (i in ABSATZ and zeichen in ".?!") else ZIEL[zeichen]
    if lang >= soll: continue
    # Einfügepunkt: leisteste Stelle, an der die Überblendung ganz in der Pause liegt (Wortränder unberührt)
    xf = int(min(0.025, max(0.005, lang / 2 - 0.005)) * SR)
    lo, hi = beststart * n + xf, (beststart + best) * n - xf
    kand = list(range(lo, hi + 1, n // 2)) or [(lo + hi) // 2]
    pos = min(kand, key=lambda q: np.mean(x[q-xf:q+xf]**2))
    ref = x[beststart*n:(beststart+best)*n]
    sp = spektrum(ref) if len(ref) >= NF else SP_ALL * (np.sqrt(np.mean(ref**2)) / (np.sqrt(np.mean(alle**2)) + 1e-20))
    rms = np.sqrt(np.mean(x[pos-xf:pos+xf]**2))      # Pegel genau an der Schnittstelle
    einfueg.append((pos, int((soll - lang) * SR), zeichen, lang, sp, rms, xf))
teile, p = [], 0
for pos, L, _, _, sp, rms, xf in einfueg:
    t = np.linspace(0, np.pi/2, xf); ein, aus = np.sin(t), np.cos(t)      # gleichleistungs-Überblendung
    r = rauschen(L + 2*xf, sp, rms)
    teile += [x[p:pos-xf], x[pos-xf:pos]*aus + r[:xf]*ein, r[xf:-xf], r[-xf:]*aus + x[pos:pos+xf]*ein]
    p = pos + xf
teile.append(x[p:]); y = np.concatenate(teile)
subprocess.run(["ffmpeg","-y","-loglevel","error","-f","s16le","-ar",str(SR),"-ac","1","-i","-","-c:a","libmp3lame","-q:a","2",out], input=(np.clip(y,-1,1)*32767).astype(np.int16).tobytes(), check=True)
json.dump([{"orig": pos/SR, "L": L/SR, "z": z, "vorher": lang, "xf": xf/SR} for pos, L, z, lang, _, _, xf in einfueg], open(out.rsplit(".",1)[0] + ".stellen.json", "w"), indent=0)
print(f"{len(einfueg)} Pausen verlängert, +{sum(e[1] for e in einfueg)/SR:.1f} s, Dauer {len(x)/SR:.1f} → {len(y)/SR:.1f} s")
