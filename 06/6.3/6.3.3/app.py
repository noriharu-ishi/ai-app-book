import os
from dotenv import load_dotenv
from openai import OpenAI
import gradio as gr

# APIキーを取得
load_dotenv()
client = OpenAI(api_key=os.environ['OPENAI_API_KEY'])

def openai_chatbot( content ):
  completion = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
      {"role": "system", "content": "あなたは生成AIのアシスタントです。"},
      {"role": "user", "content": content }
    ]
  )
  return completion.choices[0].message.content

# Gradioインターフェースの作成
interface = gr.Interface(fn=openai_chatbot, inputs="text", outputs="text")

# アプリケーションの起動
interface.launch()