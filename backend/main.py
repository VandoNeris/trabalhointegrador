
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
