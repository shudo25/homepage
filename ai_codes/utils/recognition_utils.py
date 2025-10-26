import speech_recognition as sr
import datetime


# ノイズ調整フラグ（グローバル）
_need_noise_adjust = True

def recognize_from_virtual_mic(mic, save_debug_wav=False):
    global _need_noise_adjust
    recognizer = sr.Recognizer()
    with mic as source:
        print("Zoom経由の音声を認識中...")
        if _need_noise_adjust:
            print("ノイズ調整中...")
            recognizer.adjust_for_ambient_noise(source, duration=0.5)
            _need_noise_adjust = False
        audio = recognizer.listen(source, timeout=None, phrase_time_limit=30)
    if save_debug_wav:
        ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        wav_path = f"debug_audio_{ts}.wav"
        with open(wav_path, "wb") as f:
            f.write(audio.get_wav_data())
        print(f"録音音声を {wav_path} に保存しました。")
    try:
        text = recognizer.recognize_google(audio, language="ja-JP")
        print("認識結果:", text)
        # 成功時は次回ノイズ調整不要
        _need_noise_adjust = False
        return text
    except Exception as e:
        print("認識失敗:", e)
        # 失敗時は次回ノイズ調整を行う
        _need_noise_adjust = True
        return ""


# --- 短い認識＋無音判定で応答する関数 ---
def recognize_with_silence_detection(mic, phrase_time_limit=3, max_silence_count=2, save_debug_wav=False, max_total_duration=30):
    """
    短い認識を繰り返し、無音が一定回数続いたら発話終了とみなしてバッファ内容で応答する。
    mic: speech_recognition.Microphone インスタンス
    phrase_time_limit: 1回の認識の最大秒数
    max_silence_count: 無音（認識失敗）が何回続いたら終了とみなすか
    save_debug_wav: Trueで各認識音声を保存
    max_total_duration: 最大録音時間（秒）
    """
    import speech_recognition as sr
    import datetime
    recognizer = sr.Recognizer()
    buffer = []
    silence_count = 0
    start_time = datetime.datetime.now()
    total_duration = 0
    global _need_noise_adjust
    with mic as source:
        while total_duration < max_total_duration:
            if _need_noise_adjust:
                print("ノイズ調整中...")
                recognizer.adjust_for_ambient_noise(source, duration=0.5)
                _need_noise_adjust = False
            print(f"短い認識({phrase_time_limit}s)を開始...")
            try:
                audio = recognizer.listen(source, timeout=None, phrase_time_limit=phrase_time_limit)
            except Exception as e:
                print("listen失敗:", e)
                break
            if save_debug_wav:
                ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                wav_path = f"debug_audio_chunk_{ts}.wav"
                with open(wav_path, "wb") as f:
                    f.write(audio.get_wav_data())
                print(f"チャンク音声を {wav_path} に保存しました。")
            try:
                text = recognizer.recognize_google(audio, language="ja-JP")
                print("認識結果:", text)
                buffer.append(text)
                silence_count = 0
                _need_noise_adjust = False
            except Exception as e:
                print("認識失敗(無音/ノイズ):", e)
                silence_count += 1
                _need_noise_adjust = True
            total_duration = (datetime.datetime.now() - start_time).total_seconds()
            if silence_count >= max_silence_count:
                print(f"無音が{max_silence_count}回続いたので終了")
                break
    result = " ".join(buffer)
    print("最終認識結果:", result)
    return result
