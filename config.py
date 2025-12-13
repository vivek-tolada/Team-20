import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
LLM_MODE = os.getenv("LLM_MODE", "groq")  # "openai" or "mock"
DEFAULT_MODEL = os.getenv("DEFAULT_MODEL", "llama3-70b-8192")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")  # Paste your key here
print("Loaded Groq key:", GROQ_API_KEY)
