from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Optional
from app.core.rag_pipeline import get_rag_pipeline


router = APIRouter()


class RAGQueryRequest(BaseModel):
    """Request model for RAG query."""
    data_structure_name: str = Field(
        ...,
        description="Name of the data structure to retrieve (e.g., 'Stack', 'Queue', 'Singly Linked List')",
        min_length=1
    )


class RAGQueryResponse(BaseModel):
    """Response model for RAG query."""
    success: bool = Field(..., description="Whether the query was successful")
    name: Optional[str] = Field(None, description="Name of the data structure")
    description: Optional[str] = Field(None, description="Description of the data structure")
    visualizer_code: Optional[str] = Field(None, description="Raw HTML/CSS/JS visualizer code")
    error: Optional[str] = Field(None, description="Error message if query failed")


@router.post("/query", response_model=RAGQueryResponse)
async def rag_query(request: RAGQueryRequest):
    """
    Query the RAG pipeline to retrieve a data structure visualizer.
    
    Args:
        request: RAGQueryRequest containing the data structure name.
    
    Returns:
        RAGQueryResponse with description and visualizer code.
    
    Raises:
        HTTPException: If the visualizer is not found.
    """
    # 1. Use RAG pipeline
    try:
        pipeline = get_rag_pipeline()
        result = pipeline.get_visualizer(request.data_structure_name)
    except Exception as e:
        print(f"RAG pipeline error: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    
    if not result.get("success"):
        raise HTTPException(
                status_code=404,
                detail=result.get("error", "Visualizer not found")
            )

    return RAGQueryResponse(
        success=True,
        name=result.get("name"),
        description=result.get("description"),
        visualizer_code=result.get("visualizer_code"),
        error=None
    )


@router.get("/")
async def rag_info():
    """RAG API endpoint information."""
    return {
        "message": "RAG API endpoint",
        "endpoints": {
            "POST /query": "Query for a data structure visualizer"
        }
    }
