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
from utils.recognition_utils import recognize_with_silence_detection
from utils.openai_utils import chatgpt_response


import threading
import queue
import webui_sasara

sasara_status = "listening"  # "listening"=黙って聞いている, "speaking"=応答中
last_heard_texts = []  # 最新3件まで
last_reply_texts = []  # 最新3件まで

def main():
    global sasara_status, last_heard_text, last_reply_text
    # 文脈説明を最初に与える
    context_info = "まず最初に、あなた自身（さとうささら）として一言だけ簡単に自己紹介してください。"
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": context_info}
    ]
    # LLMに自己紹介をさせて発話
    intro_reply = chatgpt_response(client, messages)
    print("ささら自己紹介:", intro_reply)
    t.speak(intro_reply)
    messages.append({"role": "assistant", "content": intro_reply})
    sleep(0.5)


    # 音声認識・WebUI指示を並行で待つためのキュー
    input_queue = queue.Queue()
    # WebUIにキューと状態・直近聞き取り内容を渡す
    webui_sasara.input_queue = input_queue
    webui_sasara.sasara_status = sasara_status
    webui_sasara.last_heard_texts = last_heard_texts
    webui_sasara.last_reply_texts = last_reply_texts
    # Flaskアプリをサブスレッドで起動
    threading.Thread(target=webui_sasara.app.run, kwargs={"debug": False, "port": 5000, "use_reloader": False}, daemon=True).start()

    def audio_thread():
        global sasara_status, last_heard_texts, last_reply_texts
        while True:
            sasara_status = "listening"
            webui_sasara.sasara_status = sasara_status
            user_text = recognize_with_silence_detection(mic, phrase_time_limit=3, max_silence_count=2, max_total_duration=30)
            if user_text:
                last_heard_texts.append(user_text)
                if len(last_heard_texts) > 3:
                    last_heard_texts[:] = last_heard_texts[-3:]
                webui_sasara.last_heard_texts = last_heard_texts
            input_queue.put(("audio", user_text))

    # スレッド開始（音声のみ）
    threading.Thread(target=audio_thread, daemon=True).start()

    # メインループ: 入力が来たら処理
    while True:
        src, user_text = input_queue.get()
        if not user_text:
            if src == "audio":
                print("[音声認識失敗] うまく聞き取れませんでした。")
            continue
        if src == "text":
            print(f"[テキスト指示] {user_text}")
        else:
            print(f"[音声入力] {user_text}")
        messages.append({"role": "user", "content": user_text})
        # 発言状態に遷移
        sasara_status = "speaking"
        webui_sasara.sasara_status = sasara_status
        reply = chatgpt_response(client, messages)
        print("ささら応答:", reply)
        last_reply_texts.append(reply)
        if len(last_reply_texts) > 3:
            last_reply_texts[:] = last_reply_texts[-3:]
        webui_sasara.last_reply_texts = last_reply_texts
        t.speak(reply)
        messages.append({"role": "assistant", "content": reply})
        # 応答後は黙って聞いている状態に戻す
        sasara_status = "listening"
        webui_sasara.sasara_status = sasara_status

if __name__ == "__main__":
    main()