"""Sprecher-Fingerabdruck (WeSpeaker ResNet34, VoxCeleb) für Audiodateien; Kosinus-Ähnlichkeit."""
import subprocess, numpy as np, onnxruntime as ort, kaldi_native_fbank as knf
M = "/tmp/claude-0/-home-user-seneca-audio/0f3890f6-5584-570a-ac34-74e78c131d3b/scratchpad/modell/resnet34.onnx"
sess = ort.InferenceSession(M, providers=["CPUExecutionProvider"])
EIN = sess.get_inputs()[0].name
def lade(f):
    pcm = subprocess.run(["ffmpeg", "-nostdin", "-loglevel", "error", "-i", f, "-ac", "1", "-ar", "16000", "-f", "s16le", "-"], capture_output=True, check=True).stdout
    return np.frombuffer(pcm, np.int16).astype(np.float32)
def fbank(x):
    o = knf.FbankOptions(); o.frame_opts.dither = 0.0; o.frame_opts.samp_freq = 16000; o.mel_opts.num_bins = 80
    fb = knf.OnlineFbank(o); fb.accept_waveform(16000, x.tolist()); fb.input_finished()
    F = np.stack([fb.get_frame(i) for i in range(fb.num_frames_ready)]); return F - F.mean(0)
def emb(f):
    x = lade(f); F = fbank(x)[None].astype(np.float32)
    e = sess.run(None, {EIN: F})[0][0]; return e / np.linalg.norm(e)
