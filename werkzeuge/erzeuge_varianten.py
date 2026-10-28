"""Varianten einer Stimme bei ElevenLabs erzeugen (Modell/Stability-Vergleich). Aufruf: erzeuge_varianten.py <text> <ausordner>
Kostet Credits (Absatz 1–2 aus Teil 1, 785 Zeichen: laut API 337 je Anfrage). Schon vorhandene Dateien werden übersprungen."""
import json, os, sys, urllib.request, urllib.error
key = os.environ["ELEVENLABS_API_KEY"]
RALF, LUPERT = "jJxw1Rvgr2c60UdJHPBn", "xoLW9SizYThZnEEVer1q"
VARIANTEN = {
    "ralf_v4_stab10": (RALF, {"model_id": "eleven_v4", "voice_settings": {"stability": 1.0, "similarity_boost": 0.81}}),
    "ralf_v2_stab075": (RALF, {"model_id": "eleven_multilingual_v2", "voice_settings": {"stability": 0.75, "similarity_boost": 0.8, "style": 0.0, "use_speaker_boost": True}}),
    "ralf_storytel": (RALF, {"model_id": "eleven_storytel_v2", "voice_settings": {"stability": 0.75, "similarity_boost": 0.8}}),
    "lupert_v4_wie0523": (LUPERT, {"model_id": "eleven_v4", "voice_settings": {"stability": 0.5}}),
    "lupert_v2_stab075": (LUPERT, {"model_id": "eleven_multilingual_v2", "voice_settings": {"stability": 0.75, "similarity_boost": 0.8, "style": 0.0, "use_speaker_boost": True}}),
}
text, aus = open(sys.argv[1], encoding="utf-8").read(), sys.argv[2]
os.makedirs(aus, exist_ok=True)
for name, (voice, body) in VARIANTEN.items():
    ziel = f"{aus}/{name}.mp3"
    if os.path.exists(ziel): continue
    req = urllib.request.Request(f"https://api.elevenlabs.io/v1/text-to-speech/{voice}?output_format=mp3_44100_128",
        data=json.dumps({"text": text, **body}).encode(), headers={"xi-api-key": key, "Content-Type": "application/json"})
    try:
        r = urllib.request.urlopen(req, timeout=300); open(ziel, "wb").write(r.read()); print(name, "ok", flush=True)
    except urllib.error.HTTPError as e:
        print(name, "Fehler", e.code, e.read()[:300], flush=True)
