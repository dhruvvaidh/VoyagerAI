import uuid, asyncio
from pathlib import Path
from dotenv import load_dotenv
import logging, warnings
warnings.filterwarnings("ignore", category=RuntimeWarning)

logging.getLogger("google.adk").setLevel(logging.ERROR)
logging.getLogger("anyio").setLevel(logging.ERROR) 


from colorama import init as colorama_init, Fore, Style  
colorama_init()                                              

env_path = Path(__file__).resolve().parent / ".env"
load_dotenv(dotenv_path=env_path)

from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types
from VoyagerAI.agent import root_agent

APP_NAME        = "VoyagerAI"
session_service = InMemorySessionService()
runner          = Runner(agent=root_agent, app_name=APP_NAME, session_service=session_service)

user_id    = "demo_user"
session_id = str(uuid.uuid4())

asyncio.run(session_service.create_session(
    app_name=APP_NAME,
    user_id=user_id,
    session_id=session_id,
    state={}
))

U = Fore.GREEN   + Style.BRIGHT   # User text → bright green
V = Fore.CYAN    + Style.BRIGHT   # Voyager text → bright cyan
R = Style.RESET_ALL               # Reset to default terminal style

print(f"{V}Interactive VoyagerAI CLI – type 'exit' to quit{R}\n")

while True:
    user_text = input(f"{U}You:{R} ")
    if user_text.lower() in {"exit", "quit"}:
        break

    new_msg = types.Content(role="user", parts=[types.Part(text=user_text)])

    for ev in runner.run(user_id=user_id, session_id=session_id, new_message=new_msg):
        if ev.is_final_response() and ev.content.parts:
            reply = ev.content.parts[0].text
            print(f"\n{V}VoyagerAI:{R} {reply}\n")