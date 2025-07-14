from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import text
from typing import Optional, List
from backend.app.schemas.compra import Compra, CompraGet
from backend.app.crud import pessoa as pessoa_crud

async def listar_compras(session: AsyncSession) -> List[CompraGet]:
    """
    Retorna uma lista de todas as compras cadastradas no banco de dados.
    Args:
        session (AsyncSession): Sessão ativa com o banco de dados.
    Returns:
        List[CompraGet]: Lista de objetos do tipo CompraGet contendo os dados de cada compra.
    """
    # Preparando a expressão SQL
    query = """
        SELECT
            compra.id_compra, 
            compra.loc_entrega, 
            compra.valor, 
            compra.dt_emissao, 
            compra.dt_vencimento, 
            compra.dt_entrega, 
            compra.dt_pagamento, 
            compra.id_pessoa,
            pessoa.nome
        FROM compra
        JOIN pessoa ON pessoa.id_pessoa = compra.id_pessoa
    """
    
    # Executando a query e salvando o resultado
    result = (await session.execute(text(query))).mappings().all()
    if result is None: return list()
    
    # Retornando lista de CompraGet
    return [ CompraGet(**row) for row in result ]

async def criar_compra(session: AsyncSession, compra: Compra) -> Optional[int]:
    """
    Insere uma nova compra na tabela `compra`.
    Args:
        session (AsyncSession): Sessão ativa com o banco de dados.
        compra (Compra): Objeto contendo os dados da compra a ser inserida.
    Returns:
        Optional[int]: ID da compra criada, ou None em caso de falha.
    Raises:
        SQLAlchemyError: Caso ocorra algum erro durante a execução ou commit da transação.
    """    
    # Validação de chaves estrangeiras
    if pessoa_crud.buscar_pessoa(session, compra.id_pessoa) is None: 
        return None
    
    # Preparando a expressão SQL
    param = compra.model_dump()
    query = """
        INSERT INTO compra (loc_entrega, valor, dt_emissao, dt_vencimento, dt_entrega, dt_pagamento, id_pessoa)
        VALUES (:loc_entrega, :valor, :dt_emissao, :dt_vencimento, :dt_entrega, :dt_pagamento, :id_pessoa)
        RETURNING id_compra
    """

    # Protegendo de excessões
    try:
        # Executando a query e salvando o resultado
        result = (await session.execute(text(query), param))
        await session.commit()
        return result.scalar()      # Retorna o id em caso de sucesso
    except SQLAlchemyError as e:
        await session.rollback()               # Reverte a transação em caso de erro
        raise e

async def atualizar_compra(session: AsyncSession, compra: Compra, id_compra: int) -> Optional[int]:
    """
    Atualiza os dados de uma compra existente com base no ID informado.
    Args:
        session (AsyncSession): Sessão ativa com o banco de dados.
        compra (Compra): Objeto contendo os novos dados da compra.
        id_compra (int): ID da compra a ser atualizada.
    Returns:
        Optional[int]: ID da compra atualizada, ou None em caso de falha.
    Raises:
        SQLAlchemyError: Caso ocorra algum erro durante a execução ou commit da transação.
    """
    # Validação de chaves estrangeiras
    if pessoa_crud.buscar_pessoa(session, compra.id_pessoa) is None: 
        return None
    
    # Preparando a expressão SQL
    param = compra.model_dump()
    param.update({"id_compra": id_compra})
    query = """
        UPDATE compra
        SET 
            loc_entrega=:loc_entrega, valor=:valor, dt_emissao=:dt_emissao, dt_vencimento=:dt_vencimento, dt_entrega=:dt_entrega, dt_pagamento=:dt_pagamento, id_pessoa=:id_pessoa
        WHERE id_compra=:id_compra
        RETURNING id_compra
    """

    # Protegendo de excessões
    try:
        # Executando a query e salvando o resultado
        result = (await session.execute(text(query), param))
        await session.commit()
        return result.scalar()      # Retorna o id em caso de sucesso
    except SQLAlchemyError as e:
        await session.rollback()               # Reverte a transação em caso de erro
        raise e

async def remover_compra(session: AsyncSession, id_compra: int) -> Optional[int]:
    """
    Remove uma compra da tabela `compra` com base no ID informado.
    Args:
        session (AsyncSession): Sessão ativa com o banco de dados.
        id_compra (int): ID da compra a ser removida.
    Returns:
        Optional[int]: ID da compra removida, ou None caso não exista.
    Raises:
        SQLAlchemyError: Caso ocorra algum erro durante a execução ou commit da transação.
    """
    # Preparando a expressão SQL
    param = {"id_compra": id_compra}
    query = """
        DELETE FROM compra WHERE id_compra=:id_compra RETURNING id_compra
    """

    # Protegendo de excessões
    try:
        # Executando a query e salvando o resultado
        result = (await session.execute(text(query), param))
        await session.commit()
        return result.scalar()      # Retorna o id em caso de sucesso
    except SQLAlchemyError as e:
        await session.rollback()               # Reverte a transação em caso de erro
        raise e

async def buscar_compra(session: AsyncSession, id_compra: int) -> Optional[CompraGet]:
    """
    Busca uma compra pelo ID na tabela `compra`.
    Args:
        session (AsyncSession): Sessão ativa com o banco de dados.
        id_compra (int): ID da compra a ser consultada.
    Returns:
        Optional[CompraGet]: Objeto contendo os dados da compra, ou None se não encontrada.
    """
    # Preparando a expressão SQL
    param = {"id_compra": id_compra}
    query = """
        SELECT
            compra.id_compra, 
            compra.loc_entrega, 
            compra.valor, 
            compra.dt_emissao, 
            compra.dt_vencimento, 
            compra.dt_entrega, 
            compra.dt_pagamento, 
            compra.id_pessoa,
            pessoa.nome
        FROM compra
        JOIN pessoa ON pessoa.id_pessoa = compra.id_pessoa
        WHERE compra.id_compra=:id_compra
        LIMIT 1
    """
    
    # Executando a query e salvando o resultado
    result = (await session.execute(text(query), param)).mappings().fetchone()

    # Retornando CompraGet
    return None if result is None else CompraGet(**result)
