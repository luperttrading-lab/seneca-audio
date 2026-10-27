import json, subprocess, numpy as np
SR = 44100; N = "/tmp/claude-0/-home-user/0523a428-572b-5d43-9560-e7907758c764/scratchpad"; XF = int(0.025*SR)
lade = lambda f: np.frombuffer(subprocess.run(["ffmpeg","-loglevel","error","-i",f,"-ac","1","-ar",str(SR),"-f","s16le","-"],capture_output=True,check=True).stdout, np.int16).astype(np.float64)/32768
x = lade(f"{N}/lupert2/lupert_exp.mp3"); alt = lade(f"{N}/lupert2/lupert_exp_pausen_knattert.mp3"); neu = lade(f"{N}/lupert2/lupert_exp_pausen2.mp3")
def mass(seg):
    m = int(0.005*SR); lev = 10*np.log10((seg[:len(seg)//m*m].reshape(-1,m)**2).mean(1)+1e-12)
    # Hüllkurven-Modulation bei 10–25 Hz (Knattern) relativ zu 2–8 Hz
    e = np.sqrt((seg[:len(seg)//44*44].reshape(-1,44)**2).mean(1)); e = e - e.mean()
    E = np.abs(np.fft.rfft(e*np.hanning(len(e))))**2; f = np.fft.rfftfreq(len(e), 44/SR)
    mod = 10*np.log10(E[(f>=12)&(f<=22)].mean() / (E[(f>=30)&(f<=60)].mean()+1e-30))
    return np.std(lev), lev.min(), mod
def sprung(sig, i):   # größter Sprung der 1-ms-Pegelkurve rund um eine Nahtstelle
    m = 44; seg = sig[i-20*m:i+20*m]; lev = 10*np.log10((seg[:len(seg)//m*m].reshape(-1,m)**2).mean(1)+1e-12)
    return np.abs(np.diff(lev)).max()
S_alt = json.load(open("stellen.json")); S_neu = json.load(open(f"{N}/lupert2/lupert_exp_pausen2.stellen.json"))
# natürliche Referenz: ruhige Kerne echter Pausen im Original
ref = [mass(x[int((s["orig"]-0.05)*SR):int((s["orig"]+0.05)*SR)]) for s in S_neu if s["vorher"] >= 0.2]
print("Original-Pausen (Kern 100 ms): Schwankung %.1f dB, Minimum %.0f dB, Knatter-Modulation %+.1f dB" % tuple(np.median(ref, 0)))
off = 0; ra = []
for s in S_alt:
    a = int((s["neu"])*SR); L = int(s["L"]*SR); ra.append(mass(alt[a:a+L]))
print("alte Fassung, eingefügt:        Schwankung %.1f dB, Minimum %.0f dB, Knatter-Modulation %+.1f dB" % tuple(np.median(ra, 0)))
off = 0; rn = []; nahtA = []; nahtN = []
for s in S_neu:
    p = int(s["orig"]*SR); L = int(s["L"]*SR); a = p - XF + off
    rn.append(mass(neu[a:a+L+2*XF])); nahtN += [sprung(neu, a), sprung(neu, a+L+2*XF)]; off += L
off = 0
for s in S_alt:
    a = int(s["neu"]*SR); L = int(s["L"]*SR); nahtA += [sprung(alt, a), sprung(alt, a+L)]
print("neue Fassung, eingefügt:        Schwankung %.1f dB, Minimum %.0f dB, Knatter-Modulation %+.1f dB" % tuple(np.median(rn, 0)))
print("schlimmster Wert je Fassung (Schwankung, Minimum, Modulation): alt", np.round(np.max(ra,0),1), np.round(np.min(ra,0)[1],0), " neu", np.round(np.max(rn,0),1), np.round(np.min(rn,0)[1],0))
print("Nahtstellen, größter Pegelsprung in 1 ms: alt median %.1f max %.1f dB | neu median %.1f max %.1f dB" % (np.median(nahtA), max(nahtA), np.median(nahtN), max(nahtN)))
