# server.py
import asyncio
import logging
from mcp.server.fastmcp import FastMCP
from utils import get_weather, get_current_datetime

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Create an MCP server
logger.debug("Creating FastMCP instance")
mcp = FastMCP("Demo")


# Add an addition tool
@mcp.tool()
def get_weather_tool(city: str) -> dict:
    """Get the current weather for a specific city"""
    return get_weather(city)


@mcp.tool()
def get_current_datetime_tool() -> str:
    """Get the current date and time"""
    return get_current_datetime()


if __name__ == "__main__":
    # Initialize and run the server
    mcp.run(transport="stdio")

# if __name__ == "__main__":
#     loop = asyncio.get_event_loop()
#     loop.run_until_complete(mcp.run_stdio_async())
