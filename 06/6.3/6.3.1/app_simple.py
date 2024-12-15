import streamlit as st

# テキストの表示
st.write("デモ")

# ボタンの表示
button = st.button("クリック")
if button:
    st.write("ボタンがクリックされました")

# 選択ボックス
options = st.multiselect(
    'どの生成AIサービスが好きですか',
    ['ChatGPT', 'Gemini', 'Claude', 'Llama3'],
    ["ChatGPT"])
st.write(",".join(options))