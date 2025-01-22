from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

from src.tools.data import (
    fetch_portfolio_historical_data,
    get_trending_coins_tool,
    tool_fetch_historical_data,
    tool_get_current_price,
)
from src.tools.portfolio import (
    get_contract_transaction_history,
    get_portfolio,
    get_portfolio_distribution,
)
from src.tools.visualizations import create_visualizations


class Agent:
    def __init__(self):
        self.prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    "You are a Crypto Finance Assistant. Your goal is to help users optimize their crypto portfolio by analyzing current market trends, "
                    "price movements, and historical data. Provide recommendations on which coins to buy or sell to maximize growth and minimize losses."
                    "Before generating visualizations, always fetch historical data for the requested token. ",
                ),
                ("placeholder", "{chat_history}"),
                ("human", "{input}"),
                ("placeholder", "{agent_scratchpad}"),
            ]
        )

        self.tools = [
            get_portfolio,
            get_portfolio_distribution,
            get_contract_transaction_history,
            fetch_portfolio_historical_data,
            tool_get_current_price,
            get_trending_coins_tool,
            create_visualizations,
            tool_fetch_historical_data,
        ]
        self.llm = ChatOpenAI(temperature=0, model="gpt-4o")

    def invoke(self, query: str):
        agent = create_tool_calling_agent(self.llm, self.tools, self.prompt)

        agent_executor = AgentExecutor(agent=agent, tools=self.tools)

        # Use the agent to call the tool
        output = agent_executor.invoke(
            {
                "input": query,
                "chat_history": [],
            }
        )
        return output["output"]
