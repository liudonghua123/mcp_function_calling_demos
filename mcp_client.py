from contextlib import asynccontextmanager, AsyncExitStack
from types import TracebackType
from mcp import ClientSession, StdioServerParameters, stdio_client

class McpClient:
    def __init__(self, server_command="python", server_args=["mcp_server.py"]):
        self.server = StdioServerParameters(
            command=server_command,
            args=server_args
        )
        self._client_session = None
        self._exit_stack = None

    @asynccontextmanager
    async def initialize(self):
        """Initialize the client connection using AsyncExitStack"""
        # Not works, RuntimeError: Attempted to exit cancel scope in a different task than it was entered in
        # rewrite the code without "async with", see also https://github.com/langchain-ai/langchain-mcp-adapters/blob/main/langchain_mcp_adapters/client.py#L221-L228
        # self._exit_stack = AsyncExitStack()
        # try:
        #     read, write = await self._exit_stack.enter_async_context(stdio_client(self.server))
        #     mcp_client = await self._exit_stack.enter_async_context(ClientSession(read, write))
        #     await mcp_client.initialize()
        #     self._client_session = mcp_client
        #     yield mcp_client
        #     # self._exit_stack.pop_all() # This line does not fix the issue too.
        # except Exception as e:
        #     await self._exit_stack.aclose()
            
        # works without errors
        async with AsyncExitStack() as stack:
            read, write = await stack.enter_async_context(stdio_client(self.server))
            mcp_client = await stack.enter_async_context(ClientSession(read, write))
            await mcp_client.initialize()
            self._client_session = mcp_client
            yield mcp_client

    async def call_tool(self, name, arguments):
        """Call a tool by name with given arguments"""
        if not self._client_session:
            raise RuntimeError("Client not initialized")
        return await self._client_session.call_tool(name=name, arguments=arguments)

    async def list_tools(self):
        """List available tools"""
        if not self._client_session:
            raise RuntimeError("Client not initialized")
        return await self._client_session.list_tools()

    @classmethod
    @asynccontextmanager
    async def get_mcp_client(cls):
        """Backward compatible context manager"""
        client = cls()
        async with client.initialize() as session:
          yield session

    
    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        print("Exiting MCP Client")
        await self._exit_stack.aclose()
