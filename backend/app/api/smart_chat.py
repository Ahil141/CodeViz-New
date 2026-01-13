"""
Smart Chat API Endpoint.

Combines intent detection with RAG retrieval to provide
intelligent responses for data structure learning queries.
"""

from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field
from typing import Optional, List
import json

from app.core.llm import LLM
from app.core.intent_detector import detect_intent, Intent
from app.core.code_extractor import get_code_extractor
from app.core.rag_pipeline import get_rag_pipeline


router = APIRouter()

# Shared LLM instance
_llm: Optional[LLM] = None


def preload_llm() -> LLM:
    """Preload and cache the LLM instance. Call this at startup."""
    global _llm
    if _llm is None:
        _llm = LLM()
    return _llm


def get_llm() -> LLM:
    """Get the shared LLM instance (loads if not already loaded)."""
    global _llm
    if _llm is None:
        _llm = LLM()
    return _llm


class SmartChatRequest(BaseModel):
    """Request model for smart chat."""
    message: str = Field(..., description="User's message", min_length=1)


class SmartChatResponse(BaseModel):
    """Response model for smart chat."""
    response_type: str = Field(..., description="'visualization' or 'text_only'")
    text: str = Field(..., description="AI response text")
    visualizer_code: Optional[str] = Field(None, description="HTML/CSS/JS visualizer code")
    data_structure: Optional[str] = Field(None, description="Detected data structure name")
    operations: Optional[List[str]] = Field(None, description="Specific operations requested")


# Prompt for generating explanations about data structures
DS_EXPLANATION_PROMPT = """You are an expert teacher explaining data structures.

The user wants to learn about: {data_structure}
{operations_context}

Provide a clear, concise explanation that:
1. Explains what this data structure is
2. Describes how the operations work
3. Mentions time complexity if relevant
4. Keep it brief (2-3 paragraphs max)

User's question: {user_message}

Your explanation:"""

DS_OPERATION_EXPLANATION_PROMPT = """You are an expert teacher explaining data structures.

The user wants to learn specifically about the {operations} operation(s) in {data_structure}.

Provide a focused explanation that:
1. Explains how these specific operations work
2. Describes the step-by-step process
3. Mentions time complexity
4. Keep it concise (1-2 paragraphs)

User's question: {user_message}

Your explanation:"""


@router.post("/", response_model=SmartChatResponse)
async def smart_chat(request: SmartChatRequest):
    """
    Smart chat endpoint that detects intent and returns appropriate response.
    
    For DS learning queries: Returns AI explanation + visualizer code
    For other queries: Returns normal AI response
    """
    message = request.message.strip()
    
    # Step 1: Detect intent
    intent = detect_intent(message)
    
    # Step 2: Handle based on intent
    if intent.is_ds_query and intent.data_structure:
        return await _handle_ds_query(message, intent)
    else:
        return await _handle_general_query(message)


async def _handle_ds_query(message: str, intent: Intent) -> SmartChatResponse:
    """Handle a data structure learning query."""
    llm = get_llm()
    rag = get_rag_pipeline()
    extractor = get_code_extractor()
    
    # Fetch visualizer from RAG
    result = rag.get_visualizer(intent.data_structure)
    
    visualizer_code = None
    if result.get("success"):
        visualizer_code = result.get("visualizer_code")
        
        # If specific operations requested, try to extract them
        if intent.operations and visualizer_code:
            if extractor.has_operation_markers(visualizer_code):
                visualizer_code = extractor.extract_operations(
                    visualizer_code,
                    intent.operations
                )
    
    # Generate explanation
    if intent.operations:
        prompt = DS_OPERATION_EXPLANATION_PROMPT.format(
            data_structure=intent.data_structure,
            operations=", ".join(intent.operations),
            user_message=message
        )
    else:
        operations_context = ""
        if intent.operations:
            operations_context = f"Specifically about: {', '.join(intent.operations)}"
        prompt = DS_EXPLANATION_PROMPT.format(
            data_structure=intent.data_structure,
            operations_context=operations_context,
            user_message=message
        )
    
    explanation = llm.generate(prompt)
    
    # Add note if visualizer not found
    if not visualizer_code:
        explanation += f"\n\n(Note: Interactive visualizer for {intent.data_structure} is not available yet.)"
    
    return SmartChatResponse(
        response_type="visualization" if visualizer_code else "text_only",
        text=explanation,
        visualizer_code=visualizer_code,
        data_structure=intent.data_structure,
        operations=intent.operations
    )


async def _handle_general_query(message: str) -> SmartChatResponse:
    """Handle a general (non-DS) query."""
    llm = get_llm()
    response = llm.generate(message)
    
    return SmartChatResponse(
        response_type="text_only",
        text=response,
        visualizer_code=None,
        data_structure=None,
        operations=None
    )


@router.post("/stream")
async def smart_chat_stream(request: SmartChatRequest):
    """
    Streaming version of smart chat.
    
    Returns a stream where:
    - First, a JSON header with metadata (response_type, visualizer_code, etc.)
    - Then, the streamed AI response text
    """
    message = request.message.strip()
    
    # Detect intent
    intent = detect_intent(message)
    
    if intent.is_ds_query and intent.data_structure:
        return await _stream_ds_query(message, intent)
    else:
        return await _stream_general_query(message)


