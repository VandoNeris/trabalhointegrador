from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from typing import AsyncGenerator
from backend.app.core.config import settings

# Acessa as variáveis
db_user = settings.DB_USER
db_password = settings.DB_PASSWORD
db_host = settings.DB_HOST
db_port = settings.DB_PORT
db_name = settings.DB_NAME

# Define a URL de conexão com o banco de dados PostgreSQL
DATABASE_URL = f"postgresql+asyncpg://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"

# Estabelecendo conexão com o banco
engine = create_async_engine(DATABASE_URL, echo=True)
AsyncSessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

# Dependência para FastAPI
async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session
