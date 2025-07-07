from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os
from pathlib import Path

# Caminho absoluto até a pasta backend (um nível acima de /app)
env_path = Path(__file__).resolve().parents[1] / ".env"
load_dotenv(dotenv_path=env_path)

# Acessa as variáveis
db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")
db_host = os.getenv("DB_HOST")
db_port = os.getenv("DB_PORT")
db_name = os.getenv("DB_NAME")

# Define a URL de conexão com o banco de dados PostgreSQL
DATABASE_URL = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"

# Cria a engine de conexão com o banco de dados
engine = create_engine(DATABASE_URL)

# Cria uma fábrica de sessões de banco de dados (SessionLocal)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Injeção de dependência
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
