from sqlalchemy.orm import Session
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from backend.app.schemas.compra import Compra, CompraGet
from backend.app.crud import pessoa as pessoa_crud
from typing import Optional, List

def listar_compras(db: Session) -> List[CompraGet]:
    """
    Retorna uma lista de todas as compras cadastradas no banco de dados.
    Args:
        db (Session): Sessão ativa com o banco de dados.
    Returns:
        List[CompraGet]: Lista de objetos do tipo CompraGet contendo os dados de cada compra.
    """
    # Preparando a expressão SQL
    query = text("""
        SELECT
            dt_emissao, dt_vencimento, dt_pagamento, status_pag, valor, loc_entrega, id_pessoa
        FROM compra
    """)
    
    # Executando a query e salvando o resultado
    result = db.execute(query).mappings().all()
    if result is None: return list()
    
    # Retornando lista de CompraGet
    return [
        CompraGet(
            dt_emissao=row["dt_emissao"], 
            dt_vencimento=row["dt_vencimento"],
            dt_pagamento=row["dt_pagamento"],
            status_pag=row["status_pag"],
            valor=row["valor"],
            loc_entrega=row["loc_entrega"],
            id_pessoa=row["id_pessoa"]
        ) 
        for row in result
    ]

def criar_compra(db: Session, compra: Compra) -> Optional[int]:
    """
    Insere uma nova compra na tabela `compra`.
    Args:
        db (Session): Sessão ativa com o banco de dados.
        compra (Compra): Objeto contendo os dados da compra a ser inserida.
    Returns:
        Optional[int]: ID da compra criada, ou None em caso de falha.
    Raises:
        SQLAlchemyError: Caso ocorra algum erro durante a execução ou commit da transação.
    """    
    # Validação de chaves estrangeiras
    if pessoa_crud.buscar_pessoa(db, compra.id_pessoa) is None: 
        return None
    
    # Preparando a expressão SQL
    param = compra.dict()
    query = text("""
        INSERT INTO compra (dt_emissao, dt_vencimento, dt_pagamento, status_pag, valor, loc_entrega, id_pessoa)
        VALUES (:dt_emissao, :dt_vencimento, :dt_pagamento, :status_pag, :valor, :loc_entrega, :id_pessoa)
        RETURNING id_compra
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

def atualizar_compra(db: Session, compra: Compra, id_compra: int) -> Optional[int]:
    """
    Atualiza os dados de uma compra existente com base no ID informado.
    Args:
        db (Session): Sessão ativa com o banco de dados.
        compra (Compra): Objeto contendo os novos dados da compra.
        id_compra (int): ID da compra a ser atualizada.
    Returns:
        Optional[int]: ID da compra atualizada, ou None em caso de falha.
    Raises:
        SQLAlchemyError: Caso ocorra algum erro durante a execução ou commit da transação.
    """
    # Validação de chaves estrangeiras
    if pessoa_crud.buscar_pessoa(db, compra.id_pessoa) is None: 
        return None
    
    # Preparando a expressão SQL
    param = compra.dict()
    param.update({"id_compra": id_compra})
    query = text("""
        UPDATE compra
        SET 
            dt_emissao=:dt_emissao, dt_vencimento=:dt_vencimento, dt_pagamento=:dt_pagamento, status_pag=:status_pag, valor=:valor, loc_entrega=:loc_entrega, id_pessoa=:id_pessoa
        WHERE id_compra=:id_compra
        RETURNING id_compra
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

def remover_compra(db: Session, id_compra: int) -> Optional[int]:
    """
    Remove uma compra da tabela `compra` com base no ID informado.
    Args:
        db (Session): Sessão ativa com o banco de dados.
        id_compra (int): ID da compra a ser removida.
    Returns:
        Optional[int]: ID da compra removida, ou None caso não exista.
    Raises:
        SQLAlchemyError: Caso ocorra algum erro durante a execução ou commit da transação.
    """
    # Preparando a expressão SQL
    query = text("""
        DELETE FROM compra WHERE id_compra=:id_compra RETURNING id_compra
    """)

    # Protegendo de excessões
    try:
        # Executando a query e salvando o resultado
        result = db.execute(query, {"id_compra": id_compra})
        db.commit()
        return result.scalar()      # Retorna o id em caso de sucesso
    except SQLAlchemyError as e:
        db.rollback()               # Reverte a transação em caso de erro
        raise e

def buscar_compra(db: Session, id_compra: int) -> Optional[CompraGet]:
    """
    Busca uma compra pelo ID na tabela `compra`.
    Args:
        db (Session): Sessão ativa com o banco de dados.
        id_compra (int): ID da compra a ser consultada.
    Returns:
        Optional[CompraGet]: Objeto contendo os dados da compra, ou None se não encontrada.
    """
    # Preparando a expressão SQL
    query = text("""
        SELECT 
            id_compra, dt_emissao, dt_vencimento, dt_pagamento, status_pag, valor, loc_entrega, id_pessoa
        FROM compra
        WHERE id_compra=:id_compra
        LIMIT 1
    """)
    
    # Executando a query e salvando o resultado
    result = db.execute(query, {"id_compra": id_compra}).mappings().fetchone()
    if result is None: return None

    # Retornando CompraGet
    return CompraGet(
        id_compra=result["id_compra"], 
        dt_emissao=result["dt_emissao"], 
        dt_vencimento=result["dt_vencimento"], 
        dt_pagamento=result["dt_pagamento"], 
        status_pag=result["status_pag"], 
        valor=result["valor"], 
        loc_entrega=result["loc_entrega"], 
        id_pessoa=result["id_pessoa"]
    )
