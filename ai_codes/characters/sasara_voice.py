# ささらの音声・Zoom環境設定
from ceviopy.cevio import Cevio
from utils.audio_utils import get_device_index_by_name
import speech_recognition as sr

# CeVIO TTSエンジン

def get_tts_engine():
    return Cevio(mode="AI")

# Zoom仮想マイクインデックス取得
_VIRTUAL_MIC_DEVICE_NAMES = {
    'B3': [
        "Voicemeeter Out B3 (VB-Audio Voicemeeter VAIO)",
        "Voicemeeter Out B3",
        "VoiceMeeter Output (VB-Audio VoiceMeeter VAIO3)",
        "VAIO3"
    ],
    # 他バスも追加可
}

def get_virtual_mic_index(bus='B3'):
    names = _VIRTUAL_MIC_DEVICE_NAMES.get(bus)
    if not names:
        raise ValueError(f"未対応のバス: {bus}")
    return get_device_index_by_name(names)

# マイクインスタンス生成

def get_microphone(bus='B3'):
    idx = get_virtual_mic_index(bus)
    return sr.Microphone(device_index=idx)
