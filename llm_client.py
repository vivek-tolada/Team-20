import traceback
from .config import LLM_MODE, DEFAULT_MODEL, GROQ_API_KEY


class LLMClient:
    def __init__(self, provider=LLM_MODE, model=DEFAULT_MODEL):
        self.provider = provider
        self.model = model

    def generate(self, prompt: str, max_tokens=800, temperature=0.2):
        """
        HYBRID LOGIC:
        1. If provider is mock → always return mock immediately
        2. If provider is groq → try real AI, fallback to mock if:
             - API key missing
             - model invalid
             - timeout
             - network error
             - any exception
        """

        # MOCK MODE ALWAYS SAFE
        if self.provider == "mock":
            return self._mock_response(prompt)

        # GROQ MODE WITH FALLBACK
        if self.provider == "groq":
            try:
                return self._groq_generate(prompt, max_tokens, temperature)
            except Exception as e:
                print("\n🔥 GROQ FAILED — FALLING BACK TO MOCK MODE 🔥")
                print("Error:", e)
                print(traceback.format_exc())
                return self._mock_response(prompt)

        return "Invalid provider mode."


    # ----------------------------------------------------------------------
    # REAL GROQ AI MODE
    # ----------------------------------------------------------------------
    def _groq_generate(self, prompt, max_tokens, temperature):

        # Missing key → immediate fallback
        if not GROQ_API_KEY:
            raise Exception("Missing GROQ_API_KEY!")

        from groq import Groq  # Requires: pip install groq

        client = Groq(api_key=GROQ_API_KEY)

        print("Calling Groq real model...")

        # TIMEOUT PREVENTS INFINITE LOADING
        response = client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "You are a senior DevOps engineer."},
                {"role": "user", "content": prompt},
            ],
            max_tokens=max_tokens,
            temperature=temperature,
            timeout=5  # IMPORTANT! ensures fallback after 5 seconds
        )

        return response.choices[0].message["content"]


    # ----------------------------------------------------------------------
    # MOCK MODE — ALWAYS WORKS, ALWAYS SAFE
    # ----------------------------------------------------------------------
    def _mock_response(self, prompt: str) -> str:
        p = prompt.lower()

        # Dockerfile mock output
        if "dockerfile" in p:
            return (
                "FROM python:3.10-slim\n"
                "WORKDIR /app\n"
                "COPY . .\n"
                "RUN pip install -r requirements.txt\n"
                "CMD [\"uvicorn\", \"main:app\", \"--host\", \"0.0.0.0\", \"--port\", \"8000\"]"
            )

        # GitHub Actions mock output
        if "github actions" in p or "ci/cd" in p:
            return (
                "name: CI\n"
                "on: [push]\n"
                "jobs:\n"
                "  build:\n"
                "    runs-on: ubuntu-latest\n"
                "    steps:\n"
                "      - uses: actions/checkout@v3\n"
                "      - run: pip install -r requirements.txt\n"
                "      - run: pytest"
            )

        # PR Review mock output
        if "review" in p:
            return (
                "Issue: Missing error handling.\n"
                "Severity: Medium\n"
                "Suggestion: Add try/except around risky operations."
            )

        # Default fallback
        return "MOCK: Generated fallback output"
