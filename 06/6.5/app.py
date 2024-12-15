import streamlit as st
from dotenv import load_dotenv
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableWithMessageHistory
from langchain_openai import ChatOpenAI

from mail_make import generate_email_content
from mail_send import send_email

# 環境変数を読み込む
load_dotenv()

# モデル作成
model = ChatOpenAI(model="gpt-4o-mini")

# ツール作成
tools = [generate_email_content, send_email]

# Agent作成
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "あなたはAI秘書です。"),
        ("placeholder", "{chat_history}"),
        ("human", "{input}"),
        ("placeholder", "{agent_scratchpad}"),
    ]
)
agent = create_tool_calling_agent(model, tools, prompt)

# メモリ
memory = ChatMessageHistory(session_id="test-session")

# メモリ付きAgentExecutorの準備
agent_executor = AgentExecutor(agent=agent, tools=tools)
agent_with_chat_history = RunnableWithMessageHistory(
    agent_executor,
    lambda session_id: memory,
    input_messages_key="input",
    history_messages_key="chat_history",
)

config = {"configurable": {"session_id": "test-session"}}

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
    response = agent_with_chat_history.invoke({"input": prompt}, config)
    response = response["output"]

    # チャットメッセージコンテナにアシスタントの応答を表示する
    with st.chat_message("assistant"):
        st.markdown(response)

    # アシスタントの応答をチャット履歴に追加する
    st.session_state.messages.append({"role": "アシスタント", "content": response})
