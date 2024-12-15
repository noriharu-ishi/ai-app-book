from dotenv import load_dotenv
from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableLambda, RunnablePassthrough
from langchain_openai import ChatOpenAI
from langchain_openai import OpenAIEmbeddings

# 環境変数読込
load_dotenv()

# サンプルドキュメントの作成
documents = [
    Document(
        page_content="犬は忠実で親しみやすい伴侶動物として知られています。",
        metadata={"source": "哺乳類ペットの資料"},
    ),
    Document(
        page_content="猫は独立心の強いペットで、自分の時間や空間を楽しむことが多いです。",
        metadata={"source": "哺乳類ペットの資料"},
    ),
    Document(
        page_content="金魚は初心者にも人気のペットで、比較的簡単な世話で飼育できます。",
        metadata={"source": "魚類ペットの資料"},
    ),
    Document(
        page_content="オウムは知能が高く、人間の言葉を真似する能力があります。",
        metadata={"source": "鳥類ペットの資料"},
    ),
    Document(
        page_content="ウサギは社交的で、飛び跳ねるための十分なスペースが必要です。",
        metadata={"source": "哺乳類ペットの資料"},
    ),
]

# ベクトルストアの作成
vectorstore = Chroma.from_documents(
    documents,
    embedding=OpenAIEmbeddings(),
)

# retrieverの定義、一番先頭の結果を取得する
retriever = RunnableLambda(vectorstore.similarity_search).bind(k=1)

# モデルの定義
model = ChatOpenAI(model="gpt-4o-mini")

# プロンプトテンプレートの定義
message = """
提供されたコンテキストのみを使用して以下の質問に答えてください。

{question}

Context:
{context}
"""

prompt = ChatPromptTemplate.from_messages([("human", message)])

# チェーンの定義
rag_chain = {"context": retriever, "question": RunnablePassthrough()} | prompt | model

# チェーン実行
response = rag_chain.invoke("猫について教えてください")

# 結果出力
print(response.content)
