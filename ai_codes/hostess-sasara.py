import os
import sys
sys.path.insert(0, r'E:\GitHub\CeVIOPy')
from ceviopy.cevio import Cevio
import speech_recognition as sr
import openai

client = openai.OpenAI(api_key=os.environ.get("HOSTESS_SASARA"))
print("OpenAI API Key:", "設定済み" if client.api_key else "未設定")

def recognize_google():
    recognizer = sr.Recognizer()
    mic = sr.Microphone()
    print("マイクからどうぞ（スピーチ開始の場合は「スピーチします」と言ってください）...")
    with mic as source:
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source, timeout=None, phrase_time_limit=30)  # 最大30秒など
    try:
        text = recognizer.recognize_google(audio, language="ja-JP")
        print("認識結果:", text)
        return text
    except Exception as e:
        print("認識失敗:", e)
        return ""

system_prompt = (
    "あなたはバーチャル司会者『さとうささら』です。\n"
    "公式な『さとうささら』のプロフィールには、次のように紹介されています。\n"
    "・アニメやゲームが好きな、ごくごく普通の女の子。\n"
    "・明るく前向き、ちょっと天然。\n"
    "・相手の話をよく聞き、前向きなリアクションを返します。\n"
    "・丁寧語を使い、時々かわいらしい表現を交えます。\n"
    "・本気なのかフリなのか分からないボケをかましては手痛いツッコミを頂戴している。\n"
    "・真面目に頑張っていたり、いじられすぎてたまに拗ねたりする。\n"
    "・応援してくれる人たちのために、今日も精一杯頑張る。\n"
    "・年齢：16歳\n"
    "・誕生日：1月22日\n"
    "・身長：160センチにちょっと足りないくらい\n"
    "・体重：乙女のヒミツ\n"
    "・好きな食べ物：もんじゃ焼き、アイス\n"
    "上記に加えて以下の点を優先して考慮してください。\n"
    "・一人称は「わたし」です。\n"
    "・明るく元気で親しみやすい性格です。\n"
    "・相手の話をよく聞き、前向きなリアクションを返します。\n"
    "・丁寧語を使い、時々かわいらしい表現を交えます。\n"
    "・場を盛り上げるため、ちょっとした合いの手や励ましも入れます。\n"
    "・冗談や軽いツッコミも交えて、楽しい雰囲気を作ります。\n"
    "・質問された場合、必ずしも正確に応答する必要はなく、柔軟に簡潔な対応をします。\n"
    "・語尾は「だよ」ではなく「です」をよく使います。\n"
)

def chatgpt_response(messages):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages,
        max_tokens=300,
        temperature=0.7,
    )
    return response.choices[0].message.content.strip()

def main():
    t = Cevio(mode="AI")

    with open("speakers.txt", "r", encoding="utf-8") as f:
        speakers = [line.strip() for line in f if line.strip()]

    for idx, name in enumerate(speakers, 1):
        t.speak(f"{idx}番、{name}さん、スピーチの前に一言どうぞ。スピーチを始める場合は「スピーチします」と言ってください。")
        print(f"--- {name}さんとの対話開始 ---")
        # スピーカーごとにmessages履歴を初期化
        messages = [{"role": "system", "content": system_prompt}]
        while True:
            user_text = recognize_google()
            if not user_text:
                t.speak(f"{name}さん、うまく聞き取れませんでした。もう一度お願いします。")
                continue
            # スピーチ開始のキーワードで本番へ
            if any(kw in user_text for kw in ["スピーチ", "始めます", "話します"]):
                print("user_text:", user_text)
                t.speak(f"{name}さん、どうぞスピーチをお願いします！")
                break
            # それ以外は対話を継続
            messages.append({"role": "user", "content": user_text})
            reply = chatgpt_response(messages)
            messages.append({"role": "assistant", "content": reply})
            # print("司会botの応答:", reply)
            t.speak(reply)
        print(f"--- {name}さんのスピーチ中 ---")
        input("スピーチが終わったらEnterを押してください...")
        t.speak("ありがとうございました。")

    t.speak("全員のスピーチが終了しました。お疲れさまでした。")

if __name__ == "__main__":
    main()