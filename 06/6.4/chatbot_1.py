import os
import time
from openai import OpenAI
from dotenv import load_dotenv

# 環境変数を読み込む
load_dotenv()

# OpenAIクライアントの初期化
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

# メッセージ履歴
message_history = []

def chat_with_gpt(prompts):
  '''ChatGPTによる対話'''
  completion = client.chat.completions.create(
    model="gpt-3.5-turbo-1106",
    messages = [
      {"role": "system", "content": "あなたはヘルプデスクです。"},
      *prompts
    ],
    max_tokens=2000,
    temperature=0.5,
    stream=True,
  )
  return completion

def print_stream_result(stream):
  '''ChatGPTの応答を表示'''
  content = []
  print("アシスタント:", end="")
  for chunk in stream:
    if chunk.choices[0].delta.content is not None:
      print(chunk.choices[0].delta.content, end="", flush=True)
      content.append(chunk.choices[0].delta.content)
      time.sleep(0.05)
  print()
  return "".join(content)

def main():
  print("こんにちは！話しかけてください。終了する場合はexitと入力してください。")
  while True:
    user_input = input("あなた:")

    # exitが入力されたら終了
    if user_input == "exit":
      break

    # ChatGPTによる対話
    message_history.append({"role": "user", "content": user_input})
    completion = chat_with_gpt(message_history)

    # ChatGPTの応答を表示
    response = print_stream_result(completion)
    message_history.append({"role": "assistant", "content": response})

if __name__ == "__main__":
  main()