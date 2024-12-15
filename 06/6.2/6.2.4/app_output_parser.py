from langchain_core.output_parsers import JsonOutputParser

# JSON Parserの準備
json_parser = JsonOutputParser()

# JSON形式データ準備
json_content = \
  """
  {
    "status": 200, 
    "data":
    [
        {
            "名前": "高橋", 
            "年齢": 30
        },
        {
            "名前": "田中",
            "年齢": 25
        }
    ]
  }
  """

# JSON Parserの実行
output = json_parser.parse(json_content)

# 結果出力
print(type(output))
print(output)