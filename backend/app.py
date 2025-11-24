"""
Main application file for the FastAPI backend.
Sets up the app, database, and includes routes.
"""

import os
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from backend.db.wallet import Base
from backend.routes.wallets import router


DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///wallets.db")

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

origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

frontend_origin = os.getenv("FRONTEND_ORIGIN")
if frontend_origin:
    origins.append(frontend_origin)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", tags=["Health Check"])
async def health_check():
    """Health check endpoint."""
    return {"status": "ok"}


app.include_router(router)
