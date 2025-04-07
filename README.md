# OpenAI Function Calling with MCP Examples

Welcome! This project provides examples of how to use OpenAI's function calling feature, particularly in conjunction with the Model Context Protocol (MCP). It's designed to help you understand different ways to connect large language models (LLMs) like those from OpenAI to external tools and data sources.

## What is OpenAI Function Calling?

OpenAI models (like GPT-3.5-turbo and GPT-4) have a feature called "function calling". This allows the model, when prompted appropriately, to request that specific functions (or "tools") be executed outside of the model itself.

Imagine you ask the model, "What's the weather like in London?". Instead of just guessing or using outdated information, the model can say, "I need to call a function named `get_weather` with the argument `city=London`". Your application code then receives this request, executes the actual `get_weather` function (which might call a real weather API), gets the result (e.g., "15°C and cloudy"), and sends this result back to the model. The model then uses this information to give you a final, accurate answer like, "The weather in London is currently 15°C and cloudy."

## What is MCP (Model Context Protocol)?

MCP is a standardized way for AI models and external tools/resources to communicate. It defines a common language (protocol) so that different models and tools can interact without needing custom integrations for each pair.

Think of it like USB for AI tools. Just as USB allows various devices (keyboards, mice, printers) to connect to a computer using a standard port, MCP allows various AI tools (weather APIs, database connectors, web search tools) to connect to different AI models using a standard protocol.

This project includes a simple MCP server (`mcp_server.py`) that exposes two tools: one for getting the weather and one for getting the current date and time.

## Project Examples Explained

This repository contains several Python scripts demonstrating different approaches:

1.  **`mcp_server.py`**:
    *   **Purpose**: This script runs a simple MCP server.
    *   **How it works**: It defines two tools (`get_weather_tool` and `get_current_datetime_tool`) and makes them available via the MCP protocol. Other scripts in this project connect to this server to use these tools. You need to run this server in the background for the MCP-based examples to work.

2.  **`openai_function_calling_with_mcp.py`**:
    *   **Purpose**: Shows the core concept of using OpenAI function calling with an MCP server *without* using extra libraries like LangChain.
    *   **How it works**:
        *   Connects to the running `mcp_server.py`.
        *   Asks the OpenAI model a question ("What's the weather in Shanghai and what's the current date and time?").
        *   The OpenAI model responds, indicating which MCP tools it wants to call (e.g., `get_weather_tool` and `get_current_datetime_tool`).
        *   This script receives the tool call requests, uses the MCP client to execute them via the `mcp_server.py`, gets the results, and sends them back to the OpenAI model.
        *   The OpenAI model then generates the final answer using the tool results.

3.  **`openai_function_calling.py`**:
    *   **Purpose**: Demonstrates OpenAI function calling *without* using MCP. This is a baseline example.
    *   **How it works**:
        *   The weather and datetime functions are defined directly within this script (not in a separate server).
        *   When the OpenAI model requests a function call, this script executes the corresponding local Python function directly.
        *   This approach is simpler for basic cases but doesn't scale as well or offer the standardization benefits of MCP.

4.  **`openai_function_calling_with_langchain.py`**:
    *   **Purpose**: Integrates MCP tools with OpenAI using the LangChain library. LangChain provides helpful abstractions for building LLM applications.
    *   **How it works**:
        *   Uses `langchain-mcp-adapters` to load the tools from the running `mcp_server.py` into a format LangChain understands.
        *   Binds these tools to the LangChain OpenAI model wrapper.
        *   Manually manages the conversation loop: sends the user message, checks if the model wants to call tools, executes them via MCP if needed, sends results back, and repeats until a final answer is generated.
        *   This shows a more structured way to handle the tool-calling process compared to the pure MCP example.

5.  **`openai_function_calling_with_langchain_langgraph.py`**:
    *   **Purpose**: Shows a more advanced integration using LangChain and LangGraph. LangGraph helps create complex, stateful agent-like applications.
    *   **How it works**:
        *   Loads MCP tools similarly using `langchain-mcp-adapters`.
        *   Uses LangGraph's `create_react_agent` function. This function takes the model and tools and automatically creates an "agent" that handles the entire loop of receiving messages, deciding to call tools, executing them, and generating the final response.
        *   This significantly simplifies the code, as LangGraph manages the conversation flow and tool execution logic internally.

## Requirements

*   Python 3.10 or newer
*   An OpenAI API Key or OpenAI compatible LLM

## Setup Instructions

1.  **Clone the Repository**: If you haven't already, get the code onto your computer.
    ```bash
    git clone <repository-url>
    cd <repository-directory>
    ```

2.  **Install Dependencies**: This project uses several Python libraries listed in `requirements.txt`. Install them using pip:
    ```bash
    pip install -r requirements.txt
    ```
    *Why?* This command reads the list of required libraries and their versions and installs them into your Python environment, ensuring the scripts have everything they need to run.

3.  **Set Up Environment Variables**: You need to provide your OpenAI API key securely.
    *   Copy the example environment file:
        ```bash
        # On Windows (Command Prompt)
        copy .env.example .env
        # On Windows (PowerShell)
        Copy-Item .env.example .env
        # On macOS/Linux
        cp .env.example .env
        ```
    *   Open the newly created `.env` file in a text editor.
    *   Replace `"your_openai_api_key"` with your actual OpenAI API key.
    *   (Optional) You can also change the `OPENAI_MODEL_NAME` if you want to use a different model like `gpt-4`.
    *Why?* Storing sensitive information like API keys in a `.env` file is a standard practice. It keeps your keys out of your code and prevents accidentally sharing them. The scripts are configured to automatically load variables from this file.

## Running the Examples

**Important**: For the examples that use MCP (`openai_function_calling_with_mcp.py`, `openai_function_calling_with_langchain.py`, `openai_function_calling_with_langchain_langgraph.py`), you **must** start the MCP server first in a separate terminal window.

1.  **Start the MCP Server (if needed)**:
    *   Open a terminal or command prompt.
    *   Navigate to the project directory.
    *   Run the server:
        ```bash
        python mcp_server.py
        ```
    *   Leave this terminal window open. It's now listening for connections from the client scripts.

2.  **Run an Example Script**:
    *   Open a **new** terminal or command prompt window.
    *   Navigate to the project directory.
    *   Choose one of the example scripts and run it:

        *   **MCP Example (requires server running):**
            ```bash
            python openai_function_calling_with_mcp.py
            ```
        *   **Direct Example (no server needed):**
            ```bash
            python openai_function_calling.py
            ```
        *   **LangChain Example (requires server running):**
            ```bash
            python openai_function_calling_with_langchain.py
            ```
        *   **LangChain + LangGraph Example (requires server running):**
            ```bash
            python openai_function_calling_with_langchain_langgraph.py
            ```

    *   **Expected Output**: Each script will print information about the tools it finds (if applicable) and the conversation flow. It will show when the model decides to call a tool, the arguments it provides, the result returned by the tool, and finally, the model's answer incorporating the tool's information (e.g., "The weather in Shanghai is ... and the current date/time is ...").

## License

This project is licensed under the MIT License. See the LICENSE file for details.
