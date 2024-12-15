from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv

# 環境変数を読み込む
load_dotenv()

# GPT-4o-miniモデル利用
model = ChatOpenAI(model="gpt-4o-mini")

# メッセージ作成
messages = [
    SystemMessage(content="以下の英語を日本語に翻訳してください。"),
    HumanMessage(content="Hello!"),
]

# LLMへメッセージ送信
result = model.invoke(messages)

# 出力パーサー
parser = StrOutputParser()
answer = parser.invoke(result)

# 結果出力
print(answer)