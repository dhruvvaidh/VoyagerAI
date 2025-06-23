from google.adk.agents.llm_agent import Agent
from .instructions import ITINERARY_PROMPT
from .tools import tripadvisor_tool,google_maps_tool
from VoyagerAI.shared.schema import DayPlan
from google.adk.agents.callback_context import CallbackContext
import json

def _format_for_schema(raw: list[dict]) -> list[dict]:
    """
    Convert the list of daily plans produced by the LLM into a list
    of DayPlan objects, then back to plain dicts for JSON-safe storage.
    Expected `raw` shape (adjust if your prompt outputs differently):

        [
          {"day": 1, "plan": "Morning canal cruise …"},
          {"day": 2, "plan": "Day trip to Rotterdam …"},
          …
        ]
    """
    return [DayPlan(**d).model_dump() for d in raw]

def _stash_in_memory(ctx: CallbackContext):
    """
    • LLM outputs a JSON array of daily plans.
    • Validate against DayPlan schema.
    • Store in ctx.state['itinerary_info'] for the aggregator.
    """
    raw_plans = json.loads(ctx.response.parts[0].text)
    ctx.state["itinerary_info"] = _format_for_schema(raw_plans)

itinerary_agent = Agent(
    model="gemini-2.0-flash",
    name="itinerary_agent",
    description="""An AI travel agent that designs personalized itineraries using user preferences, 
    Tripadvisor data, and Google Maps routing. It builds logical day-by-day plans with realistic travel flows, 
    activity matching, and local recommendations.""",
    instruction=ITINERARY_PROMPT,
    tools=[tripadvisor_tool,
           google_maps_tool
           ],
    after_agent_callback=_stash_in_memory
)