import os
import streamlit as st
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
from langchain.callbacks.base import BaseCallbackHandler

# 環境変数を読み込む
load_dotenv()

class StreamCallbackHandler(BaseCallbackHandler):
    def __init__(self, container):
        self.container = container
        self.text = ""
 
    def on_llm_new_token(self, token: str, **kwargs):
        self.text += token
        self.container.markdown(self.text)

@st.cache_resource
def setup_chain():
  # メモリの初期化
  memory = ConversationBufferMemory()
  # LLMの初期化
  llm = ChatOpenAI(model='gpt-3.5-turbo-0125', api_key=os.getenv('OPENAI_API_KEY'), temperature=0.5, streaming=True)
  # チェーンの初期化
  chain = ConversationChain(llm=llm, memory=memory, verbose=True)
  return chain
 
def display_msg(msg, author):
    '''メッセージを表示'''
    st.session_state.messages.append({"role": author, "content": msg})
    st.chat_message(author).write(msg)
 
def main():
    st.title("ChatBotデモ")

    if "messages" not in st.session_state:
        st.session_state["messages"] = []

    for msg in st.session_state["messages"]:
        st.chat_message(msg["role"]).write(msg["content"])
 
    chain = setup_chain()
    user_query = st.chat_input(placeholder="メッセージを入力してください。")
    if user_query:
        display_msg(user_query, 'user')
        with st.chat_message("assistant"):
            st_cb = StreamCallbackHandler(st.empty())
            result = chain.invoke(
                {"input":user_query},
                {"callbacks": [st_cb]}
            )
        response = result["response"]
        st.session_state.messages.append({"role": "assistant", "content": response})

if __name__ == "__main__":
  main()