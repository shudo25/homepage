import sys

import speech_recognition as sr

def recognize_from_mic():
    recognizer = sr.Recognizer()
    mic = sr.Microphone()
    print("マイクから話しかけてください...")
    with mic as source:
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
    try:
        text = recognizer.recognize_google(audio, language="ja-JP")
        print("認識結果:", text)
    except Exception as e:
        print("認識失敗:", e)
    return text

if __name__ == "__main__":
    recognize_from_mic()