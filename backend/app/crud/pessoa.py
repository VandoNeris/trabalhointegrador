from sqlalchemy.orm import Session
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from backend.app.schemas.pessoa import Pessoa, PessoaGet
from typing import Optional, List

def listar_pessoas(db: Session) -> List[PessoaGet]:
    """
    Retorna uma lista de todas as pessoas cadastradas no banco de dados.
    Args:
        db (Session): Sessão ativa com o banco de dados.
    Returns:
        List[PessoaGet]: Lista de objetos do tipo PessoaGet contendo os dados de cada pessoa.
    """
    query = text("""
        SELECT
            id_pessoa, tipo, nome, endereco, telefone, cpf, cnpj, razaosocial
        FROM pessoa
    """)

    result = db.execute(query).all()
    if result is None: return list()
    return [
        PessoaGet(
            id_pessoa=row[0], tipo=row[1], nome=row[2], endereco=row[3],
            telefone=row[4], cpf=row[5], cnpj=row[6], razaosocial=row[7]
        ) for row in result
    ]

def criar_pessoa(db: Session, pessoa: Pessoa) -> Optional[int]:
    """
    Insere uma nova pessoa na tabela `pessoa`.
    Args:
        db (Session): Sessão ativa com o banco de dados.
        pessoa (Pessoa): Objeto contendo os dados da pessoa a ser inserida.
    Returns:
        Optional[int]: ID da pessoa criada, ou None em caso de falha.
    Raises:
        SQLAlchemyError: Caso ocorra algum erro durante a execução ou commit da transação.
    """
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
    """
    Atualiza os dados de uma pessoa existente com base no ID informado.
    Args:
        db (Session): Sessão ativa com o banco de dados.
        pessoa (Pessoa): Objeto contendo os novos dados da pessoa.
        id_pessoa (int): ID da pessoa a ser atualizada.
    Returns:
        Optional[int]: ID da pessoa atualizada, ou None em caso de falha.
    Raises:
        SQLAlchemyError: Caso ocorra algum erro durante a execução ou commit da transação.
    """
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
    """
    Remove uma pessoa da tabela `pessoa` com base no ID informado.
    Args:
        db (Session): Sessão ativa com o banco de dados.
        id_pessoa (int): ID da pessoa a ser removida.
    Returns:
        Optional[int]: ID da pessoa removida, ou None caso não exista.
    Raises:
        SQLAlchemyError: Caso ocorra algum erro durante a execução ou commit da transação.
    """
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
    """
    Busca uma pessoa pelo ID na tabela `pessoa`.
    Args:
        db (Session): Sessão ativa com o banco de dados.
        id_pessoa (int): ID da pessoa a ser consultada.
    Returns:
        Optional[PessoaGet]: Objeto contendo os dados da pessoa, ou None se não encontrada.
    """
    param = {"id_pessoa": id_pessoa}
    query = text("""
        SELECT 
            id_pessoa, tipo, nome, endereco, telefone, cpf, cnpj, razaosocial
        FROM pessoa
        WHERE id_pessoa = :id_pessoa
        LIMIT 1
    """)

    result = db.execute(query, param).fetchone()
    if result is None: return None
    return PessoaGet(
        id_pessoa=result[0], tipo=result[1], nome=result[2], endereco=result[3],
        telefone=result[4], cpf=result[5], cnpj=result[6], razaosocial=result[7]
    )
