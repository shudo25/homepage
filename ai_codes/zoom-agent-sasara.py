# --- 状態切り替えキーワード ---
to_speaking_keywords = ["ささらさんどうぞ", "ささらさん答えて", "ささらさん発言", "sasara speak"]
to_listening_keywords = ["ささらさんどうも", "ささらさんありがとう", "ささらさん終了", "sasara stop"]
# --- 会議設定 ---
meeting_config = {
    "title": "定例会議",
    "participants": ["ささら", "田中一郎", "鈴木花子"],
    "use_polite_speech": True  # 年配者向け敬語
}

import sys
sys.path.insert(0, r'E:\GitHub\CeVIOPy')
import speech_recognition as sr
from characters.sasara_person import get_system_prompt, get_openai_client
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

    # 会議設定をsystem_promptに反映
    polite_note = "。今回の会議参加者は年配の方が多いので、丁寧な言葉遣い（敬語）で話してください。" if meeting_config["use_polite_speech"] else ""
    participants_note = f"本会議の参加者: {', '.join(meeting_config['participants'])}。"
    dynamic_system_prompt = get_system_prompt() + "\n" + participants_note + polite_note

    # --- プロトコル理解確認ステップ ---
    from characters.sasara_person import admin_protocol_check_message
    # --- プロトコル内容をuserメッセージにも明示的に含める ---
    protocol_content = get_system_prompt()
    protocol_enforce_message = (
        admin_protocol_check_message +
        "\n\n【プロトコル原文】\n" + protocol_content +
        "\n必ず上記プロトコル（systemメッセージで与えたルール）に厳密に従ってください。"
    )
    check_messages = [
        {"role": "system", "content": dynamic_system_prompt},
        {"role": "user", "content": protocol_enforce_message}
    ]
    check_reply = chatgpt_response(client, check_messages)
    print("[プロトコル理解確認]", check_reply)

    # 通常の会話開始
    context_info = "まず最初に、あなた自身（さとうささら）として一言だけ簡単に自己紹介してください。"
    messages = [
        {"role": "system", "content": dynamic_system_prompt},
        {"role": "user", "content": context_info}
    ]
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
                if len(last_heard_texts) > 10:
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
        # 退出ボタン受信時はスクリプトを安全に終了
        if user_text.strip() == "退出":
            print("[システム] 退出指示を受信したため、スクリプトを終了します。")
            os._exit(0)
        if src == "text":
            print(f"[テキスト指示] {user_text}")
        else:
            print(f"[音声入力] {user_text}")
        messages.append({"role": "user", "content": user_text})
        # 明示的なキーワードで状態を切り替え
        if any(kw in user_text for kw in to_speaking_keywords):
            sasara_status = "speaking"
            webui_sasara.sasara_status = sasara_status
            print("[状態切替] → 応答中 (speaking)")
        elif any(kw in user_text for kw in to_listening_keywords):
            sasara_status = "listening"
            webui_sasara.sasara_status = sasara_status
            print("[状態切替] → 会議を聞いている (listening)")

        if sasara_status == "speaking":
            reply = chatgpt_response(client, messages)
            print("ささら応答:", reply)
            last_reply_texts.append(reply)
            if len(last_reply_texts) > 3:
                last_reply_texts[:] = last_reply_texts[-3:]
            webui_sasara.last_reply_texts = last_reply_texts
            # --- 『『ADMIN: ... 』』形式ならZoom発声せず管理者UIに転送 ---
            if reply.startswith("『『ADMIN:") and reply.endswith("』』"):
                print("[管理者介入要請] 管理者UIに転送:", reply)
                # 必要に応じてwebui_sasaraで専用リストに追加するなど拡張可
            else:
                t.speak(reply)
            messages.append({"role": "assistant", "content": reply})
            # 応答後は自動でlisteningに戻さない（明示指示でのみ切替）

if __name__ == "__main__":
    main()