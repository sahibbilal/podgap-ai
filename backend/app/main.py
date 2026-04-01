from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import traceback

from app.core.config import get_settings
from app.db.session import init_db
from app.api import auth
from app.api.deps import get_current_user_optional
from app.api.routes import router as api_router

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield
    # shutdown if needed


app = FastAPI(
    title=settings.project_name,
    lifespan=lifespan,
)

# CORS middleware - must be added before routes
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.backend_cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
    max_age=3600,
)

# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    print(f"Global exception: {exc}")
    traceback.print_exc()
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"},
    )

app.include_router(auth.router, prefix=settings.api_v1_prefix)
app.include_router(api_router, prefix=settings.api_v1_prefix)


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.get("/debug/config")
async def debug_config():
    """Debug endpoint to verify configuration"""
    return {
        "cors_origins": settings.backend_cors_origins,
        "api_prefix": settings.api_v1_prefix,
        "project_name": settings.project_name,
    }
