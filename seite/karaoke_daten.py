"""Wortzeiten je Hörfassung: Whisper-Zeitstempel auf den korrekten Text legen (Karaoke-Daten für die Hörseite)."""
import json, re, difflib, subprocess, numpy as np
from faster_whisper import WhisperModel
H = "/tmp/claude-0/-home-user/0523a428-572b-5d43-9560-e7907758c764/scratchpad/hoerproben"
R = "/home/user/fragen-allgemein/audio"
V2 = f"{R}/seneca_kap1/seneca_kap1_text.txt"; V1 = f"{H}/text_v1.txt"
DATEIEN = {
  "a-neufassung": (f"{R}/seneca_neufassung/seneca_neufassung_bestof.mp3", f"{R}/seneca_neufassung/text.txt"),
  "a-neufassung2": (f"{R}/seneca_neufassung_v2/seneca_neufassung_v2_bestof.mp3", f"{R}/seneca_neufassung_v2/text.txt"),
  "a-eleven_christian": (f"{R}/seneca_neufassung_v2/elevenlabs/christian_eleven_v4.mp3", f"{R}/seneca_neufassung_v2/elevenlabs/text_absatz1-2.txt"),
  "a-eleven_robert": (f"{R}/seneca_neufassung_v2/elevenlabs/robert_ranger_eleven_v4.mp3", f"{R}/seneca_neufassung_v2/elevenlabs/text_absatz1-2.txt"),
  "a-lupert_exp": ("/tmp/claude-0/-home-user/0523a428-572b-5d43-9560-e7907758c764/scratchpad/lupert2/lupert_exp.mp3", f"{R}/seneca_neufassung_v2/text.txt"),
  "a-v-lupert": ("/tmp/claude-0/-home-user/0523a428-572b-5d43-9560-e7907758c764/scratchpad/stimmen/lupert.mp3", "/tmp/claude-0/-home-user/0523a428-572b-5d43-9560-e7907758c764/scratchpad/stimmen/text_absatz12.txt"),
  "a-v-christian": ("/tmp/claude-0/-home-user/0523a428-572b-5d43-9560-e7907758c764/scratchpad/stimmen/christian_12.mp3", "/tmp/claude-0/-home-user/0523a428-572b-5d43-9560-e7907758c764/scratchpad/stimmen/text_absatz12.txt"),
  "a-v-brian": ("/tmp/claude-0/-home-user/0523a428-572b-5d43-9560-e7907758c764/scratchpad/stimmen/brian.mp3", "/tmp/claude-0/-home-user/0523a428-572b-5d43-9560-e7907758c764/scratchpad/stimmen/text_absatz12.txt"),
  "a-v-ralf": ("/tmp/claude-0/-home-user/0523a428-572b-5d43-9560-e7907758c764/scratchpad/stimmen/ralf.mp3", "/tmp/claude-0/-home-user/0523a428-572b-5d43-9560-e7907758c764/scratchpad/stimmen/text_absatz12.txt"),
  "a-v-robert": ("/tmp/claude-0/-home-user/0523a428-572b-5d43-9560-e7907758c764/scratchpad/stimmen/robert.mp3", "/tmp/claude-0/-home-user/0523a428-572b-5d43-9560-e7907758c764/scratchpad/stimmen/text_absatz12.txt"),
  "a-teil02": ("/tmp/claude-0/-home-user/0523a428-572b-5d43-9560-e7907758c764/scratchpad/teil02/teil02b_ruhig.mp3", "/home/user/seneca-audio/texte/teil02.txt"),
  "a-lupert_ruhig": ("/tmp/claude-0/-home-user/0523a428-572b-5d43-9560-e7907758c764/scratchpad/lupert2/lupert_ruhig.mp3", f"{R}/seneca_neufassung_v2/text.txt"),
  "a-lupert_exp_pausen": ("/tmp/claude-0/-home-user/0523a428-572b-5d43-9560-e7907758c764/scratchpad/lupert2/lupert_exp_pausen.mp3", f"{R}/seneca_neufassung_v2/text.txt"),
  "a-eleven_ganz": (f"{R}/seneca_neufassung_v2/elevenlabs/christian_eleven_v4_ganz.mp3", f"{R}/seneca_neufassung_v2/text.txt"),
  "a-neufassung_v1": (f"{R}/seneca_neufassung/seneca_neufassung_bestof_v1.mp3", f"{R}/seneca_neufassung/text.txt"),
  "a-buch": (f"{R}/seneca_kap1/seneca_kap1_bestof.mp3", V2),
  "a-fenrir_1": (f"{R}/seneca_kap1/routellm_gemini25pro_onyx.mp3", V1),
  "a-edge_katja": ("/tmp/claude-0/-home-user/0523a428-572b-5d43-9560-e7907758c764/scratchpad/audio/pruef/seneca_edge_katja_v2.mp3", V2),
  "a-gpt_onyx": (f"{R}/seneca_kap1/routellm_gptaudio15_onyx.mp3", V1),
  "a-fenrir_3": (f"{R}/seneca_kap1/routellm_gemini25pro_onyx_v3.mp3", V2),
}
norm = lambda w: re.sub(r"[^a-zäöü0-9]", "", w.lower().replace("ß", "ss"))
m = WhisperModel("large-v3-turbo", device="cpu", compute_type="int8", cpu_threads=4)
import sys, os
if len(sys.argv) > 1 and sys.argv[1] == '--einzeln':
    DATEIEN = {'x': (sys.argv[2], sys.argv[3])}; AUS = sys.argv[4]; NUR = ['x']
