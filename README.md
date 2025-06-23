VoyagerAI ✈️ — Multi-Agent Travel Planner

VoyagerAI is a server-side multi-agent system that finds flights, hotels (or Airbnbs) and builds a personalised day-by-day itinerary.
Under the hood it uses Google’s Agent Development Kit, Gemini models, and a handful of MCP servers that wrap external APIs.

<p align="center">
  <img width="640" src="VoyagerAI.pdf" alt="High-level architecture">
</p>



⸻

Features

Agent	LLM	External tools
Flights	gemini-2.5-flash	• Flight Search MCP (skarlekar/mcp_travelassistant)
Accommodation	gemini-2.0-flash	• Booking Scraper MCP (hotels)  • Smithery Airbnb MCP
Itinerary	gemini-2.0-flash	• Tripadvisor Content API MCP  • Google Maps MCP
Aggregator	gemini-2.5-flash	—


⸻

1  Quick start

1.1 Clone & install


```git clone https://github.com/your-handle/VoyagerAI.git
cd VoyagerAI
python -m venv venv
source venv/bin/activate        #  Windows: .\venv\Scripts\activate
pip install -r requirements.txt```


1.2 Create .env

Copy the template and add your keys:

```
cp .env.example .env
nano .env          # or any editor```

<table>
<tr><th>Variable</th><th>What it is</th></tr>
<tr><td><code>TRIPADVISOR_MCP</code></td><td>pipedream MCP endpoint for Tripadvisor</td></tr>
<tr><td><code>GOOGLE_API_KEY</code></td><td>Gemini API key from Google AI Studio <br><em>(set <code>GOOGLE_GENAI_USE_VERTEXAI=TRUE</code> if you use Vertex AI)</em></td></tr>
<tr><td><code>GOOGLE_MAPS_API_KEY</code></td><td>Maps SDK key</td></tr>
<tr><td><code>SERPAPI_API_KEY</code></td><td>SerpAPI (used by flight MCP)</td></tr>
<tr><td><code>SMITHERY_API_KEY</code></td><td>Smithery.ai key for Airbnb MCP</td></tr>
<tr><td><code>APIFY_API_TOKEN</code></td><td>Token for Booking Scraper MCP</td></tr>
<!-- more in the template -->
</table>



⸻

2  Run in the terminal

python runner_cli.py

✈️  Interactive VoyagerAI CLI – type 'exit' to quit

You: plan a 5-day luxury trip to Amsterdam in August
VoyagerAI: <trip_document> … </trip_document>

The CLI preserves conversation state, so follow-up questions (“Make the hotel cheaper”) work.

⸻

3  Run the Streamlit web chat

```streamlit run streamlit_app.py```

	•	Press Enter to send messages.
	•	When VoyagerAI produces the <trip_document> it is shown below the chat as a nicely formatted itinerary.

⸻


4  Project structure

VoyagerAI/
│
├─ VoyagerAI/                     # Python package
│   ├─ agent.py                   # root_agent (SequentialAgent)
│   ├─ sub_agents/
│   │   ├─ trip_planner/…         # planner & its sub-agents
│   │   └─ aggregator/…           # final compiler
│   └─ shared/schema.py           # Pydantic models
│
├─ runner_cli.py                  # coloured terminal chat
├─ streamlit_app.py               # web UI
├─ requirements.txt
└─ .env.example

⸻

5  Acknowledgements & resources
	•	Google ADK  – framework for agent composition
	•	Gemini models  – LLM reasoning
	•	Tripadvisor Content API( https://www.tripadvisor.com/developers) & Pipedream MCP (https://mcp.pipedream.com/app/tripadvisor_content_api)
	•	Google Maps Platform
	•	Booking Scraper MCP (Apify)(https://apify.com/voyager/booking-scraper)
	•	Smithery Airbnb MCP(https://smithery.ai/server/@openbnb-org/mcp-server-airbnb )
	•	Flight Search MCP by skarlekar(https://github.com/skarlekar/mcp_travelassistant/tree/main)

Feel free to open issues or PRs. Enjoy your AI-planned adventures!