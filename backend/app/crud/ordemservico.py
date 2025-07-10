from sqlalchemy.orm import Session
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from backend.app.schemas.ordemservico import OrdemServico, OrdemServicoGet
from backend.app.crud import pessoa as pessoa_crud
from typing import Optional, List

def listar_ordemservicos(db: Session) -> List[OrdemServicoGet]:
    """
    Retorna uma lista de todas as ordemservicos cadastradas no banco de dados.
    Args:
        db (Session): Sessão ativa com o banco de dados.
    Returns:
        List[OrdemServicoGet]: Lista de objetos do tipo OrdemServicoGet contendo os dados de cada ordemservico.
    """
    # Preparando a expressão SQL
    query = text("""
        SELECT
            id_ordemservico, dt_ordemservico, local, descricao, id_pessoa
        FROM ordemservico
    """)
    
    # Executando a query e salvando o resultado
    result = db.execute(query).mappings().all()
    if result is None: return list()
        
    # Retornando lista de OrdemServicoGet
    return [
        OrdemServicoGet(
            id_ordemservico=row["id_ordemservico"], 
            dt_ordemservico=row["dt_ordemservico"],
            local=row["local"],
            descricao=row["descricao"],
            id_pessoa=row["id_pessoa"]
        ) 
        for row in result
    ]

def criar_ordemservico(db: Session, ordemservico: OrdemServico) -> Optional[int]:
    """
    Insere uma nova ordemservico na tabela `ordemservico`.
    Args:
        db (Session): Sessão ativa com o banco de dados.
        ordemservico (OrdemServico): Objeto contendo os dados da ordemservico a ser inserida.
    Returns:
        Optional[int]: ID da ordemservico criada, ou None em caso de falha.
    Raises:
        SQLAlchemyError: Caso ocorra algum erro durante a execução ou commit da transação.
    """    
    # Validação de chaves estrangeiras
    if pessoa_crud.buscar_pessoa(db, ordemservico.id_pessoa) is None: 
        return None
    
    # Preparando a expressão SQL
    param = ordemservico.dict()
    query = text("""
        INSERT INTO ordemservico (dt_ordemservico, local, descricao, id_pessoa)
        VALUES (:dt_ordemservico, :local, :descricao, :id_pessoa)
        RETURNING id_ordemservico
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

def atualizar_ordemservico(db: Session, ordemservico: OrdemServico, id_ordemservico: int) -> Optional[int]:
    """
    Atualiza os dados de uma ordemservico existente com base no ID informado.
    Args:
        db (Session): Sessão ativa com o banco de dados.
        ordemservico (OrdemServico): Objeto contendo os novos dados da ordemservico.
        id_ordemservico (int): ID da ordemservico a ser atualizada.
    Returns:
        Optional[int]: ID da ordemservico atualizada, ou None em caso de falha.
    Raises:
        SQLAlchemyError: Caso ocorra algum erro durante a execução ou commit da transação.
    """
    # Validação de chaves estrangeiras
    if pessoa_crud.buscar_pessoa(db, ordemservico.id_pessoa) is None: 
        return None
    
    # Preparando a expressão SQL
    param = ordemservico.dict()
    param.update({"id_ordemservico": id_ordemservico})
    query = text("""
        UPDATE ordemservico
        SET 
            dt_ordemservico=:dt_ordemservico, local=:local, descricao=:descricao, id_pessoa=:id_pessoa
        WHERE id_ordemservico=:id_ordemservico
        RETURNING id_ordemservico
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

def remover_ordemservico(db: Session, id_ordemservico: int) -> Optional[int]:
    """
    Remove uma ordemservico da tabela `ordemservico` com base no ID informado.
    Args:
        db (Session): Sessão ativa com o banco de dados.
        id_ordemservico (int): ID da ordemservico a ser removida.
    Returns:
        Optional[int]: ID da ordemservico removida, ou None caso não exista.
    Raises:
        SQLAlchemyError: Caso ocorra algum erro durante a execução ou commit da transação.
    """
    # Preparando a expressão SQL
    query = text("""
        DELETE FROM ordemservico WHERE id_ordemservico=:id_ordemservico RETURNING id_ordemservico
    """)

    # Protegendo de excessões
    try:
        # Executando a query e salvando o resultado
        result = db.execute(query, {"id_ordemservico": id_ordemservico})
        db.commit()
        return result.scalar()      # Retorna o id em caso de sucesso
    except SQLAlchemyError as e:
        db.rollback()               # Reverte a transação em caso de erro
        raise e

def buscar_ordemservico(db: Session, id_ordemservico: int) -> Optional[OrdemServicoGet]:
    """
    Busca uma ordemservico pelo ID na tabela `ordemservico`.
    Args:
        db (Session): Sessão ativa com o banco de dados.
        id_ordemservico (int): ID da ordemservico a ser consultada.
    Returns:
        Optional[OrdemServicoGet]: Objeto contendo os dados da ordemservico, ou None se não encontrada.
    """
    # Preparando a expressão SQL
    query = text("""
        SELECT 
            id_ordemservico, dt_ordemservico, local, descricao, id_pessoa
        FROM ordemservico
        WHERE id_ordemservico=:id_ordemservico
        LIMIT 1
    """)
    
    # Executando a query e salvando o resultado
    result = db.execute(query, {"id_ordemservico": id_ordemservico}).mappings().fetchone()
    if result is None: return None

    # Retornando OrdemServicoGet
    return OrdemServicoGet(
        id_ordemservico=result["id_ordemservico"], 
        dt_ordemservico=result["dt_ordemservico"],
        local=result["local"],
        descricao=result["descricao"],
        id_pessoa=result["id_pessoa"]
    )
