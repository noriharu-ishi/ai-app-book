from dotenv import load_dotenv
from langchain_community.chat_message_histories import SQLChatMessageHistory
from langchain_core.messages import HumanMessage
from langchain_core.runnables import RunnableWithMessageHistory
from langchain_openai import ChatOpenAI

# 環境変数読込
load_dotenv()

# OpenAIモデルのインスタンス作成
llm = ChatOpenAI(model="gpt-4o-mini")

# セッションIDに基づいてSQLiteデータベースからチャット履歴を取得する関数
def get_session_history(session_id):
    return SQLChatMessageHistory(session_id, connection="sqlite:///memory.db")

# チャット履歴を保持できるRunnableオブジェクト作成
runnable_with_history = RunnableWithMessageHistory(
    llm,
    get_session_history,
)

# 最初の会話：自己紹介
response = runnable_with_history.invoke(
    [HumanMessage(content="石と申します。よろしくお願いいたします。")],
    config={"configurable": {"session_id": "1"}},  # セッションID "1" を使用
)
print(response.content)

# 2回目の会話：名前の確認（同じセッションID）
response = runnable_with_history.invoke(
    [HumanMessage(content="私の名前はなんですか。")],
    config={"configurable": {"session_id": "1"}},  # 同じセッションID "1" を使用
)
print(response.content)

# 3回目の会話：名前の確認（異なるセッションID）
response = runnable_with_history.invoke(
    [HumanMessage(content="私の名前はなんですか。")],
    config={"configurable": {"session_id": "1a"}},  # 新しいセッションID "1a" を使用
)
print(response.content)