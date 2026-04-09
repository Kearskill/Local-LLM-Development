# main.py
from src import CopilotEngine, KnowledgeBase, search_kb


def start_app():
    # Initialize the local KB on your RTX 3050
    kb = KnowledgeBase(path="./chroma_db")

    # Initialize the LLM engine
    bot = CopilotEngine(model="llama3.1")

    print(f"Helpdesk Copilot v{src.__version__} is online.")
    # ... rest of your loop