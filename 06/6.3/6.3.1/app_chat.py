import streamlit as st

# タイトルの設定
st.title("Streamlit ChatBot デモ")

# チャット履歴の管理
if "messages" not in st.session_state:
    st.session_state.messages = []

# 過去のメッセージの表示
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ユーザー入力の受け取り
if prompt := st.chat_input("メッセージを入力してください。"):
    # チャットメッセージコンテナにユーザーのメッセージを表示する
    st.chat_message("user").markdown(prompt)

    # チャット履歴にユーザーメッセージを追加する
    st.session_state.messages.append({"role": "user", "content": prompt})

    response = f"Assistant: {prompt}"
    # チャットメッセージコンテナにアシスタントの応答を表示する
    with st.chat_message("assistant"):
        st.markdown(response)

    # アシスタントの応答をチャット履歴に追加する
    st.session_state.messages.append({"role": "アシスタント", "content": response})