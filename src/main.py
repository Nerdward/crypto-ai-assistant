from fastapi import FastAPI

from src.agent import Agent

app = FastAPI()
agent = Agent()


@app.get("/ask-the-ai-agent")
async def ask_the_agent(query: str):
    return agent.invoke(query)
