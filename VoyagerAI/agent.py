from google.adk.agents import SequentialAgent

from .sub_agents.trip_planner.agent import trip_planner
from .sub_agents.aggregator.agent import aggregator

# In sequential agents, the order sub-agents in the list is the order of execution of these sub-agents

root_agent = SequentialAgent(
    name="VoyagerAI",
    sub_agents=[trip_planner, aggregator],
    description="A pipeline that plans trips, travel and flights then aggregates all that information into a single document",
)