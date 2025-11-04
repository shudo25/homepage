# Flaskによる最小限の指示入力Web UI
from flask import Flask, request, render_template_string, redirect, url_for
from flask_socketio import SocketIO, emit
import queue

# メインプロセスと共有するためのキュー（zoom-agent-sasara.pyと同じものを使う想定）

input_queue = None  # 実際はmain側から渡す
sasara_status = "listening"  # "listening"=黙って聞いている, "speaking"=応答中
last_heard_texts = []
temp_asr_texts = []  # デバッグ音声入力など一時的な音声認識結果履歴

last_reply_texts = []
command_log = []  # 指示履歴


app = Flask(__name__)
socketio = SocketIO(app)

HTML = '''
<!doctype html>
<head>
<title>ささら指示入力</title>
<script src="https://cdn.socket.io/4.7.5/socket.io.min.js"></script>
<script>
var socket = io();
socket.on('asr_update', function(data) {
    var textarea = document.querySelector('textarea[name="edited_text"]');
    if (textarea && document.activeElement !== textarea) {
        textarea.value = data.text;
    }
});
function clearAsr() {
    socket.emit('clear_asr');
    // textareaも即時クリア
    var textarea = document.querySelector('textarea[name="edited_text"]');
    if (textarea) textarea.value = '';
    return false;
}
</script>
</head>
<style>
.container-flex {
    display: flex;
    flex-direction: row;
    gap: 2em;
    align-items: flex-start;
}
.left-col, .right-col {
    flex: 1 1 0;
    min-width: 320px;
}
.block {
    margin-bottom: 1.2em;
    background: #f8f8f8;
    padding: 0.8em;
    border-radius: 6px;
}
.block-title { font-weight: bold; margin-bottom: 0.3em; }
</style>
<div class="container-flex">
    <div class="left-col">
        <div class="block" style="background:#e0ffe0;">
            <span class="block-title">ささらに直接発声させる:</span><br>
            <form method="post" style="margin-bottom:0.5em; display:block;">
                <textarea name="direct_tts" rows="10" cols="48" style="width:100%;max-width:100%;box-sizing:border-box;" placeholder="この内容をAIを介さず即発声"></textarea>
                <input type="submit" value="直接発声" style="background:#bff;min-width:120px;margin-top:0.5em;">
            </form>
        </div>
        <div class="block" style="background:#eef;">
            <span class="block-title">デバッグ用音声入力:</span><br>
            <form method="post" style="display:inline;">
                <input type="text" name="debug_audio" size="40" placeholder="ここにテキストを入力し送信するとマイク入力扱いになります">
                <input type="submit" value="デバッグ音声送信" style="background:#cce;">
            </form>
        </div>
        <div class="block" style="background:#ffd;">
            <span class="block-title">音声認識結果（編集して送信可）:</span><br>
            <form method="post" style="margin-bottom:0.5em; display:block;">
                <textarea name="edited_text" rows="14" cols="48" style="width:100%;max-width:100%;box-sizing:border-box;">{% if last_heard_texts %}{{ last_heard_texts[-1] }}{% elif temp_asr_texts %}{{ temp_asr_texts|join('\n') }}{% endif %}</textarea><br>
                <div style="margin-top:0.5em; display:flex; gap:0.7em;">
                    <input type="submit" value="編集内容をささらに送信" style="background:#eef;flex:1;min-width:120px;">
                    <button onclick="return clearAsr();" style="background:#fcc;flex:1;min-width:120px;">音声認識結果クリア</button>
                </div>
            </form>
        </div>
        <div class="block">
            <form method=post style="display:inline;">
                <input type=hidden name=text value="ささらさん発言">
                <input type=submit value="ささらさん発言" style="background:#cfc;">
            </form>
            <form method=post style="display:inline;">
                <input type=hidden name=text value="ささらさん終了">
                <input type=submit value="ささらさん終了" style="background:#fcc;">
            </form>
            <form method=post style="display:inline;">
                <input type=hidden name=text value="退出">
                <input type=submit value="退出" style="background:#ccc;">
            </form>
            {% if msg %}<p style="color:green">送信しました: {{msg}}</p>{% endif %}
        </div>
        <div class="block">
            <span class="block-title">指示ログ</span>
            <ul style="max-height:120px;overflow:auto;background:#f8f8f8;padding:0.5em;font-size:90%;color:#333;list-style-type:disc;margin:0 0 1em 1.2em;">
                {% for cmd in log %}
                    <li>{{cmd}}</li>
                {% endfor %}
            </ul>
        </div>
    </div>
    <div class="right-col">
        <div class="block" style="background:#eef;">
            <span class="block-title">直近の聞き取り内容:</span>
            <div style="max-height:200px;overflow:auto;overflow-x:auto;white-space:pre;">
                {% for txt in last_heard_texts[::-1] %}
                    <div style="font-size:90%;white-space:pre;">{{txt}}</div>
                {% endfor %}
            </div>
        </div>
        {% if last_reply_texts %}
        <div class="block" style="background:#ffe;">
            <span class="block-title">直近の応答内容:</span>
            <ul style="margin:0 0 0 1.2em;padding:0;">
                {% for txt in last_reply_texts[::-1] %}
                    <li style="font-size:90%">{{txt}}</li>
                {% endfor %}
            </ul>
        </div>
        {% endif %}
        <div class="block">
            <span class="block-title">【ささらさんの状態】</span><br>
            <span style="color:{{ 'green' if status=='listening' else 'red' }};font-weight:bold;">
                {{ '会議を聞いている' if status=='listening' else '応答中' }}
            </span>
        </div>
    </div>
</div>
'''

