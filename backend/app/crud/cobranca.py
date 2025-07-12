from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import text
from typing import Optional, List
from backend.app.crud import cobranca as cobranca_crud

async def listar_cobrancas(session: AsyncSession) -> List[cobranca_crud.CobrancaGet]:
    """
    Retorna uma lista de todas as cobranças cadastradas no banco de dados.
    Args:
        session (AsyncSession): Sessão ativa com o banco de dados.
    Returns:
        List[CobrancaGet]: Lista de objetos do tipo CobrancaGet contendo os dados de cada cobrança.
    """
    # Preparando a expressão SQL
    query = text("""
        SELECT
            id_cobranca, dt_emissao, dt_vencimento, dt_pagamento, statuspag, valor
        FROM cobranca
    """)
    
    # Executando a query e salvando o resultado
    result = (await session.execute(query)).mappings().all()
    
    # Retornando lista de CobrancaGet
    return [ cobranca_crud.CobrancaGet(**row) for row in result ]

async def criar_cobranca(session: AsyncSession, cobranca: cobranca_crud.Cobranca) -> Optional[int]:
    """
    Insere uma nova cobrança na tabela `cobranca`.
    Args:
        session (AsyncSession): Sessão ativa com o banco de dados.
        cobranca (Cobranca): Objeto contendo os dados da cobrança a ser inserida.
    Returns:
        Optional[int]: ID da cobrança criada, ou None em caso de falha.
    Raises:
        SQLAlchemyError: Caso ocorra algum erro durante a execução ou commit da transação.
    """
    # Preparando a expressão SQL
    param = cobranca.dict()
    query = text("""
        INSERT INTO cobranca (dt_emissao, dt_vencimento, dt_pagamento, statuspag, valor)
        VALUES (:dt_emissao, :dt_vencimento, :dt_pagamento, :statuspag, :valor)
        RETURNING id_cobranca
    """)

    # Protegendo de excessões
    try:
        # Executando a query e salvando o resultado
        result = (await session.execute(query, param))
        await session.commit()
        return result.scalar()      # Retorna o id em caso de sucesso
    except SQLAlchemyError as e:
        await session.rollback()    # Reverte a transação em caso de erro
        raise e
    
async def atualizar_cobranca(session: AsyncSession, cobranca: cobranca_crud.Cobranca, id_cobranca: int) -> Optional[int]:
    """
    Atualiza os dados de uma cobrança existente com base no ID informado.
    Args:
        session (AsyncSession): Sessão ativa com o banco de dados.
        cobranca (Cobranca): Objeto contendo os novos dados da cobrança.
        id_cobranca (int): ID da cobrança a ser atualizada.
    Returns:
        Optional[int]: ID da cobrança atualizada, ou None em caso de falha.
    Raises:
        SQLAlchemyError: Caso ocorra algum erro durante a execução ou commit da transação.
    """
    # Preparando a expressão SQL
    param = cobranca.dict()
    param['id_cobranca'] = id_cobranca
    query = text("""
        UPDATE cobranca
        SET dt_emissao = :dt_emissao,
            dt_vencimento = :dt_vencimento,
            dt_pagamento = :dt_pagamento,
            statuspag = :statuspag,
            valor = :valor
        WHERE id_cobranca = :id_cobranca
        RETURNING id_cobranca
    """)

    # Protegendo de excessões
    try:
        # Executando a query e salvando o resultado
        result = (await session.execute(query, param))
        await session.commit()
        return result.scalar()      # Retorna o id em caso de sucesso
    except SQLAlchemyError as e:
        await session.rollback()    # Reverte a transação em caso de erro
        raise e
    
async def remover_cobranca(session: AsyncSession, id_cobranca: int) -> Optional[int]:
    """
    Remove uma cobrança existente com base no ID informado.
    Args:
        session (AsyncSession): Sessão ativa com o banco de dados.
        id_cobranca (int): ID da cobrança a ser removida.
    Returns:
        Optional[int]: ID da cobrança removida, ou None em caso de falha.
    Raises:
        SQLAlchemyError: Caso ocorra algum erro durante a execução ou commit da transação.
    """
    # Preparando a expressão SQL
    query = text("""
        DELETE FROM cobranca
        WHERE id_cobranca = :id_cobranca
        RETURNING id_cobranca
    """)

    # Protegendo de excessões
    try:
        # Executando a query e salvando o resultado
        result = (await session.execute(query, {"id_cobranca": id_cobranca}))
        await session.commit()
        return result.scalar()      # Retorna o id em caso de sucesso
    except SQLAlchemyError as e:
        await session.rollback()    # Reverte a transação em caso de erro
        raise e
    
async def buscar_cobranca(session: AsyncSession, id_cobranca: int) -> Optional[cobranca_crud.CobrancaGet]:
    """
    Busca uma cobrança pelo ID informado.
    Args:
        session (AsyncSession): Sessão ativa com o banco de dados.
        id_cobranca (int): ID da cobrança a ser buscada.
    Returns:
        Optional[CobrancaGet]: Objeto do tipo CobrancaGet contendo os dados da cobrança, ou None se não encontrada.
    Raises:
        SQLAlchemyError: Caso ocorra algum erro durante a execução da query.
    """
    # Preparando a expressão SQL
    query = text("""
        SELECT id_cobranca, dt_emissao, dt_vencimento, dt_pagamento, statuspag, valor
        FROM cobranca
        WHERE id_cobranca = :id_cobranca
    """)

    # Executando a query e salvando o resultado
    result = (await session.execute(query, {"id_cobranca": id_cobranca})).mappings().first()
    
    # Retornando o objeto CobrancaGet ou None se não encontrado
    return cobranca_crud.CobrancaGet(**result) if result else None
    