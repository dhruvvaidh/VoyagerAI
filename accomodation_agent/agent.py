from google.adk.agents.llm_agent import Agent
from .instructions import HOTEL_PROMPT
from .tools import hotels_tool,airbnb_tools

root_agent = Agent(
    model="gemini-2.0-flash",
    description="""
    The Accommodation Agent prompts users to choose between hotels or Airbnbs and gathers their location, dates, 
    guest count, amenities, and price preferences. It validates and refines any missing or inconsistent details, 
    maps these preferences to search filters, and then calls the appropriate MCP tool (hotels_tool for hotels or 
    airbnb_tools for listings) with a complete set of parameters.
""",
    name="accomodation_agent",
    instruction=HOTEL_PROMPT,
    tools=[hotels_tool,airbnb_tools],
)