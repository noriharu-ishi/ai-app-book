from dotenv import load_dotenv
from langchain_openai import OpenAI

# 環境変数読込
load_dotenv()

# モデル作成
llm = OpenAI()

# モデル実行
output = llm.invoke("日本の首都はどこですか。")

# 結果出力
print(type(output))
print(output)
