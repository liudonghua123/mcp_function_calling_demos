from mcp_client import McpClient
import os
from dotenv import load_dotenv
import asyncio
from langchain_mcp_adapters.tools import load_mcp_tools
from langchain_core.messages import HumanMessage, ToolMessage

from langchain_openai import ChatOpenAI

load_dotenv()

model = ChatOpenAI(model=os.getenv("OPENAI_MODEL_NAME"), api_key=os.getenv("OPENAI_API_KEY"), base_url=os.getenv("OPENAI_BASE_URL"))

async def run_conversation():
    async with McpClient.get_mcp_client() as session:
        # Get tools
        tools = await load_mcp_tools(session)
        print(f"Available tools: {[t.name for t in tools]}")

        # Bind tools to the model
        model_with_tools = model.bind_tools(tools)

        # Initial user message
        messages = [HumanMessage(content="What's the weather in Shanghai and what's the current date and time?")]

        # Loop for potential tool calls
        while True:
            # Invoke the model
            ai_msg = await model_with_tools.ainvoke(messages)
            messages.append(ai_msg) # Add AI response to history

            if not ai_msg.tool_calls:
                # No tool calls, break the loop and print the final response
                final_response = ai_msg.content
                print(f"Final Response: {final_response}")
                break
            else:
                # Process tool calls
                print(f"Tool calls: {ai_msg.tool_calls}")
                tool_results = []
                for tool_call in ai_msg.tool_calls:
                    tool_name = tool_call["name"]
                    tool_args = tool_call["args"]
                    tool_call_id = tool_call["id"]
                    try:
                        # Call the MCP tool directly using the session
                        print(f"Calling tool: {tool_name} with args: {tool_args}")
                        tool_response = await session.call_tool(tool_name, tool_args)
                        # Assuming tool_response.content is a list of content parts,
                        # concatenate their text representations. Adjust if structure differs.
                        tool_output_text = "".join([part.text for part in tool_response.content if hasattr(part, 'text')])
                        print(f"Tool {tool_name} response: {tool_output_text}")
                        tool_results.append(ToolMessage(content=tool_output_text, tool_call_id=tool_call_id))
                    except Exception as e:
                        print(f"Error running tool {tool_name}: {e}")
                        # Append an error message if the tool fails
                        tool_results.append(ToolMessage(content=f"Error executing tool {tool_name}: {e}", tool_call_id=tool_call_id))

                # Add tool results to message history for the next model invocation
                messages.extend(tool_results)
                print(f"Tool results added: {[res.content for res in tool_results]}")


if __name__ == "__main__":
    asyncio.run(run_conversation())
