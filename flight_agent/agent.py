from google.adk.agents.llm_agent import Agent
from .instructions import FLIGHTS_PROMPT
from .tools import flights_tool,airport_code_tool,airport_names_tool

root_agent = Agent(
    model="gemini-2.5-flash",
    name="flight_agent",
    instruction=FLIGHTS_PROMPT,
    tools=[flights_tool,airport_code_tool,airport_names_tool],
)