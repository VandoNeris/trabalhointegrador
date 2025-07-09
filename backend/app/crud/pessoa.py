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
    # Preparando a expressão SQL
    query = text("""
        SELECT
            id_pessoa, tipo, nome, endereco, email, telefone, cpf, cnpj, razaosocial
        FROM pessoa WHERE tipo = false
    """)
    
    # Executando a query e salvando o resultado
    result = db.execute(query).mappings().all()
    if result is None: return list()
    
    # Retornando lista de PessoaGet
    return [
        PessoaGet(
            id_pessoa=row["id_pessoa"], tipo=row["tipo"], nome=row["nome"], endereco=row["endereco"], email=row["email"], telefone=row["telefone"], cpf=row["cpf"], cnpj=row["cnpj"], razaosocial=row["razaosocial"]
        ) 
        for row in result
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
    # Preparando a expressão SQL
    # Executando a query e salvando o resultado
    param = pessoa.dict()
    query = text("""
        INSERT INTO pessoa (tipo, nome, endereco, email, telefone, cpf, cnpj, razaosocial)
        VALUES (:tipo, :nome, :endereco, :email, :telefone, :cpf, :cnpj, :razaosocial)
        RETURNING id_pessoa
    """)

    # Protegendo de excessões
    try:
        # Executando a query e salvando o resultado
        result = db.execute(query, param)
        db.commit()
        return result.scalar()      # Retorna o id em caso de sucesso
    except SQLAlchemyError as e:
        db.rollback()               # Reverte a transação em caso de erro
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
    # Preparando a expressão SQL
    param = pessoa.dict()
    param.update({"id_pessoa": id_pessoa})
    query = text("""
        UPDATE pessoa
        SET 
            tipo=:tipo, nome=:nome, endereco=:endereco, email=:email, telefone=:telefone, cpf=:cpf, cnpj=:cnpj, razaosocial=:razaosocial
        WHERE id_pessoa = :id_pessoa
        RETURNING id_pessoa
    """)

    # Protegendo de excessões
    try:
        # Executando a query e salvando o resultado
        result = db.execute(query, param)
        db.commit()
        return result.scalar()      # Retorna o id em caso de sucesso
    except SQLAlchemyError as e:
        db.rollback()               # Reverte a transação em caso de erro
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
    # Preparando a expressão SQL
    query = text("""
        DELETE FROM pessoa WHERE id_pessoa = :id_pessoa RETURNING id_pessoa
    """)

    # Protegendo de excessões
    try:
        # Executando a query e salvando o resultado
        result = db.execute(query, {"id_pessoa": id_pessoa})
        db.commit()
        return result.scalar()      # Retorna o id em caso de sucesso
    except SQLAlchemyError as e:
        db.rollback()               # Reverte a transação em caso de erro
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
    # Preparando a expressão SQL
    query = text("""
        SELECT 
            id_pessoa, tipo, nome, endereco, email, telefone, cpf, cnpj, razaosocial
        FROM pessoa
        WHERE id_pessoa = :id_pessoa
        LIMIT 1
    """)
    
    # Executando a query e salvando o resultado
    result = db.execute(query, {"id_pessoa": id_pessoa}).mappings().fetchone()
    if result is None: return None

    # Retornando PessoaGet
    return PessoaGet(
        id_pessoa=result["id_pessoa"],
        tipo=result["tipo"],
        nome=result["nome"],
        endereco=result["endereco"],
        email=result["email"],
        telefone=result["telefone"],
        cpf=result["cpf"],
        cnpj=result["cnpj"],
        razaosocial=result["razaosocial"]
    )
