import io

from PIL import Image
from dotenv import load_dotenv
from langchain_community.tools import TavilySearchResults
from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import END, START, StateGraph, MessagesState
from langgraph.prebuilt import ToolNode

# 環境変数読込
load_dotenv()

# 検索ツールの定義
search = TavilySearchResults()
tools = [search]

# モデルの定義
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0).bind_tools(tools)

# ツールノードの定義
tool_node = ToolNode(tools)

# 継続するかどうかを決定する関数の定義
def should_continue(state: MessagesState) -> ["tools", END]:
    messages = state['messages']
    last_message = messages[-1]

    # LLMがツール呼び出しを行う場合、"tools"ノードにルーティング
    if last_message.tool_calls:
        return "tools"

    # それ以外の場合は停止（ユーザーに返答）
    return END


# モデルを呼び出す関数を定義
def call_model(state: MessagesState):
    messages = state['messages']
    response = llm.invoke(messages)
    # 既存のリストに追加して返す
    return {"messages": [response]}


# 新しいグラフを定義
workflow = StateGraph(MessagesState)

# 2つのノードを追加
workflow.add_node("agent", call_model)
workflow.add_node("tools", tool_node)

# エントリポイントを`agent`に設定
# このノードが最初に呼び出されることを意味する
workflow.add_edge(START, "agent")

# 条件付きエッジを追加
workflow.add_conditional_edges(
    # まず、開始ノードを定義。ここでは`agent`を使用。
    # これは、`agent`ノードが呼び出された後にこれらのエッジが使用されることを意味する。
    "agent",
    # 次に、次に呼び出されるノードを決定する関数を渡す。
    should_continue,
)

# `tools`から`agent`への通常のエッジを追加
# `tools`が呼び出された後、次に`agent`ノードが呼び出されることを意味する。
workflow.add_edge("tools", 'agent')

# 最後に、グラフをコンパイル
app = workflow.compile()

# 実行する
final_state = app.invoke(
    {"messages": [HumanMessage(content="明日の東京の天気はどうですか？")]}
)

# 結果出力
print(final_state["messages"][-1].content)

# 可視化
img_data = app.get_graph().draw_mermaid_png()
image = Image.open(io.BytesIO(img_data))
image.show()