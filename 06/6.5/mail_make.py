from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI

# 環境変数を読み込む
load_dotenv()

# LLMを定義
llm = ChatOpenAI(model="gpt-4o-mini")

# プロンプトテンプレートの準備
prompt_template = PromptTemplate(
    input_variables=["request"],
    template=
    """
    ユーザーの要求に基づいて、メール内容を生成してください:\n\n{request}。
    メールのフォーマットは以下の通りです。
    xxさん

    お疲れ様です。xxです。

    　メール本文

    以上、よろしくお願いいたします。
    """
)

# OutputParserの準備
output_parser = StrOutputParser()

# チェーンの定義
chain = prompt_template | llm | output_parser

# メール内容生成関数
@tool
def generate_email_content(request):
    """
    ユーザの入力に基づき、会議調整メール内容を作成する
    """
    # 実行
    content = chain.invoke({"request": request})

    # 生成したメール文を返す
    return content

# テスト
if __name__ == "__main__":
    user_request = "来週年度計画について会議を設定したいです。"
    email_content = generate_email_content(user_request)
    print("生成されたメール内容:\n", email_content)