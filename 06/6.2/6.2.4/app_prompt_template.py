from langchain_core.prompts import PromptTemplate

# プロンプトテンプレートの準備
prompt_template = PromptTemplate(
    input_variables=["language"],
    template="次の英語を{language}に翻訳してください。：Hello",
)

# プロンプトテンプレートの実行
output = prompt_template.invoke({"language": "日本語"})

# 結果出力
print(type(output))
print(output)
