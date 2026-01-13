from typing import Dict, Any, Optional, List
from langchain_core.documents import Document
from app.db.chroma_store import get_chroma_store


class RAGPipeline:
    """LangChain-based RAG pipeline for retrieving data structure visualizers."""
    
    def __init__(self):
        """Initialize the RAG pipeline with ChromaDB store."""
        self.store = get_chroma_store()
    
    def retrieve(
        self,
        data_structure_name: str,
        n_results: int = 1,
        filter_metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Retrieve relevant document for a data structure.
        
        Args:
            data_structure_name: Name of the data structure to retrieve (e.g., "Stack", "Queue").
            n_results: Number of results to retrieve (default: 1).
            filter_metadata: Optional metadata filter (e.g., {"type": "visualizer"}).
        
        Returns:
            Dictionary containing:
            - description: Description from metadata
            - visualizer_code: Raw HTML/CSS/JS code (unmodified)
            - metadata: Full metadata dictionary
            - id: Document ID
        """
        # Build query - search for the data structure name
        query = f"{data_structure_name} visualizer"
        
        # Default filter to only get interactive visualizers
        where_filter = filter_metadata or {"type": "interactive"}
        
        # Query ChromaDB
        results = self.store.query(
            query_texts=[query],
            n_results=n_results,
            where=where_filter
        )
        
        # Check if results were found
        if not results["ids"] or not results["ids"][0]:
            return {
                "description": None,
                "visualizer_code": None,
                "metadata": None,
                "id": None,
                "found": False
            }
        
        # Get the first result
        doc_id = results["ids"][0][0]
        doc_text = results["documents"][0][0]
        doc_metadata = results["metadatas"][0][0]
        
        # Extract description from metadata
        description = doc_metadata.get("description", "")
        
        # Return raw code without modification
        return {
            "description": description,
            "visualizer_code": doc_text,  # Raw HTML/CSS/JS code
            "metadata": doc_metadata,
            "id": doc_id,
            "found": True
        }
    
    def retrieve_as_langchain_documents(
        self,
        data_structure_name: str,
        n_results: int = 1,
        filter_metadata: Optional[Dict[str, Any]] = None
    ) -> List[Document]:
        """
        Retrieve documents as LangChain Document objects.
        
        Args:
            data_structure_name: Name of the data structure to retrieve.
            n_results: Number of results to retrieve.
            filter_metadata: Optional metadata filter.
        
        Returns:
            List of LangChain Document objects.
        """
        # Build query
        query = f"{data_structure_name} visualizer"
        
        # Default filter
        where_filter = filter_metadata or {"type": "interactive"}
        
        # Query ChromaDB
        results = self.store.query(
            query_texts=[query],
            n_results=n_results,
            where=where_filter
        )
        
        # Convert to LangChain Documents
        documents = []
        if results["ids"] and results["ids"][0]:
            for i in range(len(results["ids"][0])):
                doc = Document(
                    page_content=results["documents"][0][i],
                    metadata={
                        **results["metadatas"][0][i],
                        "id": results["ids"][0][i],
                        "distance": results["distances"][0][i] if results.get("distances") else None
                    }
                )
                documents.append(doc)
        
        return documents
    
    def get_visualizer(
        self,
        data_structure_name: str
    ) -> Dict[str, Any]:
        """
        Get visualizer for a specific data structure.
        This is the main method to use for retrieving visualizers.
        
        Args:
            data_structure_name: Name of the data structure (e.g., "Stack", "Queue", "Singly Linked List").
        
        Returns:
            Dictionary with description and raw visualizer code.
        """
        result = self.retrieve(
            data_structure_name=data_structure_name,
            n_results=1,
            filter_metadata={"type": "interactive"}
        )
        
        if not result["found"]:
            return {
                "success": False,
                "error": f"Visualizer for '{data_structure_name}' not found",
                "description": None,
                "visualizer_code": None
            }
        
        return {
            "success": True,
            "name": result["metadata"].get("name", data_structure_name),
            "description": result["description"],
            "visualizer_code": result["visualizer_code"],  # Raw, unmodified code
            "metadata": result["metadata"]
        }


# Global instance (lazy-loaded)
_rag_pipeline: Optional[RAGPipeline] = None


def get_rag_pipeline() -> RAGPipeline:
    """
    Get or create the global RAG pipeline instance.
    
    Returns:
        RAGPipeline instance.
    """
    global _rag_pipeline
    if _rag_pipeline is None:
        _rag_pipeline = RAGPipeline()
    return _rag_pipeline


def get_visualizer(data_structure_name: str) -> Dict[str, Any]:
    """
    Convenience function to get a visualizer for a data structure.
    
    Args:
        data_structure_name: Name of the data structure.
    
    Returns:
        Dictionary with description and raw visualizer code.
    """
    pipeline = get_rag_pipeline()
    return pipeline.get_visualizer(data_structure_name)
