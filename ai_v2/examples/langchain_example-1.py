from langchain_classic.memory import ConversationBufferMemory
from langchain_openai import ChatOpenAI
from langchain_classic.chains import ConversationChain
# from langchain_core.runnables.history import RunnableWithMessageHistory

# OpenAI APIキーは環境変数 OPENAI_API_KEY で設定
llm = ChatOpenAI(model_name="gpt-4o", temperature=0.7)

# 会話履歴を自動で管理
memory = ConversationBufferMemory()

# 会話チェーンを作成
conversation = ConversationChain(
    llm=llm,
    memory=memory,
    verbose=True  # Trueにするとやりとりがprintされる
)

# 会話例
print(conversation.predict(input="こんにちは、自己紹介してください。"))
print(conversation.predict(input="今の自己紹介を短くまとめて。"))
print(conversation.predict(input="親睦会の進行を手伝ってください。"))