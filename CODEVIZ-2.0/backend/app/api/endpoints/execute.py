from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import subprocess
import sys
import traceback
import tempfile
import os

router = APIRouter()

class ExecuteRequest(BaseModel):
    code: str
    language: str

class ExecuteResponse(BaseModel):
    output: str
    status: str # 'success' or 'error'
    visualization_code: str | None = None # For HTML/JS

@router.post("/", response_model=ExecuteResponse)
async def execute_code(request: ExecuteRequest):
    """
    Execute code sent from the frontend.
    - Python: Runs via subprocess and captures stdout/stderr.
    - HTML/JS: Returns as visualization_code so frontend renders it.
    """
    lang = request.language.lower()
    
    # 1. Handle Web Code (HTML/CSS/JS)
    if lang in ['html', 'javascript', 'css']:
        # For web languages, "execution" means rendering in the browser
        return ExecuteResponse(
            output="Rendering preview...",
            status="success",
            visualization_code=request.code
        )

    # 2. Handle Python Code
    if lang == 'python':
        try:
            # Create a temporary file to run the code
            # This is safer than eval() but still not sandboxed!
            # WARN: For a production app, use Docker or gVisor.
            with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as tmp:
                tmp.write(request.code)
                tmp_path = tmp.name
                
            try:
                # Run the script
                result = subprocess.run(
                    [sys.executable, tmp_path],
                    capture_output=True,
                    text=True,
                    timeout=5 # 5 second timeout
                )
                
                output = result.stdout
                if result.stderr:
                    output += f"\nError:\n{result.stderr}"
                
                return ExecuteResponse(
                    output=output,
                    status="success" if result.returncode == 0 else "error"
                )
                
            finally:
                # Cleanup
                if os.path.exists(tmp_path):
                    os.remove(tmp_path)
                    
        except subprocess.TimeoutExpired:
            return ExecuteResponse(
                output="Error: Execution timed out (limit: 5s)",
                status="error"
            )
        except Exception as e:
            traceback.print_exc()
            return ExecuteResponse(
                output=f"System Error: {str(e)}",
                status="error"
            )

    return ExecuteResponse(
        output=f"Language '{lang}' execution not supported locally yet.",
        status="error"
    )
