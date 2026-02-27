"""
Chat endpoint -- Dual-Agent Architecture
-----------------------------------------
POST /api/v1/chat/
  Body:  { "prompt": "<user message>" }
  Returns:
  {
    "type":          "data_structure",
    "ai_html":       "<full HTML string | null>",
    "fallback_html": "<hardcoded HTML string | null>",
    "explanation":   "<text explanation from AI>"
  }
"""

import json
import traceback
from typing import Optional

from fastapi import APIRouter
from pydantic import BaseModel

from app.services.llm_service import llm_service
from app.core.hardcoded_visualizers import HARDCODED_VISUALIZERS

router = APIRouter()


# --- Request / Response schemas -------------------------------------------

class ChatRequest(BaseModel):
    prompt: str


class DualAgentResponse(BaseModel):
    type: str = "data_structure"
    ai_html: Optional[str] = None
    fallback_html: Optional[str] = None
    explanation: str


# --- Helper: extract HTML from an AI payload ------------------------------

def _extract_ai_html(raw: object) -> Optional[str]:
    """
    The remote AI may return the HTML in several shapes.
    We handle the most common ones and always fall back to None.

    Accepted shapes:
      1. A plain HTML string (starts with '<!DOCTYPE' or '<html')
      2. A JSON-encoded string like '{"html": "<!DOCTYPE..."}'
      3. code_blocks style: '{"code_blocks":[{"language":"html","code":"..."}]}'
      4. A dict with an "html" key (already parsed)
      5. Anything else -> None
    """
    if raw is None:
        return None

    if isinstance(raw, dict):
        if "html" in raw:
            return str(raw["html"]).strip() or None
        if "code_blocks" in raw:
            for block in raw["code_blocks"]:
                if isinstance(block, dict) and block.get("language", "").lower() == "html":
                    return str(block.get("code", "")).strip() or None
        return None

    if not isinstance(raw, str):
        return None

    stripped = raw.strip()

    if stripped.lower().startswith("<!doctype") or stripped.lower().startswith("<html"):
        return stripped

    if stripped.startswith("{"):
        try:
            parsed = json.loads(stripped)
            return _extract_ai_html(parsed)
        except json.JSONDecodeError:
            pass

    return stripped if stripped else None


# --- Helper: find the best fallback for a user query ---------------------

def _find_fallback(query: str) -> Optional[str]:
    """
    Case-insensitive substring scan.  Longer keys are checked first so
    "binary tree" beats "tree" etc.
    """
    query_lower = query.lower()
    sorted_keys = sorted(HARDCODED_VISUALIZERS.keys(), key=len, reverse=True)
    for keyword in sorted_keys:
        if keyword in query_lower:
            html = HARDCODED_VISUALIZERS[keyword].get("html")
            if html:
                return html
    return None


# --- Main endpoint --------------------------------------------------------

@router.post("/", response_model=DualAgentResponse)
async def chat(request: ChatRequest):
    """
    Dual-Agent chat endpoint.

    1. Calls the remote Ngrok/Kaggle agent to get ai_html + explanation.
    2. Normalises the ai_html payload.
    3. Searches the query for a matching hardcoded visualizer (fallback_html).
    4. Returns a strictly typed JSON response.
    """
    try:
        print(f"DEBUG: Incoming prompt: {request.prompt[:120]}")
        agent_result = llm_service.generate_response(request.prompt)

        explanation: str = agent_result.get(
            "explanation",
            "I could not generate a response at this time."
        )
        raw_ai_html = agent_result.get("ai_html", None)

        ai_html: Optional[str] = _extract_ai_html(raw_ai_html)
        print(f"DEBUG: ai_html present: {ai_html is not None}")

        fallback_html: Optional[str] = _find_fallback(request.prompt)
        print(f"DEBUG: fallback_html present: {fallback_html is not None}")

        return DualAgentResponse(
            type="data_structure",
            ai_html=ai_html,
            fallback_html=fallback_html,
            explanation=explanation,
        )

    except Exception as e:
        traceback.print_exc()
        return DualAgentResponse(
            type="data_structure",
            ai_html=None,
            fallback_html=_find_fallback(request.prompt),
            explanation=f"Server error: {str(e)}",
        )
