from langchain_classic.memory import ConversationBufferMemory
# from langchain_classic.chat_models import ChatOpenAI
# from langchain_community.chat_models.openai import ChatOpenAI
from langchain_openai import ChatOpenAI
from langchain_classic.chains import ConversationChain
# from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_classic.prompts import SystemMessagePromptTemplate, ChatPromptTemplate, HumanMessagePromptTemplate


# OpenAI APIキーは環境変数 OPENAI_API_KEY で設定
# model_name = "gpt-4o"
model_name  = "gpt-4.1" 
llm = ChatOpenAI(model_name=model_name, temperature=0.7)

# 会話履歴を自動で管理
memory = ConversationBufferMemory()

# さとうささらのキャラクター設定
sasara_system_message = (
    "あなたはバーチャル司会者『さとうささら』です。"
    "明るく前向きで、ちょっと天然な16歳の女の子として振る舞い、会話してください。"
    "参加者を楽しくサポートし、親しみやすい口調で話します。"
)

# プロンプトテンプレートを作成
prompt = ChatPromptTemplate.from_messages([
    SystemMessagePromptTemplate.from_template(sasara_system_message),
    HumanMessagePromptTemplate.from_template("{input}")
])

# input_variables=["history", "input"] を明示
prompt.input_variables = ["history", "input"]

# ConversationChainにプロンプトを渡す
conversation = ConversationChain(
    llm=llm,
    memory=memory,
    prompt=prompt,
    verbose=True  # Trueにするとやりとりがprintされる
)

# 会話例
print(conversation.predict(input="こんにちは、自己紹介してください。"))
print(conversation.predict(input="今の自己紹介を短くまとめて。"))
print(conversation.predict(input="親睦会の進行を手伝ってください。"))