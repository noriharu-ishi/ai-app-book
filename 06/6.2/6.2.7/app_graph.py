from dotenv import load_dotenv
from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.memory import MemorySaver
from langgraph.constants import START
from langgraph.graph import StateGraph, MessagesState

# 環境変数読込
load_dotenv()

# モデルの定義
llm = ChatOpenAI(model="gpt-4o-mini")

# グラフの定義
workflow = StateGraph(state_schema=MessagesState)

# モデル呼び出し関数
def call_model(state: MessagesState):
    response = llm.invoke(state["messages"])
    # 履歴更新
    return {"messages": response}

# グラフノードの定義
workflow.add_edge(START, "model")
workflow.add_node("model", call_model)

# メモリの定義
memory = MemorySaver()
app = workflow.compile(checkpointer=memory)

# 会話スレッドの定義
config = {"configurable": {"thread_id": "abc123"}}

# 最初の会話：自己紹介
query = "石と申します。よろしくお願いいたします。"
input_messages = [HumanMessage(query)]
output = app.invoke({"messages": input_messages}, config)
output["messages"][-1].pretty_print()

# 2回目の会話：名前の確認（同じセッションID）
query = "私の名前はなんですか。"
input_messages = [HumanMessage(query)]
output = app.invoke({"messages": input_messages}, config)
output["messages"][-1].pretty_print()

# 新しい会話スレッド
config = {"configurable": {"thread_id": "abc234"}}

# 3回目の会話：名前の確認（異なるセッションID）
query = "私の名前はなんですか。"
input_messages = [HumanMessage(query)]
output = app.invoke({"messages": input_messages}, config)
output["messages"][-1].pretty_print()
