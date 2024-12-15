from dotenv import load_dotenv
from fastapi import FastAPI
from langchain.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langserve import add_routes

# 環境変数読込
load_dotenv()

app = FastAPI(
    title="LangServeサンプル",
    version="1.0",
    description="LangServeサンプルインタフェース",
)

model = ChatOpenAI(model="gpt-4o-mini")
prompt = ChatPromptTemplate.from_template("{topic}についてのジョーク１つお願いします。")
add_routes(
    app,
    prompt | model,
    path="/joke",
)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="localhost", port=8080)