"""
Prompt Builder:
Creates structured prompts for:
1. DevOps template generation (Dockerfile, CI/CD, K8s, Terraform)
2. Pull request review
3. Documentation generation
"""

# Example templates for higher quality prompting
TEMPLATE_EXAMPLES = {
    "dockerfile": {
        "example": """
FROM python:3.10-slim
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
        """,
        "description": "Basic Python FastAPI Dockerfile"
    },
    "github_actions": {
        "example": """
name: CI
on: [push, pull_request]
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'
      - run: pip install -r requirements.txt
      - run: pytest -q
        """,
        "description": "Python CI pipeline example"
    }
}


# -------------------- TEMPLATE GENERATION --------------------
def build_template_prompt(project_type: str, artifact: str, details: dict) -> str:
    artifact = artifact.lower()

    # Combine details into a readable list
    details_text = "\n".join([f"- {key}: {value}" for key, value in details.items()])

    example = TEMPLATE_EXAMPLES.get(artifact, {}).get("example", "")
    description = TEMPLATE_EXAMPLES.get(artifact, {}).get("description", "No example available")

    prompt = f"""
You are a senior DevOps engineer. Your task is to generate a professional-quality **{artifact}** file.

Project Type: {project_type}

Requirements:
{details_text}

Rules:
- Return ONLY the {artifact} file.
- No explanations, no commentary.
- Use correct syntax and indentation.
- Ensure the file is production-ready.

Example ({description}):
{example}

Now generate the {artifact} file for the project described.
"""
    return prompt



# -------------------- PR REVIEW --------------------
def build_pr_review_prompt(diff: str, language: str = "python") -> str:
    prompt = f"""
You are an experienced senior engineer and security reviewer.

Analyze the following pull request diff and produce:
1. List of issues (bugs, risks, code smells, vulnerabilities)
2. Severity (Low / Medium / High)
3. Suggested fix

Return output in clear bullet points.

DIFF:
{diff}
"""
    return prompt



# -------------------- DOCUMENTATION GENERATION --------------------
def build_docs_prompt(repo_summary: str) -> str:
    prompt = f"""
You are a technical writer responsible for generating excellent project documentation.

Using the repository summary below, generate a complete README.md containing:
- Project Overview
- Features
- Architecture (text explanation)
- Installation steps
- Run instructions
- Deployment guide
- API Reference (if applicable)
- Folder structure explanation

Repository Summary:
{repo_summary}

Return ONLY valid Markdown.
"""
    return prompt
