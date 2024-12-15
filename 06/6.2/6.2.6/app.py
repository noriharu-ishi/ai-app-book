from dotenv import load_dotenv
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_community.tools import TavilySearchResults
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

# 環境変数読込
load_dotenv()

# モデル作成
model = ChatOpenAI(model="gpt-4o-mini")

# ツール作成
search = TavilySearchResults()
tools = [search]

# Agent作成
prompt = ChatPromptTemplate.from_messages(
    [
        ("human", "{input}"),
        ("placeholder", "{agent_scratchpad}"),
    ]
)
agent = create_tool_calling_agent(model, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools)

# Agent実行
response = agent_executor.invoke({"input": "明日の東京の天気はどうですか？"})

# 結果出力
print(response["output"])
