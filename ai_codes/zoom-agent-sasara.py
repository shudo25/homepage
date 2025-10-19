import sys
sys.path.insert(0, r'E:\GitHub\CeVIOPy')
import speech_recognition as sr
import openai
from ceviopy.cevio import Cevio
import os
from time import sleep

# OpenAI APIキー
client = openai.OpenAI(api_key=os.environ.get("ASSISTANT_SASARA"))

# CeVIO初期化
t = Cevio(mode="AI")

# 仮想マイクのデバイスインデックスを調べて指定
VIRTUAL_MIC_INDEX = 34 # Voicemeeter Out B1 (VB-Audio Voicemeeter VAIO)
mic = sr.Microphone(device_index=VIRTUAL_MIC_INDEX)  # ←ここを環境に合わせて設定

def recognize_from_virtual_mic():
    recognizer = sr.Recognizer()
    with mic as source:
        print("Zoom経由の音声を認識中...")
        recognizer.adjust_for_ambient_noise(source, duration=3)
        audio = recognizer.listen(source, timeout=None, phrase_time_limit=15)
    # デバッグ用に音声を保存
    import datetime
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

def chatgpt_response(messages):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages,
        max_tokens=300,
        temperature=0.7,
    )
    return response.choices[0].message.content.strip()

system_prompt = "あなたはバーチャル司会者『さとうささら』です。..."  # assistant-sasara.pyの内容を流用

def main():
    messages = [{"role": "system", "content": system_prompt}]
    while True:
        user_text = recognize_from_virtual_mic()
        if not user_text:
            t.speak("うまく聞き取れませんでした。もう一度お願いします。")
            sleep(0.5)
            continue
        messages.append({"role": "user", "content": user_text})
        reply = chatgpt_response(messages)
        print("ささら応答:", reply)
        t.speak(reply)
        messages.append({"role": "assistant", "content": reply})

if __name__ == "__main__":
    main()