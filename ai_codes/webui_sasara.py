# Flaskによる最小限の指示入力Web UI
from flask import Flask, request, render_template_string, redirect, url_for
from flask_socketio import SocketIO, emit
import queue

# メインプロセスと共有するためのキュー（zoom-agent-sasara.pyと同じものを使う想定）

input_queue = None  # 実際はmain側から渡す
sasara_status = "listening"  # "listening"=黙って聞いている, "speaking"=応答中
last_heard_texts = []

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
</script>
</head>
<h2>ささらさんへの指示</h2>
<div style="margin-bottom:1em;background:#eef;padding:0.5em;">
    <b>デバッグ用音声入力:</b>
    <form method="post" style="display:inline;">
        <input type="text" name="debug_audio" size="50" placeholder="ここにテキストを入力し送信するとマイク入力扱いになります">
        <input type="submit" value="デバッグ音声送信" style="background:#cce;">
    </form>
</div>
<div style="margin-bottom:1em;">
    <div style="background:#ffd;padding:0.5em;margin-bottom:0.3em;">
        <b>音声認識結果（編集して送信可）:</b><br>
        <form method="post" style="margin-bottom:0.5em;">
            <textarea name="edited_text" rows="2" cols="60">{% if last_heard_texts %}{{ last_heard_texts[-1] }}{% endif %}</textarea>
            <input type="submit" value="編集内容をささらに送信" style="background:#eef;">
        </form>
    </div>
</div>
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
<hr>
<h4>指示ログ</h4>
<div style="max-height:200px;overflow:auto;background:#f8f8f8;padding:0.5em;">
    {% for cmd in log %}
        <div style="font-size:90%;color:#333;">{{cmd}}</div>
    {% endfor %}
</div>
<div style="background:#eef;padding:0.5em;margin-top:1em;">
    <b>直近の聞き取り内容:</b>
    <ul style="margin:0 0 0 1.2em;padding:0;">
        {% for txt in last_heard_texts[::-1] %}
            <li style="font-size:90%">{{txt}}</li>
        {% endfor %}
    </ul>
</div>
{% if last_reply_texts %}
    <div style="background:#ffe;padding:0.5em;margin-top:1em;">
        <b>直近の応答内容:</b>
        <ul style="margin:0 0 0 1.2em;padding:0;">
            {% for txt in last_reply_texts[::-1] %}
                <li style="font-size:90%">{{txt}}</li>
            {% endfor %}
        </ul>
    </div>
{% endif %}
<div style="margin-top:1em;">
    <b>【ささらさんの状態】</b>
    <span style="color:{{ 'green' if status=='listening' else 'red' }};font-weight:bold;">
        {{ '会議を聞いている' if status=='listening' else '応答中' }}
    </span>
</div>
'''

@app.route('/', methods=['GET', 'POST'])
def index():
    global sasara_status, last_heard_texts, last_reply_texts, command_log
    msg = None
    if request.method == 'POST':
        edited_text = request.form.get('edited_text', '').strip()
        text = request.form.get('text', '').strip()
        debug_audio = request.form.get('debug_audio', '').strip()
        sent = False
        if debug_audio:
            # デバッグ用音声入力をマイク入力扱いでput
            if input_queue is not None:
                input_queue.put(("audio", debug_audio))
                command_log.append("[デバッグ音声] " + debug_audio)
                if len(command_log) > 20:
                    command_log = command_log[-20:]
                sent = True
            return redirect(url_for('index'))
        if edited_text:
            if input_queue is not None:
                input_queue.put(("text", edited_text))
                command_log.append("[編集送信] " + edited_text)
                if len(command_log) > 20:
                    command_log = command_log[-20:]
                sent = True
        elif text:
            if input_queue is not None:
                input_queue.put(("text", text))
                command_log.append(text)
                if len(command_log) > 20:
                    command_log = command_log[-20:]
                sent = True
        return redirect(url_for('index'))
    return render_template_string(HTML, msg=msg, status=sasara_status, last_heard_texts=last_heard_texts, last_reply_texts=last_reply_texts, log=command_log)

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
