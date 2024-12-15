from dotenv import load_dotenv
from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI

# 環境変数読込
load_dotenv()

# モデル作成
chat_model = ChatOpenAI()

# モデル実行
messages = [
    HumanMessage(content="日本の首都はどこですか。")
]
output = chat_model.invoke(messages)

# 結果出力
print(type(output))
print(output)