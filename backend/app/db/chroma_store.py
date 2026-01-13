import os
from typing import List, Dict, Any, Optional, TYPE_CHECKING
from pydantic_settings import BaseSettings

if TYPE_CHECKING:
    import chromadb
    from chromadb.config import Settings
    from chromadb.api.types import Documents, Embeddings
    from sentence_transformers import SentenceTransformer


class ChromaDBSettings(BaseSettings):
    """Configuration settings for ChromaDB."""
    persist_directory: str = "./chroma_db"
    collection_name: str = "codelearn_documents"
    embedding_model: str = "all-MiniLM-L6-v2"  # Fast and efficient SentenceTransformer model
    
    class Config:
        env_prefix = "CHROMA_"
        env_file = ".env"
        extra = "ignore"


class CodeLearnEmbeddingFunction:
    """Custom embedding function for ChromaDB."""
    
    def __init__(self, model_name: str):
        from sentence_transformers import SentenceTransformer
        self.embedding_model = SentenceTransformer(model_name)
        
    def __call__(self, input: List[str]) -> List[List[float]]:
        """
        Compute query embeddings using the SentenceTransformer model.
        
        Args:
            input: List of documents/texts to embed.
            
        Returns:
            List of embeddings.
        """
        embeddings = self.embedding_model.encode(input, show_progress_bar=False)
        return embeddings.tolist()


class ChromaStore:
    """ChromaDB store with SentenceTransformer embeddings and persistent storage."""
    
    def __init__(self, settings: Optional[ChromaDBSettings] = None):
        """
        Initialize ChromaDB store.
        
        Args:
            settings: Optional ChromaDB settings. If None, loads from environment.
        """
        self.settings = settings or ChromaDBSettings()
        
        # Create persist directory if it doesn't exist
        os.makedirs(self.settings.persist_directory, exist_ok=True)
        
        # Initialize embedding function
        print(f"Loading embedding model: {self.settings.embedding_model}")
        self.embedding_function = CodeLearnEmbeddingFunction(self.settings.embedding_model)
        
        # Initialize ChromaDB client with persistent storage
        import chromadb
        from chromadb.config import Settings
        
        self.client = chromadb.PersistentClient(
            path=self.settings.persist_directory,
            settings=Settings(
                anonymized_telemetry=False,
                allow_reset=True,
            )
        )
        
        # Create or get collection with custom embedding function
        self.collection = self.client.get_or_create_collection(
            name=self.settings.collection_name,
            embedding_function=self.embedding_function,
            metadata={"description": "CodeLearn AI document collection"}
        )
    
    def add_documents(
        self,
        documents: List[str],
        metadatas: Optional[List[Dict[str, Any]]] = None,
        ids: Optional[List[str]] = None
    ) -> List[str]:
        """
        Add documents to the ChromaDB collection.
        
        Args:
            documents: List of document texts to add.
            metadatas: Optional list of metadata dictionaries for each document.
                      Each dict can contain any fields (e.g., {"topic": "arrays", "type": "code"}).
            ids: Optional list of unique IDs for each document.
                 If not provided, auto-generated IDs will be used.
        
        Returns:
            List of document IDs that were added.
        """
        if not documents:
            raise ValueError("Documents list cannot be empty")
        
        # Generate IDs if not provided
        if ids is None:
            ids = [f"doc_{i}_{hash(doc) % 100000}" for i, doc in enumerate(documents)]
        
        # Ensure IDs are unique
        if len(ids) != len(set(ids)):
            raise ValueError("All document IDs must be unique")
        
        # Default metadata if not provided
        if metadatas is None:
            metadatas = [{}] * len(documents)
        
        # Ensure metadata list matches documents length
        if len(metadatas) != len(documents):
            raise ValueError("Metadatas list must match documents list length")
        
        # Ensure IDs list matches documents length
        if len(ids) != len(documents):
            raise ValueError("IDs list must match documents list length")
        
        # Add documents to collection
        self.collection.add(
            documents=documents,
            metadatas=metadatas,
            ids=ids
        )
        
        print(f"Added {len(documents)} documents to collection")
        return ids
    
    def query(
        self,
        query_texts: List[str],
        n_results: int = 5,
        where: Optional[Dict[str, Any]] = None,
        where_document: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Query documents by similarity.
        
        Args:
            query_texts: List of query texts to search for.
            n_results: Number of similar documents to return per query.
            where: Optional metadata filter (e.g., {"topic": "arrays"}).
            where_document: Optional document content filter (e.g., {"$contains": "python"}).
        
        Returns:
            Dictionary containing:
            - ids: List of lists of document IDs
            - distances: List of lists of similarity distances
            - metadatas: List of lists of metadata dictionaries
            - documents: List of lists of document texts
        """
        if not query_texts:
            raise ValueError("Query texts list cannot be empty")
        
        results = self.collection.query(
            query_texts=query_texts,
            n_results=n_results,
            where=where,
            where_document=where_document
        )
        
        return results
    
    def get_by_ids(self, ids: List[str]) -> Dict[str, Any]:
        """
        Retrieve documents by their IDs.
        
        Args:
            ids: List of document IDs to retrieve.
        
        Returns:
            Dictionary containing documents, metadatas, and ids.
        """
        results = self.collection.get(ids=ids)
        return results
    
    def delete(self, ids: Optional[List[str]] = None, where: Optional[Dict[str, Any]] = None):
        """
        Delete documents from the collection.
        
        Args:
            ids: Optional list of document IDs to delete.
            where: Optional metadata filter to delete matching documents.
        """
        if ids is None and where is None:
            raise ValueError("Either ids or where filter must be provided")
        
        self.collection.delete(ids=ids, where=where)
        print(f"Deleted documents from collection")
    
    def count(self) -> int:
        """
        Get the total number of documents in the collection.
        
        Returns:
            Number of documents in the collection.
        """
        return self.collection.count()
    
    def reset(self):
        """Reset the collection (delete all documents)."""
        self.client.delete_collection(name=self.settings.collection_name)
        self.collection = self.client.create_collection(
            name=self.settings.collection_name,
            embedding_function=self.embedding_function,
            metadata={"description": "CodeLearn AI document collection"}
        )
        print("Collection reset")


# Global instance (lazy-loaded)
_chroma_store: Optional[ChromaStore] = None


def get_chroma_store(settings: Optional[ChromaDBSettings] = None) -> ChromaStore:
    """
    Get or create the global ChromaDB store instance.
    
    Args:
        settings: Optional ChromaDB settings. Only used on first call.
    
    Returns:
        ChromaStore instance.
    """
    global _chroma_store
    if _chroma_store is None:
        _chroma_store = ChromaStore(settings)
    return _chroma_store
