# Voskによる音声認識関数
# ファイル名: recognition_utils_vosk.py

def recognize_from_virtual_mic_vosk(mic, model_path=None, save_debug_wav=False, duration=10):
    """
    Voskを使ってマイク入力から日本語音声認識を行う関数。
    mic: speech_recognition.Microphone インスタンス
    model_path: Voskモデルのディレクトリパス（省略時はデフォルト）
    save_debug_wav: Trueで録音音声をwav保存
    duration: 録音秒数（デフォルト10秒）
    """
    import wave
    from vosk import Model, KaldiRecognizer
    import speech_recognition as sr
    import datetime

    _VOSK_DEFAULT_MODEL_PATH = "e:/GitHub/homepage/ai_codes/models/vosk-model-small-ja-0.22"
    if model_path is None:
        model_path = _VOSK_DEFAULT_MODEL_PATH

    recognizer = sr.Recognizer()
    with mic as source:
        print("Vosk: Zoom経由の音声を認識中...（最大{}秒）".format(duration))
        audio = recognizer.listen(source, timeout=None, phrase_time_limit=duration)

    if save_debug_wav:
        ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        wav_path = f"debug_audio_vosk_{ts}.wav"
        with open(wav_path, "wb") as f:
            f.write(audio.get_wav_data())
        print(f"録音音声を {wav_path} に保存しました。")

    # Voskモデルのロード
    model = Model(model_path)
    rec = KaldiRecognizer(model, audio.sample_rate)

    # 音声データをVoskに渡す
    wav_data = audio.get_raw_data()
    if rec.AcceptWaveform(wav_data):
        result = rec.Result()
    else:
        result = rec.FinalResult()

    import json
    try:
        text = json.loads(result).get("text", "")
        print("Vosk認識結果:", text)
        return text
    except Exception as e:
        print("Vosk認識失敗:", e)
        return ""
