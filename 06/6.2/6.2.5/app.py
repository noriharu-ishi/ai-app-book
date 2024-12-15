from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI

# 環境変数読込
load_dotenv()

# プロンプトテンプレートの準備
prompt_template = PromptTemplate(
    input_variables=["language"],
    template="次の英語を{language}に翻訳してください。：Hello",
)

# ChatModelの準備
chat_model = ChatOpenAI(model="gpt-4o-mini")

# OutputParserの準備
output_parser = StrOutputParser()

# チェーンをつなげて実行
chain = prompt_template | chat_model | output_parser
output = chain.invoke({"language": "日本語"})

# 結果出力
print(output)