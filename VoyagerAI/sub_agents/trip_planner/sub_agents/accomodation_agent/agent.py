from google.adk.agents.llm_agent import Agent
from .instructions import HOTEL_PROMPT
from .tools import hotels_tool,airbnb_tools
from VoyagerAI.shared.schema import AccommodationInfo
from google.adk.agents.callback_context import CallbackContext
import json

def _format_for_schema(raw: dict) -> dict:
    """
    Convert the single ‘best’ hotel returned by your MCP tool
    into the pydantic AccommodationInfo → dict expected by the aggregator.
    """
    ai = AccommodationInfo(
        name         = raw["name"],
        check_in     = raw["check_in_date"],   # YYYY-MM-DD
        check_out    = raw["check_out_date"],  # YYYY-MM-DD
        price        = float(raw["total_price"]),
        booking_link = raw["url"],
    )
    return ai.model_dump()

def _stash_in_memory(ctx: CallbackContext):
    """
    • Parses the LLM output (expected JSON)
    • Picks the item flagged `"best": true` (fallback to first element)
    • Saves it in ctx.state so sibling agents & aggregator can read it
    """
    # LLM output -> Python list/dict
    listings = json.loads(ctx.response.parts[0].text)

    # pick best (adjust selector if your prompt differs)
    best = next((r for r in listings if r.get("best")), listings[0])

    # validate & store
    ctx.state["accommodation_info"] = _format_for_schema(best)

accomodation_agent = Agent(
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
    after_agent_callback=_stash_in_memory
)