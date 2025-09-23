import sys
sys.path.insert(0, r'E:\GitHub\CeVIOPy')
from os import read
from ceviopy.cevio import Cevio, CevioException
# from ReconizeVosk import recognize_from_mic as recognize_vosk
from ReconizeGoogle import recognize_from_mic as recognize_google

def main():
    """
    サンプルテキスト
    cevio.pyをそのまま実行するとサンプルテキストを再生します(さとうささらボイスのみ対応)
    """
    t = Cevio(mode="AI")
    # さとうささらのトークを利用されている方のみ、次行のサンプルを利用可能です。
    # t.make_speech_mode()
    print(t.get_talk_params())
    print(t.get_cast_params())

    text = recognize_google()
    print("認識結果:", text)
    t.speak(text)

if __name__ == "__main__":
    main()
