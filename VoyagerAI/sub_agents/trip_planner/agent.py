from google.adk.agents import Agent
from google.adk.tools.agent_tool import AgentTool
from .instructions import TRIP_PLANNER_PROMPT

from .sub_agents.flight_agent.agent import flight_agent
from .sub_agents.accomodation_agent.agent import accomodation_agent
from .sub_agents.itinerary_agent.agent import itinerary_agent


# The manager Agent basically reads through the descriptions of all the other agents 
# to figure out which one should be selected to perform the Task

# Agents in ADK work in a different way, instead of using multiple agents to do one task, 
# it focuses on delegating the task to the best agent possible. 
# There are workarounds to this for adding complex workflows like parallel, sequential and loops.

trip_planner = Agent(
    name="trip_planner",
    model="gemini-2.0-flash",
    description="Manager agent",
    instruction=TRIP_PLANNER_PROMPT,
    sub_agents=[flight_agent, accomodation_agent,itinerary_agent],
)