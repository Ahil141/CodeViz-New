from fastapi import APIRouter, HTTPException, status
from fastapi.responses import StreamingResponse
import traceback
import re
import json
import asyncio

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


@router.post("/stream")
async def chat_stream(request: ChatRequest):
    """
    Streaming chat endpoint that sends text chunks progressively via Server-Sent Events.
    After explanation completes, sends visualization data and code blocks.
    """
    
    async def event_generator():
        try:
            # Step 1: Stream the explanation text
            full_response = ""
            async for chunk in llm_service.generate_response_stream(request.prompt):
                full_response += chunk
                # Send as SSE event
                yield f"data: {json.dumps({'type': 'text', 'content': chunk})}\n\n"
            
            # Step 2: Detect visualization type
            vis_type = visualization_service.determine_visualization_type(
                request.prompt, 
                full_response
            )
            
            # Step 3: Generate visualization if needed
            code_blocks = []
            visualization_data = None
            implementation_code_block = None
            
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
                VisualizationType.ALGORITHM
            ]
            
            if vis_type != VisualizationType.NONE:
                # Try LLM visualization generation first
                fallback_prompt = (
                    f"Create a self-contained interactive visualization for: "
                    f"'{request.prompt}'.\n\n"
                    "Return ONLY THREE Markdown code blocks:\n"
                    "```html\n...``` \n"
                    "```css\n...``` \n"
                    "```javascript\n...``` \n\n"
                    "Do NOT include explanations or extra text."
                )

                try:
                    llm_vis_response = await llm_service.generate_response(
                        fallback_prompt,
                        context=""
                    )
                    
                    print(f"DEBUG: LLM Visualization Response: {llm_vis_response[:200]}...")

                    # Relaxed regex to handle spaces and optional newlines better
                    matches = re.findall(
                        r"```\s*(html|css|javascript|js)\s*\n(.*?)```",
                        llm_vis_response,
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
                        print("DEBUG: Successfully generated LLM visualization code blocks.")
                        vis_type = VisualizationType.HTML
                    else:
                        print("DEBUG: Failed to extract code blocks from LLM response.")
                        
                except Exception as e:
                    print(f"ERROR: LLM visualization generation failed: {e}")

            # Fallback logic (Native -> RAG)
            if vis_type != VisualizationType.NONE and not code_blocks:
                if vis_type in NATIVE_VISUALIZATION_TYPES:
                    pass  # Native visualizer will handle it
                else:
                    # RAG fallback
                    try:
                        retrieved_docs = rag_service.query(request.prompt)
                        if retrieved_docs:
                            for doc in retrieved_docs:
                                doc = doc.strip()
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
                    except Exception as e:
                        print(f"WARNING: RAG service failed: {e}")

            # Step 4: Generate implementation code
            if vis_type != VisualizationType.NONE:
                impl_prompt = (
                    f"Generate a Python implementation for: {request.prompt}\n\n"
                    "Return ONLY a single Python code block:\n"
                    "```python\n...\n```\n\n"
                    "Include comments and be educational."
                )

                try:
                    impl_response = await llm_service.generate_response(impl_prompt)
                    impl_match = re.search(
                        r"```python\n(.*?)```",
                        impl_response,
                        re.DOTALL | re.IGNORECASE
                    )
                    if impl_match:
                        implementation_code_block = CodeBlock(
                            language="python",
                            code=impl_match.group(1).strip()
                        )
                except Exception as e:
                    print(f"WARNING: Implementation code generation failed: {e}")

            # Step 5: Send final metadata
            final_data = {
                'type': 'complete',
                'visualization_type': vis_type.value,
                'code_blocks': [{'language': cb.language, 'code': cb.code} for cb in code_blocks],
                'visualization_data': visualization_data,
                'implementation_code': {
                    'language': implementation_code_block.language,
                    'code': implementation_code_block.code
                } if implementation_code_block else None
            }
            
            yield f"data: {json.dumps(final_data)}\n\n"
            
        except Exception as e:
            traceback.print_exc()
            error_data = {'type': 'error', 'message': str(e)}
            yield f"data: {json.dumps(error_data)}\n\n"
    
    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
        }
    )


