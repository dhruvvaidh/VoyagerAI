"""
Simple Streamlit front-end for VoyagerAI
───────────────────────────────────────────────────────────────────
• shows a chat window (user ↔ VoyagerAI)
• displays the final trip document once generated
"""

import asyncio, uuid, json, re
from pathlib import Path

import streamlit as st
from dotenv import load_dotenv
load_dotenv(dotenv_path=Path(__file__).parent / ".env")

from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

from VoyagerAI.agent import root_agent

APP_NAME = "VoyagerAI"
USER_ID  = "streamlit_user"

def init_adk():
    """Called exactly once per browser session."""
    session_service = InMemorySessionService()
    runner = Runner(
        agent           = root_agent,
        app_name        = APP_NAME,
        session_service = session_service,
    )

    session_id = str(uuid.uuid4())
    asyncio.run(
        session_service.create_session(
            app_name   = APP_NAME,
            user_id    = USER_ID,
            session_id = session_id,
            state      = {},               
        )
    )
    return runner, session_id


# ── 1. Streamlit session_state initialisation ────────────────────
if "runner" not in st.session_state:
    st.session_state["runner"], st.session_state["session_id"] = init_adk()
    st.session_state["messages"] = []      
    st.session_state["itinerary"] = None     


# ── 2. Helper: send a user message to ADK runner ─────────────────
def send_to_voyager(user_text: str):
    """Appends user text → calls runner → stores assistant reply(ies)."""
    runner      = st.session_state["runner"]
    session_id  = st.session_state["session_id"]

    # build ADK Content
    new_msg = types.Content(role="user", parts=[types.Part(text=user_text)])

    assistant_reply = ""
    for ev in runner.run(
        user_id     = USER_ID,
        session_id  = session_id,
        new_message = new_msg,
    ):
        if ev.is_final_response() and ev.content.parts:
            assistant_reply = ev.content.parts[0].text

    # save both sides of the turn
    st.session_state["messages"].append(("user", user_text))
    st.session_state["messages"].append(("assistant", assistant_reply))

    # detect final itinerary
    if "<trip_document>" in assistant_reply:
        trip_doc = re.sub(r"</?trip_document>", "", assistant_reply).strip()
        st.session_state["itinerary"] = trip_doc


# ── 3. Chat UI  ───────────────────────────────────────────────────
st.title("✈️ VoyagerAI – Trip Planner")

# Display chat history
for role, text in st.session_state["messages"]:
    with st.chat_message(role):
        st.markdown(text)

# Chat input box
if prompt := st.chat_input("Plan my trip…"):
    send_to_voyager(prompt)
    st.rerun()  # refresh UI with new messages

# ── 4. Show itinerary if present ─────────────────────────────────
if st.session_state["itinerary"]:
    st.divider()
    st.subheader("Your Trip Document")
    st.markdown(st.session_state["itinerary"])