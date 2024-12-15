from dotenv import load_dotenv
from openai import OpenAI

# 環境変数を読み込む
load_dotenv()

# OpenAIクライアントを初期化
client = OpenAI()

# ファインチューニングジョブを作成する
client.fine_tuning.jobs.create(
  training_file="data.jsonl",
  model="gpt-3.5-turbo"
)
