from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Request, status
from fastapi.responses import JSONResponse
from sqlalchemy import text

from app.core.database import SessionDep, engine
from app.core.exceptions import AppError
from app.modules.user.router import router as user_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    await engine.dispose()


app = FastAPI(lifespan=lifespan)

app.include_router(user_router, prefix="/users", tags=["users"])


@app.get("/health")
async def health_check(session: SessionDep):
    """Health check endpoint to verify database connectivity."""
    try:
        await session.execute(text("SELECT 1"))
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database unavailable",
        ) from exc
    return {"status": "connected"}


@app.exception_handler(AppError)
async def app_error_handler(request: Request, exc: AppError):

    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )
