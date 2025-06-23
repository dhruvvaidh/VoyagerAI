import os
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset,SseServerParams, StdioServerParameters
# from google.adk.tools.agent_tool import AgentTool
# from .maps_agent.agent import maps_agent

tripadvisor_tool= MCPToolset(
    connection_params=SseServerParams(  
        url=os.getenv('TRIPADVISOR_MCP'),
    )
)

# openweather_tool= MCPToolset(
#     connection_params=SseServerParams( 
#         url=os.getenv('OPENWEATHER_MCP'),
#     )
# )

google_maps_tool = MCPToolset(
            connection_params=StdioServerParameters(
                command='npx',
                args=[
                    "-y",
                    "@modelcontextprotocol/server-google-maps",
                ],
                env={
                    "GOOGLE_MAPS_API_KEY": os.getenv('GOOGLE_MAPS_API_KEY')
                }
            )
)


# google_maps_tool = AgentTool(maps_agent)

# weather_tool = MCPToolset(
#             connection_params=StdioServerParameters(
#                 command="uvx",
#                 args=["--from", "git+https://github.com/adhikasp/mcp-weather.git", "mcp-weather"],
#                 env={"ACCUWEATHER_API_KEY": os.getenv('ACCUWEATHER_API_KEY')},
#             )
# )