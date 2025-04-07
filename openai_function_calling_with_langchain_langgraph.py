from mcp_client import McpClient
from openai import OpenAI
import os
from dotenv import load_dotenv
import asyncio
from langchain_mcp_adapters.tools import load_mcp_tools
from langgraph.prebuilt import create_react_agent

from langchain_openai import ChatOpenAI

load_dotenv()

model = ChatOpenAI(model=os.getenv("OPENAI_MODEL_NAME"), api_key=os.getenv("OPENAI_API_KEY"), base_url=os.getenv("OPENAI_BASE_URL"))

async def run_conversation():
    async with McpClient.get_mcp_client() as session:
        # Get tools
        tools = await load_mcp_tools(session)
        print(f"Available tools: {[t.name for t in tools]}")

        # Create and run the agent
        agent = create_react_agent(model, tools)
        response = await agent.ainvoke({"messages": [("user", "What's the weather in Shanghai and what's the current date and time?")]})
        # The final response is in the 'content' of the last message
        final_response = response['messages'][-1].content
        print(f"Final Response: {final_response}")


if __name__ == "__main__":
    asyncio.run(run_conversation())
