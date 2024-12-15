import streamlit as st
from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_milvus import Milvus
from langchain_openai import ChatOpenAI, OpenAIEmbeddings

# 環境変数を読み込む
load_dotenv()

# モデル作成
model = ChatOpenAI(model="gpt-4o-mini")

# Embeddingモデルの定義
embeddings = OpenAIEmbeddings(
    model="text-embedding-3-large",
)

# プロンプトテンプレート
PROMPT_TEMPLATE = """
Human: あなたはAIアシスタントで、可能な限り事実に基づいた情報使用して質問に答えます。
以下の情報を使用して、<question>タグに囲まれた質問に対して簡潔な回答を提供してください。
答えがわからない場合は、「わかりません」とだけ言ってください。無理に答えを作ろうとしないでください。

<context>
{context}
</context>

<question>
{question}
</question>

回答は具体的にしてください。

Assistant:"""
prompt = PromptTemplate(
    template=PROMPT_TEMPLATE, input_variables=["context", "question"]
)

# ファイルとして保存する場合
# URI = "./milvus_example.db"

# Milvusデータベースに保存する場合
URI = "http://localhost:19530"

# Milvusデータベースに接続
vectorstore = Milvus(
  collection_name="langchain_example",
  connection_args={"uri": URI},
  embedding_function=embeddings,
)

# ベクトルデータベースをretrieverに変換
retriever = vectorstore.as_retriever()

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

# チェーンの定義
rag_chain = (
    {"context": retriever | format_docs, "question": RunnablePassthrough()}
    | prompt
    | model
    | StrOutputParser()
)

# 画面のタイトルを設定する
st.title("会社規則アシスタント")

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
    response = rag_chain.invoke(prompt)

    # チャットメッセージコンテナにアシスタントの応答を表示する
    with st.chat_message("assistant"):
        st.markdown(response)

    # アシスタントの応答をチャット履歴に追加する
    st.session_state.messages.append({"role": "アシスタント", "content": response})
