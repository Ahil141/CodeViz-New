from fastapi import APIRouter, HTTPException, status
import traceback
import re
import json

from app.schemas.chat import (
    ChatRequest,
    ChatResponse,
    VisualizationType,
    CodeBlock,
)

from app.services.llm_service import llm_service
from app.services.visualization_service import visualization_service
from app.services.rag_service import rag_service

router = APIRouter()


@router.post("/", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Chat endpoint that:
    1. Queries RAG (if available)
    2. Generates LLM explanation
    3. Detects visualization intent
    4. Extracts visualization code from RAG OR
    5. Falls back to LLM-generated HTML/CSS/JS visualization
    """

    try:
        # --------------------------------------------------
        # 1. Query RAG
        # --------------------------------------------------
        retrieved_docs = []
        try:
            retrieved_docs = rag_service.query(request.prompt)
        except Exception as e:
            print(f"WARNING: RAG service failed: {e}")

        context = "\n".join(retrieved_docs) if retrieved_docs else ""

        # --------------------------------------------------
        # 2. Normal LLM response (text explanation)
        # --------------------------------------------------
        raw_response = await llm_service.generate_response(
            request.prompt,
            context=context
        )

        # --------------------------------------------------
        # 3. Detect visualization intent
        # --------------------------------------------------
        vis_type = visualization_service.determine_visualization_type(
            request.prompt,
            raw_response
        )

        print(f"DEBUG: Visualization Type Detected: {vis_type}")
        print(f"DEBUG: RAG Docs Retrieved: {len(retrieved_docs)}")

        code_blocks = []
        visualization_data = None

        # --------------------------------------------------
        # 4. Try extracting visualization code from RAG docs
        # --------------------------------------------------
        if vis_type != VisualizationType.NONE and retrieved_docs:
            for doc in retrieved_docs:
                doc = doc.strip()

                # Look for fenced code blocks
                matches = re.findall(
                    r"```(\w+)\n(.*?)```",
                    doc,
                    re.DOTALL | re.IGNORECASE
                )

                for lang, code in matches:
                    lang = lang.lower()
                    if lang == "js":
                        lang = "javascript"

                    if lang in ["html", "css", "javascript"]:
                        code_blocks.append(
                            CodeBlock(language=lang, code=code.strip())
                        )

                if code_blocks:
                    vis_type = VisualizationType.HTML
                    break

                # Optional: JSON-based visualization
                if doc.startswith("{"):
                    try:
                        visualization_data = json.loads(doc)
                        vis_type = VisualizationType.DATA
                        break
                    except Exception:
                        pass

        # 5. HARD FALLBACK: Ask LLM to generate visualization
        # --------------------------------------------------
        # CRITICAL FIX: Do NOT overwrite native supported types with generated HTML
        # The frontend has built-in React components for these.
        NATIVE_VISUALIZATION_TYPES = [
            VisualizationType.STACK,
            VisualizationType.QUEUE,
            VisualizationType.CIRCULAR_QUEUE,
            VisualizationType.DEQUE,
            VisualizationType.ARRAY,
            VisualizationType.LINKED_LIST,
            VisualizationType.DOUBLY_LINKED_LIST,
            VisualizationType.CIRCULAR_LINKED_LIST,
            VisualizationType.BINARY_TREE,
            VisualizationType.HEAP,
            VisualizationType.GRAPH,
            VisualizationType.SORTING,
            VisualizationType.SEARCHING,
            VisualizationType.ALGORITHM # Since we mapped this to StackVisualizer or SortingAlgorithms
        ]

        if vis_type != VisualizationType.NONE and not code_blocks:
            if vis_type in NATIVE_VISUALIZATION_TYPES:
                print(f"DEBUG: Skipping fallback for native type: {vis_type}")
                # We intentionally leave code_blocks empty so frontend uses the native component
            else:
                print("DEBUG: Triggering visualization fallback generation")

            fallback_prompt = (
                f"Create a self-contained interactive visualization for: "
                f"'{request.prompt}'.\n\n"
                "Return ONLY THREE Markdown code blocks:\n"
                "```html\n...``` \n"
                "```css\n...``` \n"
                "```javascript\n...``` \n\n"
                "Do NOT include explanations or extra text."
            )

            fallback_response = await llm_service.generate_response(
                fallback_prompt,
                context=""
            )

            matches = re.findall(
                r"```(html|css|javascript|js)\n(.*?)```",
                fallback_response,
                re.DOTALL | re.IGNORECASE
            )

            for lang, code in matches:
                lang = lang.lower()
                if lang == "js":
                    lang = "javascript"

                code_blocks.append(
                    CodeBlock(language=lang, code=code.strip())
                )

            if code_blocks:
                vis_type = VisualizationType.HTML
            else:
                print("ERROR: Visualization fallback returned no code")

        # --------------------------------------------------
        # 6. Final polish
        # --------------------------------------------------
        if raw_response.startswith("Error:") and code_blocks:
            raw_response = (
                "Here is an interactive visualization to help you "
                "understand the concept."
            )

        # --------------------------------------------------
        # 7. Generate Implementation Code (New Feature)
        # --------------------------------------------------
        implementation_code_block = None
        if vis_type != VisualizationType.NONE:
            print(f"DEBUG: Generating implementation code for {vis_type}")
            impl_prompt = (
                f"Provide the standard Python implementation code for: '{request.prompt}'.\n"
                "Return the code in a single Markdown code block like ```python ... ```.\n"
                "Do not include any explanation, just the code."
            )
            
            try:
                impl_response = await llm_service.generate_response(impl_prompt, context="")
                # Extract first code block
                impl_matches = re.findall(r"```(\w+)\n(.*?)```", impl_response, re.DOTALL | re.IGNORECASE)
                if impl_matches:
                    lang, code = impl_matches[0]
                    if lang.lower() == 'py': lang = 'python'
                    implementation_code_block = CodeBlock(language=lang.lower(), code=code.strip())
            except Exception as e:
                print(f"Error generating implementation code: {e}")

        return ChatResponse(
            text_response=raw_response,
            visualization_type=vis_type,
            code_blocks=code_blocks,
            visualization_data=visualization_data,
            implementation_code=implementation_code_block,
        )

    except Exception as e:
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Chat processing failed: {str(e)}",
        )
