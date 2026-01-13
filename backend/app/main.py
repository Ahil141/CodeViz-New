from typing import Dict, Any
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import chat, rag, smart_chat


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for startup/shutdown events."""
    # Startup: Preload the LLM model
    print("=" * 50)
    print("🚀 Starting CodeLearn AI...")
    print("=" * 50)
    print("📦 Preloading LLM model (this takes 30-60 seconds)...")
    
    try:
        # Use preload_llm to ensure the shared instance is created
        from app.api.smart_chat import preload_llm
        preload_llm()
        print("✅ LLM model loaded successfully!")
    except Exception as e:
        print(f"⚠️ Warning: Failed to preload LLM: {e}")
        print("   LLM will be loaded on first request instead.")
    
    print("=" * 50)
    print("✅ CodeLearn AI is ready!")
    print("=" * 50)
    
    yield  # Server runs here
    
    # Shutdown
    print("👋 Shutting down CodeLearn AI...")


app = FastAPI(
    title="CodeLearn AI",
    description="AI-powered data structures learning platform",
    version="1.0.0",
    lifespan=lifespan,
)

# CORS configuration for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:5173",
        "http://localhost:8080",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:8080",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health check endpoint
@app.get("/health")
async def health_check() -> Dict[str, str]:
    """Health check endpoint for monitoring."""
    return {"status": "healthy", "service": "codelearn-ai"}

# Include API routers
app.include_router(chat.router, prefix="/api/chat", tags=["chat"])
app.include_router(rag.router, prefix="/api/rag", tags=["rag"])
app.include_router(smart_chat.router, prefix="/api/smart-chat", tags=["smart-chat"])

@app.get("/")
async def root() -> Dict[str, Any]:
    """Root endpoint."""
    return {
        "message": "CodeLearn AI API",
        "version": "1.0.0",
        "docs": "/docs",
    }
