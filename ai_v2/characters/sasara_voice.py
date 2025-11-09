# CeVIO TTSエンジン
class CevioDummy:
    def speak(self, text):
        print(f"CeVIOが発声: {text}")

def get_tts_engine():
    try:
        from ceviopy.cevio import Cevio
        return Cevio(mode="AI")
    except ImportError:
        print("CeVIO Pyがインストールされていません。TTSエンジンを利用できません。")
        return CevioDummy()