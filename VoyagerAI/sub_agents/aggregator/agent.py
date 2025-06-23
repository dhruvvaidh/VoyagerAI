from google.adk.agents.llm_agent import Agent
from .instructions import AGGREGATOR_PROMPT
from VoyagerAI.shared.schema import AggregatedTrip
from google.adk.agents.callback_context import CallbackContext
import json

def _build_trip_doc(ctx: CallbackContext):
    """
    Gather the JSON slices written by sibling agents, validate them via
    AggregatedTrip, and expose the combined blob as {{TRIP_JSON}} for
    the LLM prompt.
    """
    trip = AggregatedTrip(
        flight_info        = ctx.state.get("flight_info"),
        accommodation_info = ctx.state.get("accommodation_info"),
        itinerary_info     = ctx.state.get("itinerary_info"),
    )
    ctx.variables["TRIP_JSON"] = json.dumps(trip.model_dump())

aggregator = Agent(
    name        = "aggregator",
    model       = "gemini-2.5-flash",
    description = "Compiles sub-agent results into one document",
    instruction = AGGREGATOR_PROMPT,
    before_agent_callback=_build_trip_doc
)