import sys
sys.path.insert(0, r'E:\GitHub\CeVIOPy')
import threading
from flask import Flask, request, jsonify
from characters.sasara_voice import get_tts_engine

app = Flask(__name__)
tts_engine = get_tts_engine()

@app.route('/speak', methods=['POST'])
def speak():
    data = request.get_json()
    text = data.get('text', '')
    if not text:
        return jsonify({'status': 'error', 'message': 'No text provided'}), 400
    threading.Thread(target=tts_engine.speak, args=(text,)).start()
    return jsonify({'status': 'ok'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5100)
