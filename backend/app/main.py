
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
import sqlite3

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DB_PATH = "clientes2.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS cliente(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL
        );
    """)
    conn.commit()
    conn.close()

init_db()

class ClienteIn(BaseModel):
    nome: str

class Cliente(ClienteIn):
    id: int

class Maquina(BaseModel):
    id: int
    desc: str

class Servico(BaseModel):
    id: int
    desc: str
    horas: int
    quilometros: int

@app.get("/clientes", response_model=List[Cliente])
def listar_clientes():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT id, nome FROM cliente ORDER BY id DESC")
    clientes = [Cliente(id=row[0], nome=row[1]) for row in c.fetchall()]
    conn.close()
    return clientes

@app.post("/clientes", response_model=Cliente)
def criar_cliente(cliente: ClienteIn):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("INSERT INTO cliente (nome) VALUES (?)", (cliente.nome,))
    conn.commit()
    new_id = c.lastrowid
    conn.close()
    return Cliente(id=new_id, nome=cliente.nome)

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




