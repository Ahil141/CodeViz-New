import os
import sys
from typing import List, Dict, Any

# Add backend directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))

from app.db.chroma_store import get_chroma_store

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")

def parse_document(file_path: str) -> Dict[str, Any]:
    """
    Parse a document file with metadata headers.
    
    Headers format:
    ### KEY: VALUE
    
    Returns:
        Dict with 'content', 'metadata', and 'id'
    """
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
        
    lines = content.split("\n")
    metadata = {}
    body_start_index = 0
    
    for i, line in enumerate(lines):
        if line.startswith("### "):
            try:
                key, value = line[4:].split(":", 1)
                metadata[key.strip().lower()] = value.strip()
            except ValueError:
                continue
        elif line.strip() == "":
            continue
        else:
            body_start_index = i
            break
            
    body = "\n".join(lines[body_start_index:])
    
    # Normalize metadata keys
    # Map 'document_type' -> 'type' (to match schema preference)
    if "document_type" in metadata:
        metadata["type"] = metadata.pop("document_type").lower()
    
    # Construct a stable ID
    name = metadata.get("name", os.path.basename(file_path))
    doc_id = f"{metadata.get('type', 'generic')}_{name.replace(' ', '_')}"
    
    return {
        "content": body,
        "metadata": metadata,
        "id": doc_id
    }

def load_data():
    store = get_chroma_store()
    
    documents = []
    metadatas = []
    ids = []
    
    print(f"Scanning {DATA_DIR}...")
    
    for root, _, files in os.walk(DATA_DIR):
        for file in files:
            if file.endswith(".txt") or file.endswith(".html") or file.endswith(".py"):
                file_path = os.path.join(root, file)
                try:
                    doc = parse_document(file_path)
                    
                    # Only add if content is not empty
                    if doc["content"].strip():
                        documents.append(doc["content"])
                        metadatas.append(doc["metadata"])
                        ids.append(doc["id"])
                        print(f"Prepared: {doc['id']}")
                except Exception as e:
                    print(f"Error parsing {file}: {e}")

    if documents:
        print(f"Ingesting {len(documents)} documents...")
        # Use upsert to handle updates
        store.collection.upsert(
            documents=documents,
            metadatas=metadatas,
            ids=ids
        )
        print("Ingestion complete.")
    else:
        print("No documents found to ingest.")

if __name__ == "__main__":
    load_data()
