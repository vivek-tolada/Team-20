from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, Dict

from .llm_client import LLMClient
from .prompt_builder import (
    build_template_prompt,
    build_pr_review_prompt,
    build_docs_prompt
)
from .validators import (
    is_yaml,
    try_fix_yaml,
    is_json,
    pretty_json,
    basic_dockerfile_check
)
from .config import LLM_MODE, DEFAULT_MODEL

app = FastAPI(title="DevOps Copilot API")

# Create LLM engine
llm = LLMClient(provider=LLM_MODE, model=DEFAULT_MODEL)


# -------------------- MODELS --------------------
class TemplateRequest(BaseModel):
    project_type: str
    artifact: str
    details: Optional[Dict] = None


class PRReviewRequest(BaseModel):
    diff: str
    language: Optional[str] = "python"


class DocsRequest(BaseModel):
    repo_summary: str


# -------------------- TEMPLATE GENERATION --------------------
@app.post("/api/generate/template")
async def generate_template(req: TemplateRequest):
    prompt = build_template_prompt(req.project_type, req.artifact, req.details or {})
    out = llm.generate(prompt)

    # Dockerfile
    if req.artifact.lower() == "dockerfile":
        valid, warnings = basic_dockerfile_check(out)
        return {
            "artifact_type": req.artifact,
            "valid": valid,
            "warnings": warnings,
            "content": out
        }

    # YAML auto-fix
    if is_yaml(out):
        fixed = try_fix_yaml(out)
        return {"artifact_type": req.artifact, "valid": True, "content": fixed}

    # JSON auto-pretty
    if is_json(out):
        return {"artifact_type": req.artifact, "valid": True, "content": pretty_json(out)}

    # Generic plaintext fallback
    return {"artifact_type": req.artifact, "valid": True, "content": out}


# -------------------- PR REVIEW --------------------
@app.post("/api/review/pr")
async def review_pr(req: PRReviewRequest):
    prompt = build_pr_review_prompt(req.diff, req.language)
    out = llm.generate(prompt)
    return {"review": out}


# -------------------- DOCUMENTATION --------------------
@app.post("/api/generate/docs")
async def generate_docs(req: DocsRequest):
    prompt = build_docs_prompt(req.repo_summary)
    out = llm.generate(prompt)
    return {"readme": out}


# -------------------- CHAT ASSISTANT --------------------
@app.post("/api/chat")
async def chat(payload: Dict):
    message = payload.get("message", "")
    if not message:
        raise HTTPException(status_code=400, detail="message missing")

    prompt = f"You are a senior DevOps engineer.\nUser: {message}\n"
    out = llm.generate(prompt)

    return {"reply": out}


# -------------------- GITHUB PR CREATION --------------------
@app.post("/api/github/create_pr")
async def create_pr(payload: Dict):
    from .github_client import GitHubClient

    repo = payload.get("repo")
    branch = payload.get("branch", "ai-generated-devops")
    base = payload.get("base", "main")
    files = payload.get("files", {})
    title = payload.get("title", "AI Generated DevOps Files")
    body = payload.get("body", "This PR contains AI-generated DevOps resources.")

    if not repo or not files:
        raise HTTPException(
            status_code=400,
            detail="repo and files fields are required."
        )

    gh = GitHubClient()

    try:
        pr_url = gh.create_branch_and_pr(
            repo_full_name=repo,
            base_branch=base,
            new_branch=branch,
            files=files,
            pr_title=title,
            pr_body=body
        )
        return {"pr_url": pr_url}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