# Original non-streaming endpoint (preserved for compatibility)
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
        # 1. Normal LLM response (text explanation)
        # --------------------------------------------------
        # PROACTIVE LLM FIRST: Query LLM without RAG context initially
        print("DEBUG: Generating LLM response (Primary)")
        raw_response = await llm_service.generate_response(request.prompt)

        # --------------------------------------------------
        # 2. VISUALIZATION DETECTION
        # --------------------------------------------------
        vis_type = visualization_service.determine_visualization_type(
            request.prompt, raw_response
        )
        print(f"DEBUG: Visualization Type Detected: {vis_type}")

        code_blocks = []
        visualization_data = None
        implementation_code_block = None
        retrieved_docs = []

        # --------------------------------------------------
        # 3. VISUALIZATION GENERATION (LLM PRIMARY)
        # --------------------------------------------------
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
            VisualizationType.ALGORITHM
        ]

        if vis_type != VisualizationType.NONE:
            print(f"DEBUG: Attempting LLM visualization generation for {vis_type}")
            
            fallback_prompt = (
                f"Create a self-contained interactive visualization for: "
                f"'{request.prompt}'.\n\n"
                "Return ONLY THREE Markdown code blocks:\n"
                "```html\n...``` \n"
                "```css\n...``` \n"
                "```javascript\n...``` \n\n"
                "Do NOT include explanations or extra text."
            )

            try:
                llm_vis_response = await llm_service.generate_response(
                    fallback_prompt,
                    context=""
                )

                print(f"DEBUG: LLM Visualization Response (Sync): {llm_vis_response[:200]}...")

                matches = re.findall(
                    r"```\s*(html|css|javascript|js)\s*\n(.*?)```",
                    llm_vis_response,
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
                    print("DEBUG: Successfully generated LLM visualization (Sync).")
                    vis_type = VisualizationType.HTML
                else:
                    print("DEBUG: Failed to extract code blocks from LLM response (Sync).")

            except Exception as e:
                print(f"ERROR: LLM visualization generation failed: {e}")

        # --------------------------------------------------
        # 4. FALLBACK LOGIC (Native -> RAG)
        # --------------------------------------------------
        if vis_type != VisualizationType.NONE and not code_blocks:
            # First Check: Is it a native type we can handle on the frontend?
            if vis_type in NATIVE_VISUALIZATION_TYPES:
                print(f"DEBUG: Using native visualizer for {vis_type}")
                # We leave code_blocks empty, frontend will use the native component
            else:
                # Second Check: Does RAG have a stored visualization?
                print(f"DEBUG: Falling back to RAG for {vis_type}")
                try:
                    retrieved_docs = rag_service.query(request.prompt)
                except Exception as e:
                    print(f"WARNING: RAG service failed: {e}")

                if retrieved_docs:
                    print(f"DEBUG: RAG Docs Retrieved: {len(retrieved_docs)}")
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

        # --------------------------------------------------
        # 5. Final polish
        # --------------------------------------------------
        if vis_type != VisualizationType.NONE:
            print("DEBUG: Generating implementation code for", vis_type)
            impl_prompt = (
                f"Generate a Python implementation for: {request.prompt}\n\n"
                "Return ONLY a single Python code block:\n"
                "```python\n...\n```\n\n"
                "Include comments and be educational."
            )

            try:
                impl_response = await llm_service.generate_response(impl_prompt)
                impl_match = re.search(
                    r"```python\n(.*?)```",
                    impl_response,
                    re.DOTALL | re.IGNORECASE
                )
                if impl_match:
                    implementation_code_block = CodeBlock(
                        language="python",
                        code=impl_match.group(1).strip()
                    )
            except Exception as e:
                print(f"WARNING: Implementation code generation failed: {e}")

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
