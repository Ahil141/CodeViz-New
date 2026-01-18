import os
import glob
from app.services.rag_service import rag_service

def ingest_frontend_components():
    # Define paths relative to backend logic or project root
    # Assuming this script runs from backend/
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    frontend_base = os.path.join(project_root, "frontend", "src", "components")
    
    target_dirs = [
        os.path.join(frontend_base, "dataStructures"),
        os.path.join(frontend_base, "algorithms")
    ]
    
    documents = []
    metadatas = []
    ids = []
    
    print(f"Scanning directories: {target_dirs}")
    
    for directory in target_dirs:
        if not os.path.exists(directory):
            print(f"Warning: Directory not found: {directory}")
            continue
            
        # Recursive search for .tsx files
        # Using glob with recursive=True
        pattern = os.path.join(directory, "**", "*.tsx")
        files = glob.glob(pattern, recursive=True)
        
        for filepath in files:
            try:
                # Normalize path separators
                filepath = os.path.normpath(filepath)
                
                # Create a readable ID and name
                filename = os.path.basename(filepath)
                rel_path = os.path.relpath(filepath, frontend_base)
                
                # Determine category based on path
                if "dataStructures" in rel_path:
                    category = "data_structure_component"
                    # Try to extract specific DS name, e.g. "stack" from "dataStructures/stack/..."
                    parts = rel_path.split(os.sep)
                    # parts[0] is 'dataStructures', parts[1] is likely the DS folder name
                    algo_name = parts[1] if len(parts) > 1 else "unknown"
                elif "algorithms" in rel_path:
                    category = "algorithm_component"
                    algo_name = os.path.splitext(filename)[0] # e.g. SortingAlgorithms
                else:
                    category = "frontend_component"
                    algo_name = "general"

                with open(filepath, "r", encoding="utf-8") as f:
                    content = f.read()
                
                # Add context to the document
                doc_content = f"File: {filename}\nPath: {rel_path}\nType: React Component\n\n{content}"
                
                documents.append(doc_content)
                metadatas.append({
                    "type": "source_code",
                    "category": category,
                    "algo": algo_name,
                    "filename": filename,
                    "path": rel_path
                })
                ids.append(f"fe_{rel_path.replace(os.sep, '_')}")
                
            except Exception as e:
                print(f"Error processing {filepath}: {e}")

    if documents:
        print(f"Found {len(documents)} components. Ingesting into VectorDB...")
        success = rag_service.add_documents(documents, metadatas, ids)
        if success:
            print("Successfully ingested frontend components.")
        else:
            print("Failed to ingest frontend components.")
    else:
        print("No component files found.")

if __name__ == "__main__":
    ingest_frontend_components()
