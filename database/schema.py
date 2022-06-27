from config import postgres
from sqlalchemy import (
    BigInteger,
    Column,
)
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# engine = create_async_engine(
#     f"postgresql+asyncpg://{postgres['user']}:{postgres['password']}@{postgres['host']}:{postgres['port']}/{postgres['database']}",
#     echo=False,
#     pool_size=5,
#     pool_timeout=60,
#     max_overflow=9,
# )
Base = declarative_base()
metadata = Base.metadata

# async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

async_session = ""


class Guilds(Base):
    __tablename__ = "Guilds"
    id = Column(BigInteger, primary_key=True)