else:
    AUS = None; NUR = sys.argv[1:]
out = json.load(open(f"{H}/karaoke.json", encoding="utf-8")) if (NUR and not AUS and os.path.exists(f"{H}/karaoke.json")) else {}
for aid, (mp3, txt) in DATEIEN.items():
    if NUR and aid not in NUR: continue
    pcm = subprocess.run(["ffmpeg", "-loglevel", "error", "-i", mp3, "-ac", "1", "-ar", "16000", "-f", "s16le", "-"], capture_output=True, check=True).stdout
    a = np.frombuffer(pcm, np.int16).astype(np.float32) / 32768; dauer = len(a) / 16000
    # In Stücke ≤ 25 s an Sprechpausen schneiden: Whisper überspringt in langen Dateien sonst ganze Passagen
    fr = a[: len(a) // 160 * 160].reshape(-1, 160).astype(np.float64); db = 10 * np.log10((fr ** 2).mean(1) + 1e-12)
    still = db < max(np.percentile(db, 95) - 35, np.percentile(db, 10) + 6)
    pausen, k = [], 0
    while k < len(still):
        if still[k]:
            j = k
            while j < len(still) and still[j]: j += 1
            if (j - k) * 0.01 >= 0.35: pausen.append((k + j) / 2 * 0.01)
            k = j
        else: k += 1
    schnitte, start = [0.0], 0.0
    for i, pz in enumerate(pausen):
        naechste = pausen[i + 1] if i + 1 < len(pausen) else dauer
        if naechste - start > 25 and pz - start > 3: schnitte.append(pz); start = pz
    schnitte.append(dauer)
    hyp = []
    for s0, s1 in zip(schnitte[:-1], schnitte[1:]):
        segs, _ = m.transcribe(a[int(s0 * 16000):int(s1 * 16000)], language="de", beam_size=5, word_timestamps=True, condition_on_previous_text=False, vad_filter=False)
        hyp += [(norm(x.word), s0 + x.start, s0 + x.end) for s in segs for x in s.words if norm(x.word)]
    # Anzeige-Wörter aus dem Text; Satzzeichen-Tokens („–“) an das vorige Wort hängen; Absatzgrenzen merken
    disp, absatz = [], []
    for pi, para in enumerate(open(txt, encoding="utf-8").read().strip().split("\n\n")):
        for tok in para.split():
            if not norm(tok) and disp: disp[-1] += " " + tok
            else: disp.append(tok); absatz.append(pi)
    ref = [norm(t) for t in disp]
    st = [None] * len(ref); en = [None] * len(ref)
    sm = difflib.SequenceMatcher(None, ref, [h[0] for h in hyp], autojunk=False)
    treffer = 0
    for op, i1, i2, j1, j2 in sm.get_opcodes():
        if op == "equal" or (op == "replace" and i2 - i1 == j2 - j1):
            for k in range(i2 - i1): st[i1 + k], en[i1 + k] = hyp[j1 + k][1], hyp[j1 + k][2]
            treffer += (i2 - i1) if op == "equal" else 0
        elif op == "replace" and j2 > j1:     # ungleich lang („um so“/„umso“): Zeitspanne nach Zeichenzahl verteilen
            t0, t1 = hyp[j1][1], hyp[j2 - 1][2]; L = [max(1, len(ref[i])) for i in range(i1, i2)]; c = t0
            for k, i in enumerate(range(i1, i2)): st[i] = c; c += (t1 - t0) * L[k] / sum(L); en[i] = c
    # Lücken (nicht erkannte Wörter) zwischen Nachbarn nach Zeichenzahl auffüllen
    i = 0
    while i < len(ref):
        if st[i] is None:
            j = i
            while j < len(ref) and st[j] is None: j += 1
            t0 = en[i - 1] if i > 0 else 0.0; t1 = st[j] if j < len(ref) else dauer
            L = [max(1, len(ref[k])) for k in range(i, j)]; c = t0
            for k in range(i, j): st[k] = c; c += (t1 - t0) * L[k - i] / sum(L); en[k] = c
            i = j
        else: i += 1
    out[aid] = {"w": disp, "t": [round(x, 2) for x in st], "p": absatz, "ende": round(dauer, 2)}
    print(f"{aid:14} {len(schnitte)-1} Stücke, {len(disp)} Wörter, {treffer} exakt getroffen ({treffer/len(disp):.0%}), erkannt {len(hyp)}, Dauer {dauer:.1f} s", flush=True)
if AUS:
    d = out["x"]; t = d["t"] + [d["ende"]]
    json.dump([{"w": d["w"][i], "s": t[i], "e": min(t[i+1], t[i] + 1.2)} for i in range(len(d["w"])) if t[i] < 100], open(AUS, "w"), ensure_ascii=False)
else:
    json.dump(out, open(f"{H}/karaoke.json", "w", encoding="utf-8"), ensure_ascii=False)
