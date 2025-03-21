# OpenAI Function Calling with MCP

This project demonstrates integrating OpenAI's function calling with MCP (Model Context Protocol).

## Overview

The project demonstrates OpenAI function calling through two different implementations:

1. **With MCP (Model Context Protocol)**
   - `mcp_server.py`: Implements an MCP server with two tools:
     - `get_weather_tool`: Gets current weather for a specified city
     - `get_current_datetime_tool`: Gets current date and time
   - `openai_function_calling_with_mcp.py`: Demonstrates OpenAI function calling using MCP by:
     - Initializing OpenAI client
     - Connecting to MCP server
     - Listing available tools
     - Handling tool calls from OpenAI

2. **Direct Implementation**
   - `openai_function_calling.py`: Demonstrates OpenAI function calling without MCP by:
     - Defining functions directly in the code
     - Handling tool calls from OpenAI
     - Using utility functions directly

## Requirements

- Python 3.7+
- Required packages (see `requirements.txt`)

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Create a `.env` file based on `.env.example` and fill in your OpenAI API credentials.

3. Run the MCP server:
   ```bash
   python mcp_server.py
   ```

4. Run the OpenAI function calling demo:
   ```bash
   python openai_function_calling_with_mcp.py
   ```

## Example Usage

The demo will ask OpenAI about the weather in Shanghai and the current date/time. The OpenAI model will call the appropriate MCP tools to get the information.

## License

MIT License (see LICENSE file)
