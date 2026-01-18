

import sys
import traceback

with open("verification_result.txt", "w") as f:
    f.write("Starting import test...\n")
    try:
        from app.services.rag_service import rag_service
        f.write("Import successful!\n")
        f.write(f"Collection: {rag_service.collection}\n")
    except Exception as e:
        f.write("Import failed!\n")
        f.write(str(e) + "\n")
        traceback.print_exc(file=f)

