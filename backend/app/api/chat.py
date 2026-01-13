from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import Optional

from app.core.llm import LLM

router = APIRouter()
llm = LLM()


class ChatRequest(BaseModel):
    prompt: Optional[str] = None
    message: Optional[str] = None


@router.post("/")
def chat(request: ChatRequest):
    prompt = request.prompt or request.message

    if not prompt:
        raise HTTPException(
            status_code=422,
            detail="Either 'prompt' or 'message' must be provided"
        )

    response = llm.generate(prompt)
    return {"response": response}


@router.post("/stream")
def chat_stream(request: ChatRequest):
    prompt = request.prompt or request.message

    if not prompt:
        raise HTTPException(
            status_code=422,
            detail="Either 'prompt' or 'message' must be provided"
        )

    def generator():
        for chunk in llm.stream_generate(prompt):
            yield chunk

    return StreamingResponse(generator(), media_type="text/plain")
