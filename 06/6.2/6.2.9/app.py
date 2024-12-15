from typing import Any

from dotenv import load_dotenv
from langchain_core.callbacks import BaseCallbackHandler
from langchain_core.outputs import LLMResult
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

# カスタムCallback Handler定義
class MyCustomHandler(BaseCallbackHandler):

    # LLM の呼び出しが開始されたとき
    def on_llm_start(self, serialized: dict[str, Any], prompts: list[str], **kwargs):
        print("===開始===")
        print(prompts)

    # 新しいトークンが生成されたとき
    def on_llm_new_token(self, token: str, **kwargs) -> None:
        print(f"トークン: {token}")

    # LLMの呼び出しが終了したとき
    def on_llm_end(self, response: LLMResult, **kwargs):
        print("===終了===")
        print(response)

# 環境変数の読込
load_dotenv()

# プロンプトテンプレート
prompt = ChatPromptTemplate.from_messages(["{animal}に関する面白い話をひとつお願いします"])

# LLMモデルを作成して、カスタムCallback Handlerを渡す
llm = ChatOpenAI(
    model="gpt-4o-mini", streaming=True, callbacks=[MyCustomHandler()]
)

# チェーンの定義
chain = prompt | llm

# 実行
chain.invoke({"animal": "虎"})
