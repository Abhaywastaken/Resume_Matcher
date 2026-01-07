#FILE: skills.py
import os
from typing import List, Set

OPENAI_KEY = os.environ.get("OPENAI_API_KEY")

def _call_openai_chat(prompt: str) -> str:
    try:
        import openai
        if OPENAI_KEY:
            openai.api_key = OPENAI_KEY
        else:
            raise RuntimeError("OPENAI_API_KEY not set")
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini" if hasattr(openai, "ChatCompletion") else "gpt-3.5-turbo",
            messages=[{"role":"user","content":prompt}],
            max_tokens=300,
            temperature=0.0,
        )
        content = response["choices"][0]["message"]["content"]
        return content
    except Exception as e:
        raise RuntimeError(f"OpenAI call failed: {e}")

def extract_skills(text: str) -> Set[str]:
    """
    Use an LLM to extract short skill tokens from free text.
    Returns a set of lowercase skill strings.
    """
    prompt = (
        "Extract a comma-separated list of concise skills, tools, and technologies from the following text. "
        "Only return the comma-separated list (no extra commentary). "
        "Normalize to short tokens like 'python', 'git', 'docker', 'ci/cd', 'nlp', 'pandas', etc.\n\n"
        "Text:\n"
        f"{text}\n\nList:"
    )
    try:
        raw = _call_openai_chat(prompt)
    except RuntimeError:
        # Fallback naive extractor: take 1-2 word tokens that look like skills
        import re
        tokens = re.findall(r"\b[A-Za-z0-9\+\#\.\-/]{2,20}\b", text)
        # filter and choose frequent candidates
        lower = [t.lower() for t in tokens]
        common = set([t for t in lower if len(t) > 1])
        return common
    # parse comma-separated list
    items = []
    for part in raw.split(","):
        p = part.strip().lower()
        if p:
            items.append(p)
    return set(items)

def missing_skills(required: Set[str], candidate: Set[str]) -> Set[str]:
    """
    Returns required - candidate using basic normalization.
    """
    # naive normalization: lowercase + strip
    req = set(r.strip().lower() for r in required)
    cand = set(c.strip().lower() for c in candidate)
    return req - cand

