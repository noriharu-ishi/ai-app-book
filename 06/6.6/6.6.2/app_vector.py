import os

from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_milvus import Milvus
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import CharacterTextSplitter

# 環境変数を読み込む
load_dotenv()

# Embeddingモデルの定義
embeddings = OpenAIEmbeddings(
    model="text-embedding-3-large",
)

# ファイルとして保存する場合
# URI = "./milvus_example.db"

# Milvusデータベースに保存する場合
URI = "http://localhost:19530"

# MilvusベクトルDBの定義
vector_store = Milvus(
    embedding_function=embeddings,
    connection_args={"uri": URI},
)

# PDFファイルロード
file_path = "./"
file_name = "就業規則.pdf"
loader = PyPDFLoader(os.path.join(file_path, file_name))

# PDFファイルをページ単位に分割
pages = loader.load_and_split()

# ページごとにベクトル化処理
for page_number, page in enumerate(pages, start=1):
    # メタ情報追加
    page.metadata["source"] = file_path
    page.metadata["name"] = file_name

    # チャンク分割
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    docs = text_splitter.split_documents([page])

    # ベクトルDBに保存
    vector_store_saved = Milvus.from_documents(
        docs,
        embeddings,
        collection_name="langchain_example",
        connection_args={"uri": URI},
    )

    # 処理中
    print(f"ベクトル化完了: ページ {page_number}")
