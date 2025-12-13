from openai import OpenAI
from dotenv import load_dotenv
import os
from prompts import DEVOPS_PROMPT

# Force load .env from current directory
load_dotenv(dotenv_path=".env", override=True)

print("DEBUG API KEY:", os.getenv("OPENAI_API_KEY"))

client = OpenAI()

def devops_assistant(query):
    prompt = DEVOPS_PROMPT.format(query=query)

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content


if __name__ == "__main__":
    print("🚀 LLM-Based DevOps Assistant\n")
    while True:
        q = input("DevOps Query → ")
        if q.lower() == "exit":
            break
        print(devops_assistant(q))
