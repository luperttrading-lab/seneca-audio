"""Gemeinsame Bausteine der Bearbeitungskette für Kapitel, Paragrafen und Sätze (kapitel.py, paragraf.py, satz.py)."""
import re, subprocess, sys
import numpy as np

STIMME, MODELL, TEMPO, SR = "JiW03c2Gt43XNUQAumRP", "eleven_v4", 0.96, 44100
RAUSCH = ("highpass=f=60,anlmdn=s=0.0007,agate=threshold=0.01:ratio=3:range=0.15:attack=5:release=200:knee=6:detection=rms,"
          "atrim=start_sample=353,apad=pad_len=353")   # anlmdn verzögert um 8 ms (353 Samples), hier ausgeglichen
PAUSEN = {".": 0.9, "absatz": 1.3, ":": 0.55, ";": 0.55, "–": 0.45, ",": 0.35,   # „ruhig“ wie Teil 1, aber an Kommas
          "komma_ab": 0.15}   # nur, wo die Stimme schon 0,15 s pausiert (sonst holpert der Schnitt, Nutzer 29.10.)
ff = lambda *a: subprocess.run(["ffmpeg", "-nostdin", "-y", "-loglevel", "error", *a], check=True)
py = lambda *a, **k: subprocess.run([sys.executable, *a], check=True, stdin=subprocess.DEVNULL, **k)

def lufs(f):
    o = subprocess.run(["ffmpeg", "-nostdin", "-hide_banner", "-i", f, "-af", "ebur128", "-f", "null", "-"], capture_output=True, text=True).stderr
    return float(re.findall(r"I:\s+(-?[\d.]+) LUFS", o)[-1])

def lade(f):
    return np.frombuffer(subprocess.run(["ffmpeg", "-nostdin", "-loglevel", "error", "-i", f, "-ac", "1", "-ar", str(SR), "-f", "s16le", "-"],
                                        capture_output=True, check=True).stdout, np.int16).astype(np.float64) / 32768

def sprache(x):   # Anfang und Ende der Sprache (Rahmen über Spitzenpegel − 45 dB)
    n = 441; db = 10 * np.log10((x[:len(x) // n * n].reshape(-1, n) ** 2).mean(1) + 1e-12); an = np.flatnonzero(db > db.max() - 45)
    return an[0] * n, (an[-1] + 1) * n

def pegel(y):   # typischer Pegel der Sprache (Median der lauten 10-ms-Rahmen)
    r = np.sqrt((y[:len(y) // 441 * 441].reshape(-1, 441) ** 2).mean(1)); return np.median(r[r > r.max() * 0.05])



pnorm = lambda t: re.sub(r"[^a-zäöü0-9]", "", re.sub(r"\bgall?io\b", "gallio", re.sub(r"\bdass\b", "das", t.lower().replace("ß", "ss"))))   # wie pruef.py

def abweichungen(zeile, woerter):   # Meldungen von pruef.py („…vor[soll→ist]“) → {Wortindex: gehörtes Wort}
    wn = [pnorm(w) for w in woerter]; start = np.cumsum([0] + [len(x) for x in wn])[:-1]; ganz = "".join(wn); erg = {}
    for teil in re.findall(r"'([^']*)'", zeile):
        vor, rest = teil.split("[", 1); soll, ist = rest.rstrip("]").split("→")
        pos = ganz.find(vor + soll)
        if pos < 0: continue
        pos += len(vor); i = int(np.flatnonzero(start <= pos)[-1]); off = pos - start[i]
        alt = erg.get(i, wn[i]); erg[i] = alt[:off] + ist + alt[off + len(soll):]
    return erg

def bestaetigt(kapitel, datei="texte/verhoerer.txt"):   # vom Nutzer als richtig gehörte Stellen, die Whisper anders hört
    import os
    pfad = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), datei)
    if not os.path.exists(pfad): return set()
    return {pnorm(z.split()[1]) for z in open(pfad, encoding="utf-8") if z.split("#")[0].split() and z.split()[0] == str(kapitel)}
