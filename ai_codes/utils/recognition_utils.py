import speech_recognition as sr
import datetime

def recognize_from_virtual_mic(mic, save_debug_wav=False):
    recognizer = sr.Recognizer()
    with mic as source:
        print("Zoom経由の音声を認識中...")
        recognizer.adjust_for_ambient_noise(source, duration=3)
        audio = recognizer.listen(source, timeout=None, phrase_time_limit=15)
    if save_debug_wav:
        ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        wav_path = f"debug_audio_{ts}.wav"
        with open(wav_path, "wb") as f:
            f.write(audio.get_wav_data())
        print(f"録音音声を {wav_path} に保存しました。")
    try:
        text = recognizer.recognize_google(audio, language="ja-JP")
        print("認識結果:", text)
        return text
    except Exception as e:
        print("認識失敗:", e)
        return ""
