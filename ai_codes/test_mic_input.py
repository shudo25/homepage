import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav

# デバイスインデックスを環境に合わせて設定
VIRTUAL_MIC_INDEX = 34  # 例: Voicemeeter Out B1
SAMPLERATE = 16000
DURATION = 5  # 秒

print(f"{DURATION}秒間録音して test_output.wav に保存します。Zoom等から音を出してテストしてください。")
print("録音開始...")
audio = sd.rec(int(DURATION * SAMPLERATE), samplerate=SAMPLERATE, channels=1, dtype='int16', device=VIRTUAL_MIC_INDEX)
sd.wait()
print("録音終了。")

# WAVファイルとして保存
wav.write("test_output.wav", SAMPLERATE, audio)
print("test_output.wav に保存しました。再生して音が入っているか確認してください。")
