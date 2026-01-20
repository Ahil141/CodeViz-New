import chromadb
from chromadb.config import Settings
import os

class RAGService:

    def __init__(self):
        # Initialize persistent client
        # Save data to 'chroma_db' folder in the project root (or backend)
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        persist_directory = os.path.join(base_dir, "chroma_db")
        
        try:
            self.client = chromadb.PersistentClient(path=persist_directory)
            # Create or get a collection for educational content and visualizers
            # We can use the same collection but filter by metadata
            self.collection = self.client.get_or_create_collection(name="cs_concepts")
        except Exception as e:
            print(f"CRITICAL ERROR: Failed to initialize ChromaDB: {e}")
            self.client = None
            self.collection = None


    def add_documents(self, documents: list[str], metadatas: list[dict], ids: list[str]):
        """
        Add documents to the collection.
        """
        if not self.collection:
            return False
            
        try:
            self.collection.add(
                documents=documents,
                metadatas=metadatas,
                ids=ids
            )
            return True
        except Exception as e:
            print(f"Error adding documents: {e}")
            return False

    def query(self, query_text: str, n_results: int = 2) -> list[str]:
        """
        Retrieve relevant documents for a given query.
        """
        if not self.collection:
            return []

        try:
            results = self.collection.query(
                query_texts=[query_text],
                n_results=n_results
            )
            # results['documents'] is a list of lists (one list per query)
            if results and results['documents']:
                return results['documents'][0]
            return []
        except Exception as e:
            print(f"Error querying ChromaDB: {e}")
            return []
            
    def get_visualizer(self, name: str) -> dict:
        """
        Retrieve a specific visualizer by name from the collection.
        Uses metadata filtering for precise retrieval.
        """
        if not self.collection:
            return None

        try:
            # We search for something with type='visualization' and algo=name
            # Or we can do a semantic search if exact match fails, but let's try exact filtering first
            results = self.collection.get(
                where={"$and": [{"type": "visualization"}, {"algo": name}]},
                include=["documents", "metadatas"]
            )
            
            if results and results['documents']:
                return {
                    "code": results['documents'][0],
                    "metadata": results['metadatas'][0]
                }
            
            return None

        except Exception as e:
            print(f"Error retrieving visualizer {name}: {e}")
            return None

rag_service = RAGService()
