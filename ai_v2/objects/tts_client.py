import requests

class TTSClient:
    def __init__(self, server_url='http://localhost:5100'):
        self.server_url = server_url

    def speak(self, text: str):
        try:
            resp = requests.post(f'{self.server_url}/speak', json={'text': text}, timeout=3)
            if resp.status_code == 200:
                return True
            else:
                print(f"[TTSClient] Error: {resp.text}")
                return False
        except Exception as e:
            print(f"[TTSClient] Exception: {e}")
            return False
