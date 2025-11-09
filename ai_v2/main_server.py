import subprocess
import sys
import time
import os

# TTSサーバの起動
TTS_SERVER_PATH = os.path.join(os.path.dirname(__file__), 'tts_server.py')
tts_proc = subprocess.Popen([sys.executable, TTS_SERVER_PATH])

try:
    # TTSサーバの起動待ち（必要に応じて調整）
    time.sleep(2)
    # WebUIサーバの起動
    WEBUI_SERVER_PATH = os.path.join(os.path.dirname(__file__), 'webui_server.py')
    subprocess.run([sys.executable, WEBUI_SERVER_PATH])
finally:
    # WebUIサーバ終了時にTTSサーバも終了
    tts_proc.terminate()
    try:
        tts_proc.wait(timeout=5)
    except Exception:
        tts_proc.kill()
