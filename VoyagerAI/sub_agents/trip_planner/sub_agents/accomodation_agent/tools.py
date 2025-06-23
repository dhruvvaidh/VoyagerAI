import os
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset, SseServerParams, StdioServerParameters

hotels_tool = MCPToolset(
    connection_params=StdioServerParameters(
        command="npx",
        args=[
            "-y",                     
            "mcp-remote",
            "https://mcp.apify.com/sse?actors=voyager/booking-scraper",
            "--header",
            f"Authorization: Bearer {os.getenv('APIFY_API_TOKEN')}",
        ],
        # optional but nice – give the remote 30 s to start
        startup_timeout_seconds=30,
    )
)

# hotels_tool = MCPToolset(
#     connection_params=SseServerParams(
#         url="https://mcp.apify.com/sse?actors=voyager/booking-scraper",
#         headers={
#             "Authorization": f"Bearer {os.getenv("APIFY_API_TOKEN")}"
#             },
#     )
# )

airbnb_tools = MCPToolset(
    connection_params=StdioServerParameters(
        command="npx",
        args=[
            "-y",
            "@smithery/cli@latest",
            "run",
            "@openbnb-org/mcp-server-airbnb",
            "--key",
            os.getenv("SMITHERY_API_KEY"),
            ],
    )
)