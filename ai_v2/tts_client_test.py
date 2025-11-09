import requests

resp = requests.post("http://localhost:5100/speak", json={"text": "テスト発声です"})
print(resp.status_code, resp.text)

from objects.tts_client import TTSClient

tts = TTSClient()
tts.speak("TTSクライアント経由のテスト発声です")