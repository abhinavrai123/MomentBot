import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, Session
from contextlib import asynccontextmanager

# Load database URL from environment variable
DATABASE_URL = "sqlite+aiosqlite:////Users/abhinavrai/PycharmProjects/MomentBot/data/data.db"

engine = create_async_engine(DATABASE_URL, echo=False)

# Create session factory
AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False
)

@asynccontextmanager
async def get_session() -> AsyncSession:
    """Returns an async database session."""
    async with AsyncSessionLocal() as session:
        yield session  # for use with dependency injection, like FastAPI