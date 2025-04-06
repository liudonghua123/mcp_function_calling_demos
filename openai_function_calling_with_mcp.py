from mcp_client import McpClient
from openai import OpenAI
import os
import json
from dotenv import load_dotenv
import asyncio

load_dotenv()

# Initialize OpenAI client with environment variables
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"), base_url=os.getenv("OPENAI_BASE_URL")
)

async def run_conversation():
    messages = [
        {
            "role": "user",
            "content": "What's the weather in Shanghai and what's the current date and time?",
        }
    ]

    async with McpClient.get_mcp_client() as mcp_client:
        # Get available tools
        mcp_tools = await mcp_client.list_tools()
        tools = [
            {
                "type": "function",
                "function": {
                    "name": tool.name,
                    "description": tool.description,
                    "parameters": tool.inputSchema,
                },
            }
            for tool in mcp_tools.tools
        ]
        print(f"Available tools: {[t.name for t in mcp_tools.tools]}")

        response = client.chat.completions.create(
            model=os.getenv("OPENAI_MODEL_NAME"),
            messages=messages,
            tools=tools,
            tool_choice="auto",
        )

        # Handle function calling
        while response.choices[0].finish_reason == "tool_calls":
            tool_call = response.choices[0].message.tool_calls[0]
            function_name = tool_call.function.name
            arguments = json.loads(tool_call.function.arguments)

            # Call MCP tool
            function_response = await mcp_client.call_tool(
                name=function_name, arguments=arguments
            )

            messages.append(response.choices[0].message)
            messages.append(
                {
                    "role": "tool",
                    "content": function_response.content[0].text,
                    "tool_call_id": tool_call.id,
                }
            )

            response = client.chat.completions.create(
                model=os.getenv("OPENAI_MODEL_NAME"),
                messages=messages,
                tools=tools,
                tool_choice="auto",
            )

        print(response.choices[0].message.content)


if __name__ == "__main__":
    asyncio.run(run_conversation())
