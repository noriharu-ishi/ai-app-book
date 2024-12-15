from dotenv import load_dotenv
from openai import OpenAI

# 環境変数を読み込む
load_dotenv()

# OpenAIクライアントを初期化
client = OpenAI()

# ファイルをアップロードする
file = client.files.create(
  file=open("data.jsonl", "rb"),
  purpose="fine-tune"
)
