from config import settings
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

engine = create_async_engine(
    settings.DB.URL,
    echo=True,
)

AsyncSessionFactory = async_sessionmaker(
    bind=engine,
    autoflush=False,
    expire_on_commit=False,
)


async def get_db_session() -> AsyncSession:
    async with AsyncSessionFactory() as session:
        yield session
