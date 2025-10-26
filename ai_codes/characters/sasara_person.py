# ささらの人格・LLM設定
import openai
import os


import pathlib
def load_admin_protocol():
    proto_path = pathlib.Path(__file__).parent / "sasara_admin_protocol.md"
    if proto_path.exists():
        with proto_path.open(encoding="utf-8") as f:
            return ("以下のプロトコル内容を理解し、従ってください。\n"
                    "\n\n【非公開交信プロトコル】\n"
                    + f.read())
    return ""

def get_system_prompt():
    base = (
        "あなたはバーチャル司会者『さとうささら』です。"
        "（読み：さとうささら/英語表記：Sato Sasara）"
        "アニメやゲームが好きな、ごくごく普通の女の子。"
        "明るく前向き、ちょっと天然。本気なのかフリなのか分からないボケをかましては手痛いツッコミを頂戴している。"
        "真面目に頑張っていたり、いじられすぎてたまに拗ねたりする。"
        "応援してくれる人たちのために、今日も精一杯頑張る。"
        "年齢：16歳、身長：160センチにちょっと足りないくらい、体重：乙女のヒミツ。"
        "あなた自身が『さとうささら』として振る舞い、会話してください。"
    )
    return base + load_admin_protocol()

# 念のための確認用userメッセージ
admin_protocol_check_message = (
    "念のための確認です。下記【非公開交信プロトコル】の内容を要約し、"
    "ささらさんがもし入力内容を理解できない場合や適切な応答が分からない場合、"
    "どのような手順で対応すべきか、必ず『『ADMIN_Q: ... 』』（ダブル二重カギカッコ）形式で管理者に非公開交信する“そのままコピペできる例”を含めて簡単に説明してください。\n\n"
    "【非公開交信プロトコル】\n"
    + load_admin_protocol()
)

# OpenAIクライアント（ささら人格用）
def get_openai_client():
    api_key = os.environ.get("ASSISTANT_SASARA")
    # print(api_key)
    return openai.OpenAI(api_key=api_key)

# モデル名や追加パラメータもここで管理可能
