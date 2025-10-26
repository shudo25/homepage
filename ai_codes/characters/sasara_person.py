# ささらの人格・LLM設定
import openai
import os

system_prompt = "あなたはバーチャル司会者『さとうささら』です。..."  # 必要に応じて詳細化

# OpenAIクライアント（ささら人格用）
def get_openai_client():
    return openai.OpenAI(api_key=os.environ.get("ASSISTANT_SASARA"))

# モデル名や追加パラメータもここで管理可能
