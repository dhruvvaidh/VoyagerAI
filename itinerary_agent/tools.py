import os
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset,SseServerParams
from google.adk.tools.agent_tool import AgentTool
from .maps_agent.agent import maps_agent

tripadvisor_tool= MCPToolset(
    connection_params=SseServerParams(  
        url=os.getenv('TRIPADVISOR_MCP'),
    )
)

openweather_tool= MCPToolset(
    connection_params=SseServerParams( 
        url=os.getenv('OPENWEATHER_MCP'),
    )
)

google_maps_tool = AgentTool(maps_agent)