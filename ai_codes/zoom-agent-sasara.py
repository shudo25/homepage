import sys
sys.path.insert(0, r'E:\GitHub\CeVIOPy')
import speech_recognition as sr
from characters.sasara_person import system_prompt, get_openai_client
from characters.sasara_voice import get_tts_engine, get_microphone
import os
from time import sleep

client = get_openai_client()

# CeVIO初期化
t = get_tts_engine()
# マイクインスタンス生成
mic = get_microphone('B3')

# utils配下からimport
from utils.recognition_utils import recognize_from_virtual_mic
from utils.openai_utils import chatgpt_response

def main():
    # 文脈説明を最初に与える
    context_info = "（例）あなたはZoom会議の司会者です。参加者はAさんとBさんです。今日はイベントの進行役をお願いします。"
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": context_info}
    ]
    # 文脈説明を音声で発話
    t.speak(context_info)
    sleep(0.5)
    # 通常の会話ループ
    while True:
        user_text = recognize_from_virtual_mic(mic, save_debug_wav=False)
        if not user_text:
            t.speak("うまく聞き取れませんでした。もう一度お願いします。")
            sleep(0.5)
            continue
        messages.append({"role": "user", "content": user_text})
        reply = chatgpt_response(client, messages)
        print("ささら応答:", reply)
        t.speak(reply)
        messages.append({"role": "assistant", "content": reply})

if __name__ == "__main__":
    main()