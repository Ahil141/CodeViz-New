from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.main import api_router
from app.api.endpoints import rag_endpoint

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# Set all CORS enabled origins
if settings.CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.include_router(api_router, prefix=settings.API_V1_STR)
app.include_router(rag_endpoint.router, prefix=f"{settings.API_V1_STR}/rag", tags=["rag"])
from app.api.endpoints import execute
app.include_router(execute.router, prefix=f"{settings.API_V1_STR}/execute", tags=["execute"])

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "project": settings.PROJECT_NAME,
        "version": "0.1.0"
    }

@app.get("/")
def root():
    return {"message": "Welcome to CodeViz 2.0 API"}
