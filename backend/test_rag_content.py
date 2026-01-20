

from app.services.rag_service import rag_service
import json
import traceback

def test_rag_retrieval():
    query = "linked list"
    try:
        results = rag_service.query(query)
        print(f"Query: {query}")
        print(f"Number of results: {len(results)}")
        for i, res in enumerate(results):
            print(f"\n--- Result {i+1} ---")
            print(res[:500] + "..." if len(res) > 500 else res)

    except Exception:
        with open("traceback_log.txt", "w") as f:
            traceback.print_exc(file=f)


if __name__ == "__main__":
    test_rag_retrieval()

