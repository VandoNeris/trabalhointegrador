from sqlalchemy.orm import Session
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from backend.app.schemas.pessoa import Pessoa, PessoaGet
from typing import Optional, List

def listar_pessoas(db: Session) -> List[PessoaGet]:
    query = text("""
        SELECT 
            id_pessoa, tipo, nome, endereco, telefone, cpf, cnpj, razaosocial
        FROM pessoa
    """)

    try:
        result = db.execute(query).all()
        if result is None: return list()
        return [
            PessoaGet(
                id_pessoa=row[0], tipo=row[1], nome=row[2], endereco=row[3],
                telefone=row[4], cpf=row[5], cnpj=row[6], razaosocial=row[7]
            ) for row in result
        ]
    except SQLAlchemyError as e:
        raise e



def criar_pessoa(db: Session, pessoa: Pessoa) -> Optional[int]:
    param = pessoa.dict()
    query = text("""
        INSERT INTO pessoa (tipo, nome, endereco, telefone, cpf, cnpj, razaosocial)
        VALUES (:tipo, :nome, :endereco, :telefone, :cpf, :cnpj, :razaosocial)
        RETURNING id_pessoa
    """)

    try:
        result = db.execute(query, param)
        db.commit()
        return result.scalar()
    except SQLAlchemyError as e:
        db.rollback()
        raise e

def atualizar_pessoa(db: Session, pessoa: Pessoa, id_pessoa: int) -> Optional[int]:
    param = pessoa.dict()
    param.update({"id_pessoa": id_pessoa})
    query = text("""
        UPDATE pessoa
        SET 
            tipo = :tipo, 
            nome = :nome, 
            endereco = :endereco, 
            telefone = :telefone,
            cpf = :cpf, 
            cnpj = :cnpj, 
            razaosocial = :razaosocial
        WHERE id_pessoa = :id_pessoa
        RETURNING id_pessoa
    """)

    try:
        result = db.execute(query, param)
        db.commit()
        return result.scalar()
    except SQLAlchemyError as e:
        db.rollback()
        raise e

def remover_pessoa(db: Session, id_pessoa: int) -> Optional[int]:
    param = {"id_pessoa": id_pessoa}
    query = text("""
        DELETE FROM pessoa WHERE id_pessoa = :id_pessoa RETURNING id_pessoa
    """)

    try:
        result = db.execute(query, param)
        db.commit()
        return result.scalar()
    except SQLAlchemyError as e:
        db.rollback()
        raise e

def buscar_pessoa(db: Session, id_pessoa: int) -> Optional[PessoaGet]:
    param = {"id_pessoa": id_pessoa}
    query = text("""
        SELECT 
            id_pessoa, tipo, nome, endereco, telefone, cpf, cnpj, razaosocial
        FROM pessoa
        WHERE id_pessoa = :id_pessoa
        LIMIT 1
    """)

    try: 
        result = db.execute(query, param).fetchone()
        if result is None: return None
        return PessoaGet(
            id_pessoa=result[0], tipo=result[1], nome=result[2], endereco=result[3],
            telefone=result[4], cpf=result[5], cnpj=result[6], razaosocial=result[7]
        )
    except SQLAlchemyError as e:
        raise e
