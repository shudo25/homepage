from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, emit
from objects.Assistant import Assistant
import threading

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

assistant = Assistant()
assistant.load_context()
import os
@socketio.on('save_context')
def handle_save_context():
    assistant.save_context()
    emit('context_saved', {'status': 'ok'})

@socketio.on('shutdown_server')
def handle_shutdown_server():
    assistant.save_context()
    emit('server_shutdown', {'status': 'ok'})
    # Flask-SocketIOのstopはイベントループによって異なるため、os._exitで強制終了
    os._exit(0)

tts_enabled = True  # 発声ON/OFFの状態

def synthesize_and_play(text):
    # ここにTTS合成＆再生処理を実装（例: subprocessで外部TTS呼び出し等）
    print(f"[TTS] {text}")
    assistant.speak(text)

@app.route('/')
def index():
    return render_template('chat.html')

@socketio.on('user_message')
def handle_user_message(data):
    user_input = data.get('message', '')
    direct_tts = data.get('direct_tts', False)
    global tts_enabled
    if direct_tts:
        # LLMを介さず直接発声
        emit('bot_message', {'message': user_input})
        if tts_enabled:
            threading.Thread(target=synthesize_and_play, args=(user_input,)).start()
        return
    # LLM応答
    response = assistant.ask(user_input)
    emit('bot_message', {'message': response})
    if tts_enabled:
        threading.Thread(target=synthesize_and_play, args=(response,)).start()

@socketio.on('toggle_tts')
def handle_toggle_tts(data):
    global tts_enabled
    tts_enabled = data.get('enabled', True)
    emit('tts_status', {'enabled': tts_enabled}, broadcast=True)

if __name__ == '__main__':
    try:
        socketio.run(app, host='0.0.0.0', port=5000, debug=True)
    finally:
        assistant.save_context()
