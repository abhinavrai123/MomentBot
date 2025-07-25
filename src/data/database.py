from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
DB_URL = "sqlite+aiosqlite:////Users/abhinavrai/PycharmProjects/MomentBot/data/data.db"


Base = declarative_base()
async_engine = create_async_engine(DB_URL, echo=True)

async def init_db():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)