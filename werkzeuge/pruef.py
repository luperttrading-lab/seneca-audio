import sys, json, re, difflib, subprocess, numpy as np
from faster_whisper import WhisperModel
norm = lambda t: re.sub(r"[^a-zäöü0-9]", "", re.sub(r"\bgall?io\b", "gallio", re.sub(r"\bdass\b", "das", t.lower().replace("ß", "ss"))))
m = WhisperModel(sys.argv[1], device="cpu", compute_type="int8", cpu_threads=4)
soll = norm(open(sys.argv[2], encoding="utf-8").read())
for f in sys.argv[3:]:
    a = np.frombuffer(subprocess.run(["ffmpeg","-loglevel","error","-i",f,"-ac","1","-ar","16000","-f","s16le","-"],capture_output=True,check=True).stdout, np.int16).astype(np.float32)/32768
    fr = a[: len(a) // 160 * 160].reshape(-1, 160).astype(np.float64); db = 10 * np.log10((fr ** 2).mean(1) + 1e-12)
    still = db < max(np.percentile(db, 95) - 35, np.percentile(db, 10) + 6); dauer = len(a) / 16000
    pausen, k = [], 0
    while k < len(still):
        if still[k]:
            j = k
            while j < len(still) and still[j]: j += 1
            if (j - k) * 0.01 >= 0.3: pausen.append((k + j) / 2 * 0.01)
            k = j
        else: k += 1
    schnitte, start = [0.0], 0.0
    for i, pz in enumerate(pausen):
        nx = pausen[i + 1] if i + 1 < len(pausen) else dauer
        if nx - start > 20 and pz - start > 3: schnitte.append(pz); start = pz
    schnitte.append(dauer)
    hyp = ""
    for s0, s1 in zip(schnitte[:-1], schnitte[1:]):
        segs, _ = m.transcribe(a[int(s0 * 16000):int(s1 * 16000)], language="de", beam_size=5, condition_on_previous_text=False)
        hyp += " " + " ".join(s.text for s in segs)
    h = norm(hyp); sm = difflib.SequenceMatcher(None, soll, h, autojunk=False)
    abw = [f"{soll[max(0,i1-14):i1]}[{soll[i1:i2]}→{h[j1:j2]}]" for op, i1, i2, j1, j2 in sm.get_opcodes() if op != "equal"]
    print(f.rsplit("/", 1)[-1], sys.argv[1], "| Stücke", len(schnitte) - 1, "|", "wortgetreu" if not abw else abw)
