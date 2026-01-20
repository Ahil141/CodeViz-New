from app.services.rag_service import rag_service
import time

def test_rag():
    print("Testing RAG Service...")
    
    # 1. Add Documents
    docs = [
        "Bubble Sort is the simplest sorting algorithm that works by repeatedly swapping the adjacent elements if they are in wrong order.",
        "Merge Sort is a Divide and Conquer algorithm. It divides the input array into two halves, calls itself for the two halves, and then merges the two sorted halves.",
        "QuickSort is a Divide and Conquer algorithm. It picks an element as pivot and partitions the given array around the picked pivot."
    ]
    metadatas = [{"source": "geeksforgeeks"}, {"source": "geeksforgeeks"}, {"source": "geeksforgeeks"}]
    ids = ["bubble_sort", "merge_sort", "quick_sort"]
    
    print("Adding documents...")
    rag_service.add_documents(documents=docs, metadatas=metadatas, ids=ids)
    
    # 2. Query
    query = "explain bubble sort"
    print(f"Querying for: '{query}'")
    results = rag_service.query(query)
    
    print("\nResults:")
    for doc in results:
        print(f"- {doc}")

if __name__ == "__main__":
    test_rag()
