from google.adk.agents.llm_agent import Agent
from .instructions import MAPS_PROMPT
from .tools import google_maps_tool

maps_agent = Agent(
    model="gemini-2.0-flash",
    description="The Google Maps Agent helps plan routes, estimate travel times, and find nearby points of interest using the Google Maps API. It converts location names into coordinates and provides accurate, real-time routing and distance information using the Google Maps API",
    name="maps_agent",
    instruction=MAPS_PROMPT,
    tools=[google_maps_tool]
)