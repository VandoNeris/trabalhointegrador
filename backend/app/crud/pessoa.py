from sqlalchemy.orm import Session
from sqlalchemy import text
from backend.app.schemas.pessoa import Pessoa, PessoaGet

def listar_pessoas(db: Session):
    query = text("""
        SELECT id_pessoa, tipo, nome, endereco, telefone, cpf, cnpj, razaosocial FROM pessoa
    """)
    result = db.execute(query)

    return [ PessoaGet(
        id_pessoa=row[0], tipo=row[1], nome=row[2], endereco=row[3],telefone=row[4], cpf=row[5], cnpj=row[6], razaosocial=row[7]
    ) for row in result.all() ]

def criar_pessoa(db: Session, pessoa: Pessoa):
    valores = pessoa.dict()
    query = text("""
        INSERT INTO pessoa (tipo, nome, endereco, telefone, cpf, cnpj, razaosocial)
        VALUES (:tipo, :nome, :endereco, :telefone, :cpf, :cnpj, :razaosocial)
    """)
    db.execute(query, valores)
    db.commit()

def remover_pessoa(db: Session, id_pessoa: int):
    valores = pessoa.dict()
    query = text("""
        INSERT INTO pessoa (tipo, nome, endereco, telefone, cpf, cnpj, razaosocial)
        VALUES (:tipo, :nome, :endereco, :telefone, :cpf, :cnpj, :razaosocial)
    """)
    db.execute(query, valores)
    db.commit()
