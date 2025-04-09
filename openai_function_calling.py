from openai import OpenAI
import os
import json
from utils import get_weather, get_current_datetime
import httpx
from dotenv import load_dotenv

load_dotenv()

# Initialize OpenAI client
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"), 
    base_url=os.getenv("OPENAI_BASE_URL"),
    http_client=httpx.Client(verify=False)
)

# Define available functions
functions = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get the current weather for a specific city",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {"type": "string", "description": "The city name"}
                },
                "required": ["city"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_current_datetime",
            "description": "Get the current date and time",
            "parameters": {"type": "object", "properties": {}},
        },
    },
]


def run_conversation():
    messages = [
        {
            "role": "user",
            "content": "What's the weather in Shanghai and what's the current date and time?",
        }
    ]

    response = client.chat.completions.create(
        model=os.getenv("OPENAI_MODEL_NAME"),
        messages=messages,
        tools=functions,
        tool_choice="auto",
        stream=False,
    )

    # Handle function calling
    while response.choices[0].finish_reason == "tool_calls":
        for tool_call in response.choices[0].message.tool_calls:
            print(f"Tool call: {tool_call}")
            function_name = tool_call.function.name
            arguments = json.loads(tool_call.function.arguments)
            if function_name == "get_weather":
                function_response = get_weather(arguments["city"])
            elif function_name == "get_current_datetime":
                function_response = get_current_datetime()
            messages.append(
                {
                    "role": "tool",
                    "content": json.dumps(function_response),
                    "tool_call_id": response.choices[0].message.tool_calls[0].id,
                }
            )

        response = client.chat.completions.create(
            model=os.getenv("OPENAI_MODEL_NAME"),
            messages=messages,
            tools=functions,
            tool_choice="auto",
            stream=False,
        )

    print(response.choices[0].message.content)


if __name__ == "__main__":
    run_conversation()
