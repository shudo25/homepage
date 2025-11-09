# CeVIO TTSエンジンラッパー
class CevioTTS:
    def __init__(self):
        try:
            from ceviopy.cevio import Cevio
            self.engine = Cevio(mode="AI")
        except ImportError:
            print("CeVIO Pyがインストールされていません。TTSエンジンを利用できません。ダミーで動作します。")
            self.engine = None

    def speak(self, text: str):
        if self.engine:
            self.engine.speak(text)
        else:
            print(f"[CeVIO Dummy] {text}")
