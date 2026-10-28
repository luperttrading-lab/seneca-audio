"""Hörproben der Bibliothek laden, mit Whisper Wortzeiten holen (ohne Solltext), Prosodie messen."""
import json, os, sys, subprocess, urllib.request, numpy as np, traceback
from faster_whisper import WhisperModel
R = "/home/user/seneca-audio"
exec(open(f"{R}/werkzeuge/prosodie.py").read().split("W = sys.argv[1]")[0])
B = sys.argv[1]   # Ordner mit bibliothek.json; Proben landen in B/proben; alle = json.load(open(f"{B}/bibliothek.json"))
aus = f"{B}/screening.json"; erg = json.load(open(aus)) if os.path.exists(aus) else {}
wahl = [v for v in alle.values() if v.get("kalib") or (v.get("use_case") in ("narrative_story", "informative_educational")
        and v.get("descriptive") not in ("excited", "upbeat", "intense") and v.get("age") != "young")]
wahl.sort(key=lambda v: (not v.get("kalib"), -(v.get("usage_character_count_1y") or 0)))
print(len(wahl), "Stimmen", flush=True)
m = WhisperModel("large-v3-turbo", device="cpu", compute_type="int8", cpu_threads=4)
for i, v in enumerate(wahl):
    vid = v["voice_id"]
    if vid in erg or not v.get("preview_url"): continue
    p = f"{B}/proben/{vid}"
    try:
        if not os.path.exists(p + ".mp3"):
            urllib.request.urlretrieve(v["preview_url"], p + ".mp3")
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", p + ".mp3", "-ac", "1", "-ar", "16000", p + ".wav"], check=True)
        a = lade(p + ".wav").astype(np.float32)
        segs, info = m.transcribe(a, beam_size=5, word_timestamps=True, condition_on_previous_text=False)
        ws = [{"w": x.word.strip(), "s": x.start, "e": x.end} for s in segs for x in s.words if x.word.strip()]
        json.dump(ws, open(p + ".words.json", "w"), ensure_ascii=False)
        r = {"name": v["name"], "sprache": info.language, "sprache_p": info.language_probability, "dauer": len(a) / 16000,
             "woerter": len(ws), "text": " ".join(w["w"] for w in ws)[:300]}
        if len(ws) >= 15: r.update(merkmale(p + ".wav"))
        erg[vid] = r
        print(i, v["name"][:40], r["sprache"], round(r["dauer"], 1), round(r.get("Melodie-Spannweite HT", 0), 2), flush=True)
    except Exception as ex:
        erg[vid] = {"name": v["name"], "fehler": repr(ex)[:200]}; print(i, v["name"][:40], "Fehler", repr(ex)[:120], flush=True)
    json.dump(erg, open(aus, "w"), ensure_ascii=False, indent=1)
print("fertig", flush=True)
