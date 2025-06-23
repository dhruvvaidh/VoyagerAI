from google.adk.agents.llm_agent import Agent
from .instructions import FLIGHTS_PROMPT
from .tools import flights_tool,airport_code_tool,airport_names_tool
# flights_agent/agent.py
from VoyagerAI.shared.schema import FlightInfo, FlightLeg
from google.adk.agents.callback_context import CallbackContext
import json

def _format_for_schema(raw: dict) -> dict:
    """
    Convert the single ‘best’ flight returned by flights_tool
    into the FlightInfo → dict expected by the aggregator.
    """
    outbound_leg = FlightLeg(
        depart_airport = raw["outbound"]["from"],
        arrive_airport = raw["outbound"]["to"],
        depart_time    = raw["outbound"]["depart_at"],
        arrive_time    = raw["outbound"]["arrive_at"],
        airline        = raw["outbound"]["airline"],
        flight_number  = raw["outbound"]["flight_number"],
    )

    return_leg = FlightLeg(
        depart_airport = raw["return"]["from"],
        arrive_airport = raw["return"]["to"],
        depart_time    = raw["return"]["depart_at"],
        arrive_time    = raw["return"]["arrive_at"],
        airline        = raw["return"]["airline"],
        flight_number  = raw["return"]["flight_number"],
    ) if raw.get("return") else None

    fi = FlightInfo(
        outbound      = outbound_leg,
        return_       = return_leg,
        price         = float(raw["price"]),
        booking_link  = raw["link"] or None,
    )
    return fi.model_dump()

def _stash_in_memory(ctx: CallbackContext):
    """
    • ctx.response.parts[0].text is expected to be JSON from the LLM.
    • Select the dict with `"best": true` (fallback to first item).
    • Convert → FlightInfo → dict and store in ctx.state.
    """
    flights = json.loads(ctx.response.parts[0].text)
    best    = next((f for f in flights if f.get("best")), flights[0])

    ctx.state["flight_info"] = _format_for_schema(best)

flight_agent = Agent(
    model="gemini-2.5-flash",
    name="flight_agent",
    description="""An AI flight booking assistant that analyzes user preferences and uses a local MCP server 
    to find optimal flight options. It intelligently handles missing inputs, filters results, and recommends top 
    flights with detailed insights.""",
    instruction=FLIGHTS_PROMPT,
    tools=[flights_tool,airport_code_tool,airport_names_tool],
    after_agent_callback=_stash_in_memory
)