async def _stream_ds_query(message: str, intent: Intent):
    """Stream a data structure learning response with LLM explanation."""
    rag = get_rag_pipeline()
    extractor = get_code_extractor()
    
    # Fetch visualizer (instant)
    result = rag.get_visualizer(intent.data_structure)
    
    visualizer_code = None
    if result.get("success"):
        visualizer_code = result.get("visualizer_code")
        
        if intent.operations and visualizer_code:
            if extractor.has_operation_markers(visualizer_code):
                visualizer_code = extractor.extract_operations(
                    visualizer_code,
                    intent.operations
                )
    
    # Build prompt for LLM explanation
    if intent.operations:
        prompt = DS_OPERATION_EXPLANATION_PROMPT.format(
            data_structure=intent.data_structure,
            operations=", ".join(intent.operations),
            user_message=message
        )
    else:
        prompt = DS_EXPLANATION_PROMPT.format(
            data_structure=intent.data_structure,
            operations_context="",
            user_message=message
        )
    
    def generator():
        # Send metadata with visualizer code IMMEDIATELY
        metadata = {
            "type": "metadata",
            "response_type": "visualization" if visualizer_code else "text_only",
            "data_structure": intent.data_structure,
            "operations": intent.operations,
            "visualizer_code": visualizer_code
        }
        yield f"__METADATA__{json.dumps(metadata)}__END_METADATA__"
        
        # Stream explanation from LLM
        try:
            print(f"[DEBUG] Starting LLM generation for {intent.data_structure}...")
            llm = get_llm()
            print("[DEBUG] LLM loaded, starting generation...")
            has_output = False
            for chunk in llm.stream_generate(prompt):
                has_output = True
                yield chunk
            
            print(f"[DEBUG] LLM generation complete. has_output={has_output}")
            
            if not has_output:
                # LLM produced no output, use fallback
                print("[DEBUG] Using fallback explanation (no LLM output)")
                yield _get_static_explanation(intent.data_structure, intent.operations)
                
        except Exception as e:
            print(f"[DEBUG] LLM error for DS query: {e}")
            import traceback
            traceback.print_exc()
            # Fallback to static explanation
            yield _get_static_explanation(intent.data_structure, intent.operations)
        
        # Add note if no visualizer
        if not visualizer_code:
            yield f"\n\n(Note: Interactive visualizer for {intent.data_structure} is not available yet.)"
    
    return StreamingResponse(generator(), media_type="text/plain")


# Pre-written explanations for instant responses
DS_EXPLANATIONS = {
    "Stack": """**Stack** is a linear data structure that follows the **LIFO (Last In, First Out)** principle.

**Key Operations:**
- **Push**: Add an element to the top of the stack
- **Pop**: Remove and return the top element
- **Peek**: View the top element without removing it

**Time Complexity:** All operations are O(1)

Try the interactive visualizer on the right to see how push and pop work!""",

    "Queue": """**Queue** is a linear data structure that follows the **FIFO (First In, First Out)** principle.

**Key Operations:**
- **Enqueue**: Add an element to the back of the queue
- **Dequeue**: Remove and return the front element
- **Peek**: View the front element without removing it

**Time Complexity:** All operations are O(1)

Try the interactive visualizer on the right to see how enqueue and dequeue work!""",

    "Singly Linked List": """**Singly Linked List** is a linear data structure where each element (node) contains data and a pointer to the next node.

**Key Operations:**
- **Insert at Head**: Add element at the beginning - O(1)
- **Insert at Tail**: Add element at the end - O(n)
- **Delete**: Remove an element by value - O(n)
- **Search**: Find an element - O(n)

**Advantages:** Dynamic size, efficient insertions/deletions at head

Try the interactive visualizer on the right to see how linked list operations work!""",
}


def _get_static_explanation(ds_name: str, operations: list = None) -> str:
    """Get a pre-written explanation for a data structure."""
    base_explanation = DS_EXPLANATIONS.get(ds_name, f"Learn about {ds_name} with the interactive visualizer!")
    
    if operations:
        ops_str = ", ".join(operations)
        return f"Showing **{ops_str}** operation(s) for {ds_name}.\n\n{base_explanation}"
    
    return base_explanation


async def _stream_general_query(message: str):
    """Stream a general response using LLM."""
    
    def generator():
        # Send metadata header first
        metadata = {
            "type": "metadata",
            "response_type": "text_only",
            "data_structure": None,
            "operations": None,
            "visualizer_code": None
        }
        yield f"__METADATA__{json.dumps(metadata)}__END_METADATA__"
        
        # Try to use LLM
        try:
            llm = get_llm()
            has_output = False
            for chunk in llm.stream_generate(message):
                has_output = True
                yield chunk
            
            if not has_output:
                yield "I'm sorry, I couldn't generate a response. Please try again."
                
        except Exception as e:
            print(f"LLM generation error: {e}")
            yield f"I'm having trouble generating a response right now. For data structure topics, try asking about 'stack', 'queue', or 'linked list' for instant visualizations!"
    
    return StreamingResponse(generator(), media_type="text/plain")
