from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langsmith import Client
from langsmith.evaluation import evaluate

# 環境変数を読み込む
load_dotenv()

# データセット定義
client = Client()
dataset_name = "Sample Dataset"
dataset = client.create_dataset(dataset_name, description="LangSmithサンプルデータセット")
client.create_examples(
    inputs=[
        {"postfix": "LangSmithへ"},
        {"postfix": "LangSmithの評価へ"},
        {"postfix": "LangSmithの体験へ"},
    ],
    outputs=[
        {"output": "ようこそ、LangSmithへ"},
        {"output": "ようこそ、LangSmithの評価へ"},
        {"output": "Hello、LangSmithの体験へ"},
    ],
    dataset_id=dataset.id,
)

# OpenAIのモデルを使って入力から出力を生成する関数を定義
def generate_openai_response(input_data):
    prompt = ChatPromptTemplate.from_messages(["生成してください: ようこそ、{postfix}"])
    llm = ChatOpenAI(model="gpt-4o-mini", streaming=True)
    chain = prompt | llm
    response = chain.invoke({'postfix': input_data['postfix']})
    return response.content.strip()

# 評価ロジックを定義（前方一致を行う）
def prefix_match(run, example):
    # AIモデルの出力が期待する出力の前方一致かを確認
    is_match = run.outputs["output"].startswith(example.outputs["output"])
    return {"score": is_match}

# 評価の実行
experiment_results = evaluate(
    generate_openai_response, # OpenAIモデルによる応答生成関数を指定
    data=dataset_name, # データセット名
    evaluators=[prefix_match], # prefix_matchによる評価を行う
    experiment_prefix="sample-experiment", # 実験名を設定
    metadata={
      "version": "1.0.0",
      "revision_id": "beta"
    },
)
