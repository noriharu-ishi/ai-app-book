from openai import OpenAI
from dotenv import load_dotenv

# 環境変数を読み込む
load_dotenv()

client = OpenAI()

completion = client.chat.completions.create(
  # model="ft:gpt-3.5-turbo:my-org:custom_suffix:id",
  model="ft:gpt-3.5-turbo-0125:rgs::9dD7VClW",
  messages=[
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "Hello!"}
  ]
)
print(completion.choices[0].message)