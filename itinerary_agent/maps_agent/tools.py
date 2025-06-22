import os
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset, StdioServerParameters

google_maps_tool = MCPToolset(
            connection_params=StdioServerParameters(
                command='npx',
                args=[
                    "-y",
                    "@modelcontextprotocol/server-google-maps",
                ],
                # Pass the API key as an environment variable to the npx process
                # This is how the MCP server for Google Maps expects the key.
                env={
                    "GOOGLE_MAPS_API_KEY": os.getenv('GOOGLE_MAPS_API_KEY')
                }
            )
)