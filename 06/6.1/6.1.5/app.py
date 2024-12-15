import openai

# APIキー設定
client = openai.OpenAI(
    api_key="<OpenAI API Key>"
)

# 応答生成
response = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": "こんにちは",
        }
    ],
    model="gpt-4o",
)

# 結果出力
print(response.choices[0].message.content)
