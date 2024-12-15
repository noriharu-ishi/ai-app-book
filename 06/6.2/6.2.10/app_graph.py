import io
from typing import TypedDict

from PIL import Image
from langgraph.constants import START, END
from langgraph.graph import StateGraph

# 入力Stateの定義：ユーザー入力を含む
class InputState(TypedDict):
    user_input: str

# 出力Stateの定義：グラフの最終出力を含む
class OutputState(TypedDict):
    graph_output: str

# 全体のStateの定義：グラフ全体で共有される状態
class OverallState(TypedDict):
    foo: str
    user_input: str
    graph_output: str

# ノード間で共有されないプライベートな状態の定義
class PrivateState(TypedDict):
    bar: str

# node1: ユーザー入力を受け取り、OverallStateに中間値を書き込む
def node_1(state: InputState) -> OverallState:
    return {"foo": state["user_input"] + "の名前"}

# node2: node2: OverallStateから読み出し、新たな中間値をPrivateStateに書き込む
def node_2(state: OverallState) -> PrivateState:
    return {"bar": state["foo"] + "は"}

# node3: PrivateStateから読み出し、最終的な出力をOutputStateに書き込む
def node_3(state: PrivateState) -> OutputState:
    return {"graph_output": state["bar"] + "石です"}

# StateGraphの定義：全体の状態、入力、出力の型を指定
workflow = StateGraph(OverallState, input=InputState, output=OutputState)

# グラフにノードを追加
workflow.add_node("node_1", node_1)
workflow.add_node("node_2", node_2)
workflow.add_node("node_3", node_3)

# ノード間のエッジを定義
workflow.add_edge(START, "node_1")
workflow.add_edge("node_1", "node_2")
workflow.add_edge("node_2", "node_3")
workflow.add_edge("node_3", END)

# グラフをコンパイルして実行可能な形式に変換
app = workflow.compile()

# グラフを実行：ユーザー入力"私"を与えて処理を開始
result = app.invoke({"user_input": "私"})

# 実行結果出力
print(result)

# 可視化
img_data = app.get_graph().draw_mermaid_png()
image = Image.open(io.BytesIO(img_data))
image.show()