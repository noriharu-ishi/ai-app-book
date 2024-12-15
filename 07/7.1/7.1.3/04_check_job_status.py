from openai import OpenAI
from dotenv import load_dotenv

# 環境変数を読み込む
load_dotenv()

# OpenAIクライアントを初期化
client = OpenAI()

# ファインチューニングジョブ一覧を取得する
client.fine_tuning.jobs.list(limit=10)

# ファインチューニングジョブを検索する
client.fine_tuning.jobs.retrieve("ftjob-abc123")

# ファインチューニングジョブをキャンセルする
client.fine_tuning.jobs.cancel("ftjob-abc123")

# ファインチューニングジョブのイベントを最大10件取得する
client.fine_tuning.jobs.list_events(fine_tuning_job_id="ftjob-abc123", limit=10)

# ファインチューニングされたモデルを削除する（モデルが作成された組織の所有者である必要がある）
client.models.delete("ft:gpt-3.5-turbo:acemeco:suffix:abc123")