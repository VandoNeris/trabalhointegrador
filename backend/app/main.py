from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text

from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import  List

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# URL de conexão com o PostgreSQL
# Formato: "postgresql://usuario:senha@host:porta/nomedobanco"
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:postgres@localhost:5432/tractodatabase"

# Cria a engine de conexão com o banco de dados
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Cria uma fábrica de sessões (SessionLocal) que será usada para criar sessões de banco de dados
# autocommit=False e autoflush=False são configurações padrão para sessões em APIs
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Retorna uma classe base para os modelos ORM. Nossos modelos herdarão desta classe.
Base = declarative_base()

# Função para obter uma sessão do banco de dados (será usada com Injeção de Dependência no FastAPI)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class Cliente(BaseModel):
    nome: str

class Maquina(BaseModel):
    id: int
    desc: str

class Servico(BaseModel):
    id: int
    desc: str
    horas: int
    quilometros: int

class ClienteGet(Cliente):
    id: int

class Pessoa(BaseModel):
    tipo: bool
    nome: str
    endereco: str
    telefone: str
    cpf: str | None = None
    cnpj: str | None = None
    razaosocial: str | None = None

class PessoaGet(Pessoa):
    id_pessoa: int

@app.get("/pessoas", response_model=List[PessoaGet])
def listar_pessoas(db: Session = Depends(get_db)):
    result = db.execute(text("SELECT id_pessoa, tipo, nome, endereco, telefone, cpf, cnpj, razaosocial FROM public.pessoa;"))
    pessoas = [PessoaGet(id_pessoa=row[0], tipo=row[1], nome=row[2], endereco=row[3], telefone=row[4], cpf=row[5], cnpj=row[6], razaosocial=row[7]) for row in result.all()]
    return pessoas

@app.post("/pessoas")
def criar_pessoa(pessoa: Pessoa, db: Session = Depends(get_db)):
    valores = {"tipo": pessoa.tipo,
               "nome": pessoa.nome,
               "endereco": pessoa.endereco,
               "telefone": pessoa.telefone,
               "cpf": pessoa.cpf,
               "cnpj": pessoa.cnpj,
               "razaosocial": pessoa.razaosocial}
    db.execute(text("INSERT INTO pessoa (tipo, nome, endereco, telefone, cpf, cnpj, razaosocial) VALUES (:tipo, :nome, :endereco, :telefone, :cpf, :cnpj, :razaosocial)"), valores)
    db.commit()
    return {"message": "Pessoa Cadastrada"}

@app.delete("/clientes/{cliente_id}")
def remover_cliente(cliente_id: int):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("DELETE FROM cliente WHERE id=?", (cliente_id,))
    conn.commit()
    conn.close()
    return {"ok": True}

@app.get("/maquinas", response_model=List[Maquina])
def listar_maquinas():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT id, nome FROM maquina ORDER BY id DESC")
    maquinas = [Maquina(id=row[0], nome=row[1]) for row in c.fetchall()]
    conn.close()
    return maquinas

@app.post("/maquinas", response_model=Maquina)
def criar_maquina():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("INSERT INTO maquina (nome, desc) VALUES (?, ?)", ("Nova Máquina",))
    conn.commit()
    new_id = c.lastrowid
    conn.close()
    return Maquina(id=new_id, nome="Nova Máquina")

@app.delete("/maquinas/{maquina_id}")
def remover_maquina(maquina_id: int):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("DELETE FROM maquina WHERE id=?", (maquina_id,))
    conn.commit()
    conn.close()
    return {"ok": True}


@app.get("/servicos", response_model=List[Servico])
def listar_servicos():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT id, desc, horas, quilometros FROM servico ORDER BY id DESC")
    servicos = [Servico(id=row[0], desc=row[1], horas=row[2], quilometros=row[3]) for row in c.fetchall()]
    conn.close()
    return servicos

@app.post("/servicos", response_model=Servico) 
def criar_servico(servico: Servico):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("INSERT INTO servico (desc, horas, quilometros) VALUES (?, ?, ?)",
              (servico.desc, servico.horas, servico.quilometros))
    conn.commit()
    new_id = c.lastrowid
    conn.close()
    return Servico(id=new_id, desc=servico.desc, horas=servico.horas, quilometros=servico.quilometros)

@app.delete("/servicos/{servico_id}")
def remover_servico(servico_id: int):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("DELETE FROM servico WHERE id=?", (servico_id,))
    conn.commit()
    conn.close()
    return {"ok": True}
