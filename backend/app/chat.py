import json
import traceback
from typing import Optional

from fastapi import APIRouter
from pydantic import BaseModel

from app.llm_service import llm_service
from app.hardcoded_visualizers import HARDCODED_VISUALIZERS

router = APIRouter()


class ChatRequest(BaseModel):
    prompt: str


class DualAgentResponse(BaseModel):
    type: str = "data_structure"
    ai_html: Optional[str] = None
    fallback_html: Optional[str] = None
    explanation: str
    python_code: Optional[str] = None


# Normalises the various shapes the remote AI may return HTML in
def _extract_ai_html(raw: object) -> Optional[str]:
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


def _find_fallback(query: str) -> Optional[str]:
    query_lower = query.lower()
    sorted_keys = sorted(HARDCODED_VISUALIZERS.keys(), key=len, reverse=True)
    for keyword in sorted_keys:
        if keyword in query_lower:
            html = HARDCODED_VISUALIZERS[keyword].get("html")
            if html:
                return html
    return None


@router.post("/", response_model=DualAgentResponse)
async def chat(request: ChatRequest):
    try:
        agent_result = llm_service.generate_response(request.prompt)

        explanation: str = agent_result.get("explanation", "I could not generate a response at this time.")
        ai_html: Optional[str] = _extract_ai_html(agent_result.get("ai_html"))
        python_code: Optional[str] = agent_result.get("python_code")
        fallback_html: Optional[str] = _find_fallback(request.prompt)

        return DualAgentResponse(
            type="data_structure",
            ai_html=ai_html,
            fallback_html=fallback_html,
            explanation=explanation,
            python_code=python_code,
        )

    except Exception as e:
        traceback.print_exc()
        return DualAgentResponse(
            type="data_structure",
            ai_html=None,
            fallback_html=_find_fallback(request.prompt),
            explanation=f"Server error: {str(e)}",
        )
