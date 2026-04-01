from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from .base import Base
from app.core.config import get_settings

settings = get_settings()
engine = create_async_engine(
    settings.get_database_url_async(),
    echo=False,
)
AsyncSessionLocal = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False, autoflush=False)


async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
