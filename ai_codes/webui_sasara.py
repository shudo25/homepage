# Flaskによる最小限の指示入力Web UI
from flask import Flask, request, render_template_string, redirect, url_for
import queue

# メインプロセスと共有するためのキュー（zoom-agent-sasara.pyと同じものを使う想定）

input_queue = None  # 実際はmain側から渡す
sasara_status = "listening"  # "listening"=黙って聞いている, "speaking"=応答中
last_heard_texts = []

last_reply_texts = []
command_log = []  # 指示履歴
# 管理者用非公開交信メッセージ履歴
admin_msgs = []

app = Flask(__name__)

HTML = '''
<!doctype html>
<head>
<title>ささら指示入力</title>
<script>
// 入力欄にフォーカスがなく、かつテキスト選択中でなければ1秒ごと自動リロード
setInterval(function() {
    var input = document.getElementById('sasara_input');
    var sel = window.getSelection ? window.getSelection().toString() : '';
    if (input && document.activeElement !== input && !sel) {
        location.reload();
    }
}, 1000);
</script>
</head>
<h2>ささらさんへの指示</h2>
<div style="margin-bottom:1em;">
    <b>【ささらさんの状態】</b>
    <span style="color:{{ 'green' if status=='listening' else 'red' }};font-weight:bold;">
        {{ '会議を聞いている' if status=='listening' else '応答中' }}
    </span>
</div>
<div style="margin-bottom:1em;">
    {% if last_heard_texts %}
        <div style="background:#eef;padding:0.5em;margin-bottom:0.3em;">
            <b>直近の聞き取り内容:</b>
            <ul style="margin:0 0 0 1.2em;padding:0;">
                {% for txt in last_heard_texts[::-1] %}
                    <li style="font-size:90%">{{txt}}</li>
                {% endfor %}
            </ul>
        </div>
    {% endif %}
    {% if last_reply_texts %}
        <div style="background:#ffe;padding:0.5em;">
            <b>直近の応答内容:</b>
            <ul style="margin:0 0 0 1.2em;padding:0;">
                {% for txt in last_reply_texts[::-1] %}
                    <li style="font-size:90%">{{txt}}</li>
                {% endfor %}
            </ul>
        </div>
    {% endif %}
</div>
<form method=post style="margin-bottom:0.5em;">
    <input id="sasara_input" name=text size=60 autofocus>
    <input type=submit value="送信">
</form>
<form method=post style="display:inline;">
    <input type=hidden name=text value="ささらさん発言">
    <input type=submit value="ささらさん発言" style="background:#cfc;">
</form>
<form method=post style="display:inline;">
    <input type=hidden name=text value="ささらさん終了">
    <input type=submit value="ささらさん終了" style="background:#fcc;">
</form>
<form method=post style="display:inline;">
    <input type=hidden name=text value="参加終了">
    <input type=submit value="参加終了" style="background:#ccc;">
</form>
{% if msg %}<p style="color:green">送信しました: {{msg}}</p>{% endif %}
<hr>
<h4 style="color:#900;">管理者用 非公開交信</h4>
<div style="max-height:120px;overflow:auto;background:#fee;padding:0.5em;">
    {% for msg in admin_msgs[::-1] %}
        <div style="font-size:90%;color:#900;">{{msg}}</div>
    {% endfor %}
</div>
<h4>指示ログ</h4>
<div style="max-height:200px;overflow:auto;background:#f8f8f8;padding:0.5em;">
    {% for cmd in log %}
        <div style="font-size:90%;color:#333;">{{cmd}}</div>
    {% endfor %}
</div>
'''

@app.route('/', methods=['GET', 'POST'])
def index():
    global sasara_status, last_heard_texts, last_reply_texts, command_log, admin_msgs
    msg = None
    # 直近の応答内容から『『ADMIN: ... 』』形式を抽出してadmin_msgsに追加
    if last_reply_texts:
        last = last_reply_texts[-1]
        if isinstance(last, str) and last.startswith("『『ADMIN:") and last.endswith("』』"):
            if (not admin_msgs) or (admin_msgs and last != admin_msgs[-1]):
                admin_msgs.append(last)
                if len(admin_msgs) > 10:
                    admin_msgs = admin_msgs[-10:]
    if request.method == 'POST':
        text = request.form.get('text', '').strip()
        if text and input_queue is not None:
            input_queue.put(("text", text))
            command_log.append(text)
            # ログは最新20件まで
            if len(command_log) > 20:
                command_log = command_log[-20:]
        # Post/Redirect/Get: 送信後はGETでリダイレクト
        return redirect(url_for('index'))
    # 状態・直近聞き取り・直近応答・指示ログ・非公開交信をテンプレートに渡す
    return render_template_string(HTML, msg=msg, status=sasara_status, last_heard_texts=last_heard_texts, last_reply_texts=last_reply_texts, log=command_log, admin_msgs=admin_msgs)

if __name__ == '__main__':
    # テスト用: 単体で動かす場合はローカルキューを使う
    import threading
    import time
    input_queue = queue.Queue()
    def consumer():
        while True:
            src, text = input_queue.get()
            print(f"[WebUI] {src}: {text}")
    threading.Thread(target=consumer, daemon=True).start()
    app.run(debug=True, port=5000)