@app.route('/', methods=['GET', 'POST'])
def index():
    global sasara_status, last_heard_texts, last_reply_texts, command_log, temp_asr_texts
    msg = None
    if request.method == 'POST':
        edited_text = request.form.get('edited_text', '').strip()
        text = request.form.get('text', '').strip()
        debug_audio = request.form.get('debug_audio', '').strip()
        direct_tts = request.form.get('direct_tts', '').strip()
        sent = False
        if direct_tts:
            if input_queue is not None:
                input_queue.put(("direct_tts", direct_tts))
                # ログに記録（任意）
                command_log.append("[直接発声] " + direct_tts)
                if len(command_log) > 20:
                    command_log = command_log[-20:]
                sent = True
            return redirect(url_for('index'))
        if debug_audio:
            # デバッグ用音声入力はtemp_asr_textsに履歴として保存
            temp_asr_texts.append(debug_audio)
            if len(temp_asr_texts) > 10:
                temp_asr_texts[:] = temp_asr_texts[-3:]
            push_asr_update(debug_audio)
            # 指示ログ、input_queue、last_heard_textsには追加しない
            return redirect(url_for('index'))
        if edited_text:
            if input_queue is not None:
                input_queue.put(("text", edited_text))
                # 指示ログには追加しない
                # 送信内容を履歴として追加
                last_heard_texts.append(edited_text)
                temp_asr_texts.clear()
                sent = True
        elif text:
            if input_queue is not None:
                input_queue.put(("text", text))
                # 指示ボタンからの指示のみログに追加
                if text in ("ささらさん発言", "ささらさん終了", "退出"):
                    command_log.append(text)
                    if len(command_log) > 20:
                        command_log = command_log[-20:]
                sent = True
        return redirect(url_for('index'))
    # WebSocketイベントでクリア要求を受ける
    @socketio.on('clear_asr')
    def handle_clear_asr():
        global temp_asr_texts
        temp_asr_texts.clear()
        push_asr_update("")
    return render_template_string(HTML, msg=msg, status=sasara_status, last_heard_texts=last_heard_texts, last_reply_texts=last_reply_texts, log=command_log, temp_asr_texts=temp_asr_texts)

# 音声認識結果を即時pushする関数例
def push_asr_update(new_text):
    socketio.emit('asr_update', {'text': new_text})

if __name__ == '__main__':
    # テスト用: 単体で動かす場合はローカルキューを使う
    import threading
    import time
    input_queue = queue.Queue()
    def consumer():
        global last_heard_texts
        while True:
            src, text = input_queue.get()
            print(f"[WebUI] {src}: {text}")
            if src in ("asr", "audio"):
                # last_heard_texts[-1]を上書き、空なら追加
                if last_heard_texts:
                    last_heard_texts[-1] = text
                else:
                    last_heard_texts.append(text)
                print("emit asr_update", text)
                push_asr_update(text)
    threading.Thread(target=consumer, daemon=True).start()
    socketio.run(app, debug=True, port=5000)
