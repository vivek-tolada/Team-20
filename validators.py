"""
Validators & fixers for DevOps artifacts:
- YAML validator & auto-fix
- JSON validator & auto-format
- Dockerfile basic checker
"""

import yaml
import json
import re


# -------------------- YAML VALIDATION --------------------
def is_yaml(text: str) -> bool:
    try:
        yaml.safe_load(text)
        return True
    except Exception:
        return False


def try_fix_yaml(text: str) -> str:
    """
    Attempt to load YAML and re-dump it properly formatted.
    This auto-fixes indentation issues and missing spacing.
    """
    try:
        obj = yaml.safe_load(text)
        fixed = yaml.safe_dump(obj, sort_keys=False)
        return fixed
    except Exception:
        return text  # If fixing fails, return original



# -------------------- JSON VALIDATION --------------------
def is_json(text: str) -> bool:
    try:
        json.loads(text)
        return True
    except Exception:
        return False


def pretty_json(text: str) -> str:
    try:
        obj = json.loads(text)
        return json.dumps(obj, indent=2)
    except Exception:
        return text



# -------------------- DOCKERFILE CHECK --------------------
def basic_dockerfile_check(text: str):
    """
    Very basic Dockerfile validation.
    Checks:
    - FROM exists
    - CMD or ENTRYPOINT exists
    - Optional warnings for RUN commands
    """

    warnings = []

    if not re.search(r"^FROM\s+", text, re.MULTILINE):
        warnings.append("Missing FROM instruction")

    if not (re.search(r"^CMD\s+", text, re.MULTILINE) or re.search(r"^ENTRYPOINT\s+", text, re.MULTILINE)):
        warnings.append("Missing CMD or ENTRYPOINT")

    if "latest" in text:
        warnings.append("Avoid using 'latest' tags in production Dockerfiles")

    valid = len(warnings) == 0

    return valid, warnings
