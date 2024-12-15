from openai import OpenAI

# APIキー設定
client = OpenAI(
    api_key="<OpenAI API Key>"
)

# 応答生成
stream = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": "こんにちは"}],
    stream=True,
)

# 結果出力
for chunk in stream:
    if chunk.choices[0].delta.content is not None:
        print(chunk.choices[0].delta.content, end="")