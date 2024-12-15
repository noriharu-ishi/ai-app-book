import streamlit as st
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import create_react_agent

from mail_make import generate_email_content
from mail_send import send_email

# 環境変数を読み込む
load_dotenv()

# モデル作成
model = ChatOpenAI(model="gpt-4o-mini")

# ツール作成
tools = [generate_email_content, send_email]

# メモリ
memory = MemorySaver()

# メモリ付きAgentExecutorの準備
agent_executor = create_react_agent(model, tools, checkpointer=memory)

config = {"configurable": {"thread_id": "abc123"}}

# 画面のタイトルを設定する
st.title("AI秘書")

# チャット履歴を初期化する
if "messages" not in st.session_state:
    st.session_state.messages = []

# アプリを再実行したときに履歴からチャットメッセージを表示する
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ユーザーの入力に反応する
if prompt := st.chat_input("メッセージを入力してください。"):
    # チャットメッセージコンテナにユーザーのメッセージを表示する
    st.chat_message("user").markdown(prompt)

    # チャット履歴にユーザーメッセージを追加する
    st.session_state.messages.append({"role": "user", "content": prompt})

    # 実行
    response = agent_executor.invoke({"messages": [HumanMessage(content=prompt)]}, config)
    print(response)

    # チャットメッセージコンテナにアシスタントの応答を表示する
    with st.chat_message("assistant"):
        st.markdown(response)

    # アシスタントの応答をチャット履歴に追加する
    st.session_state.messages.append({"role": "アシスタント", "content": response})
