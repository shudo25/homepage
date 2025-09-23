import sys
import queue

# --- 設定 ---
recognizer_type = "google"  # "vosk" または "google"
model_path = r"E:\Vosk\vosk-model-small-ja-0.22"
samplerate = 16000
device = None  # デフォルトのマイク

import sounddevice as sd
import vosk
import json

q = queue.Queue()

def callback(indata, frames, time, status):
    if status:
        print(status, file=sys.stderr)
    q.put(bytes(indata))

def recognize_from_mic():
    print("モデルを読み込み中...")
    model = vosk.Model(model_path)
    recognizer = vosk.KaldiRecognizer(model, samplerate)
    with sd.RawInputStream(samplerate=samplerate, blocksize=8000, device=device, dtype='int16',
                            channels=1, callback=callback):
        print("マイクから話しかけてください...")
        while True:
            data = q.get()
            if recognizer.AcceptWaveform(data):
                result = recognizer.Result()
                text = json.loads(result).get("text", "")
                print("認識結果:", text)
                return text
            else:
                partial_result = recognizer.PartialResult()
                # print("部分認識結果:", json.loads(partial_result).get("partial", ""))
            # Ctrl+Cで終了
