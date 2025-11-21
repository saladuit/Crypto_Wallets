from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from backend.db.wallet import Base
from backend.routes.wallets import router


DATABASE_URL = "sqlite:///wallets.db"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)


@asynccontextmanager
async def lifespan(_app: FastAPI):
    """Create the database tables on startup and drop them on shutdown."""
    Base.metadata.create_all(bind=engine)
    try:
        yield
    finally:
        Base.metadata.drop_all(bind=engine)


app = FastAPI(lifespan=lifespan)

# Add permissive CORS for local frontend development (vite runs on :3000).
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(router, prefix="/api")
