AGGREGATOR_PROMPT = """
You will receive one JSON blob inside <trip_json> tags:

<trip_json>
{{TRIP_JSON?}}
</trip_json>

Transform it into a **clear, well-formatted** trip brief with:
• Trip overview
• Day-by-day itinerary
• Accommodation details
• Flight summary

Wrap the entire finished text in <trip_document> tags.
"""