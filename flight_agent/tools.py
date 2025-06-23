import os
from .airport_code_lookup import get_iata_code, get_airport_name
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset, StdioServerParameters
from google.adk.tools import FunctionTool
from pathlib import Path



current_dir = Path().cwd()
server_dir = current_dir/"flight_server"

flights_tool = MCPToolset(
    connection_params=StdioServerParameters(
        command="python",
        args=["flight_server.py"],
        cwd=str(server_dir),
        env={"SERPAPI_KEY": os.getenv('SERPAPI_API_KEY')},
    )
)



airport_code_tool = FunctionTool(func=get_iata_code)
airport_names_tool = FunctionTool(func=get_airport_name)