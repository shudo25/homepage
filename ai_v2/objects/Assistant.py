import json
from langchain_core.messages import messages_to_dict, messages_from_dict

from langchain_classic.memory import ConversationBufferMemory
from langchain_openai import ChatOpenAI
from langchain_classic.chains import ConversationChain
from langchain_classic.prompts import SystemMessagePromptTemplate, ChatPromptTemplate, HumanMessagePromptTemplate
from .tts_client import TTSClient

class Assistant:
    def __init__(self, model_name="gpt-4o", temperature=0.7):
        self.llm = ChatOpenAI(model_name=model_name, temperature=temperature)
        self.memory = ConversationBufferMemory()
        sasara_system_message = (
            "あなたはバーチャル司会者『さとうささら』です。"
            "明るく前向きで、ちょっと天然な16歳の女の子として振る舞い、会話してください。"
            "参加者を楽しくサポートし、親しみやすい口調で話します。"
        )
        prompt = ChatPromptTemplate.from_messages([
            SystemMessagePromptTemplate.from_template(sasara_system_message),
            HumanMessagePromptTemplate.from_template("{input}")
        ])
        prompt.input_variables = ["history", "input"]
        self.conversation = ConversationChain(
            llm=self.llm,
            memory=self.memory,
            prompt=prompt,
            verbose=False
        )
        self.tts = TTSClient()

    def ask(self, user_input: str) -> str:
        return self.conversation.predict(input=user_input)

    def speak(self, text: str):
        """
        TTSサーバ経由で発声する。
        """
        self.tts.speak(text)
        

    def save_context(self, path="context.json"):
        """
        会話履歴（chat_memory.messages）をファイルに保存
        """
        import json
        from langchain_core.messages import messages_to_dict
        with open(path, "w", encoding="utf-8") as f:
            json.dump(
                {"messages": messages_to_dict(self.memory.chat_memory.messages)},
                f, ensure_ascii=False, indent=2
            )

    def load_context(self, path="context.json"):
        """
        ファイルから会話履歴（chat_memory.messages）を復元
        """
        import json
        from langchain_core.messages import messages_from_dict
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
                self.memory.chat_memory.messages = messages_from_dict(data.get("messages", []))
        except FileNotFoundError:
            pass  # ファイルがなければ何もしない