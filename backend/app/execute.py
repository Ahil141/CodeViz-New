import io
import sys
from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()


class ExecuteRequest(BaseModel):
    code: str


@router.post("/")
def execute(request: ExecuteRequest):
    buffer = io.StringIO()
    try:
        sys.stdout = buffer
        exec(request.code, {})  # noqa: S102
    except Exception as e:
        return {"output": f"Error: {str(e)}"}
    finally:
        sys.stdout = sys.__stdout__
    return {"output": buffer.getvalue()}
