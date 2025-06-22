from google.adk.agents.llm_agent import Agent
from .instructions import ITINERARY_PROMPT
from .tools import openweather_tool,tripadvisor_tool,google_maps_tool

root_agent = Agent(
    model="gemini-2.0-flash",
    name="itinerary_agent",
    instruction=ITINERARY_PROMPT,
    tools=[openweather_tool,
           tripadvisor_tool,
           google_maps_tool
           ],
)