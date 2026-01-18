from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from app.services.rag_service import rag_service

router = APIRouter()

class VisualizerQuery(BaseModel):
    data_structure_name: str

class VisualizerResponse(BaseModel):
    success: bool
    name: str
    visualizer_code: str | None = None
    description: str | None = None
    error: str | None = None

@router.post("/query", response_model=VisualizerResponse)
async def get_visualizer(query: VisualizerQuery):
    """
    Retrieve visualization code for a specific data structure.
    """
    try:
        name = query.data_structure_name.lower().replace(" ", "_").strip()
        
        # 1. Try exact match via get_visualizer method (metadata filter)
        result = rag_service.get_visualizer(name)
        
        if result:
            return VisualizerResponse(
                success=True,
                name=query.data_structure_name,
                visualizer_code=result['code'],
                description=result['metadata'].get('description', 'Interactive visualization')
            )
            
        # 2. Fallback: Semantic search if exact match fails
        # querying "Show me [name] visualization code"
        search_results = rag_service.query(f"{name} visualization code html javascript", n_results=1)
        
        if search_results:
             return VisualizerResponse(
                success=True,
                name=query.data_structure_name,
                visualizer_code=search_results[0],
                description="Retrieved via semantic search"
            )

        return VisualizerResponse(
            success=False,
            name=query.data_structure_name,
            error="Visualizer not found in database."
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve visualizer: {str(e)}"
        )
