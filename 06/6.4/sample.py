import os
from dotenv import load_dotenv
import streamlit as st
from openai import OpenAI

# 環境変数を読み込む
load_dotenv()

# APIキーの設定
client = OpenAI(
    # This is the default and can be omitted
    api_key=os.getenv('OPENAI_API_KEY'),
)

st.title("ChatBotデモ")

# 定数定義
USER_NAME = "user"
ASSISTANT_NAME = "assistant"

def response_chatgpt(user_msg: str,):
    """ChatGPTのレスポンスを取得

    Args:
        user_msg (str): ユーザーメッセージ。
    """
    response = client.chat.completions.create(
        messages=[
            {"role": "user", "content": user_msg},
        ],
        model="gpt-3.5-turbo",
        stream=True,
    )
    return response


# チャットログを保存したセッション情報を初期化
if "chat_log" not in st.session_state:
    st.session_state.chat_log = []


user_msg = st.chat_input("ここにメッセージを入力")
if user_msg:
    # 以前のチャットログを表示
    for chat in st.session_state.chat_log:
        with st.chat_message(chat["name"]):
            st.write(chat["msg"])

    # 最新のメッセージを表示
    with st.chat_message(USER_NAME):
        st.write(user_msg)

    # アシスタントのメッセージを表示
    response = response_chatgpt(user_msg)
    with st.chat_message(ASSISTANT_NAME):
        assistant_msg = ""
        assistant_response_area = st.empty()
        for chunk in response:
            if chunk.choices[0].finish_reason is not None:
                break
            # 回答を逐次表示
            assistant_msg += chunk.choices[0].delta.content
            assistant_response_area.write(assistant_msg)

    # セッションにチャットログを追加
    st.session_state.chat_log.append({"name": USER_NAME, "msg": user_msg})
    st.session_state.chat_log.append({"name": ASSISTANT_NAME, "msg": assistant_msg})