import uvicorn
import os
import sys

# Ensure backend dir is in path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from app.main import app
    print("Successfully imported app.")
except Exception as e:
    import traceback
    with open("error.log", "w") as f:
        f.write(traceback.format_exc())
    traceback.print_exc()
    print(f"Failed to import app: {e}")
    sys.exit(1)

if __name__ == "__main__":
    print("Starting server...")
    uvicorn.run(app, host="127.0.0.1", port=8000)
