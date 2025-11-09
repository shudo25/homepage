from objects.Assistant import Assistant

if __name__ == "__main__":
    assistant = Assistant()
    print("ささら進行アシスタントとチャットできます。'exit'で終了。\n")
    while True:
        user_input = input("あなた: ")
        if user_input.strip().lower() in ["exit", "quit", "bye", "終了"]:
            print("ささら: ありがとうございました！またお話ししましょう。")
            break
        response = assistant.ask(user_input)
        print(f"ささら: {response}\n")
        # 発声サンプル（ON/OFFやTTS切替はここで制御可能）
        assistant.speak(response)
