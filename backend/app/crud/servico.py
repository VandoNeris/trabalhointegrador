from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import text
from typing import Optional, List
from backend.app.schemas.servico import Servico, ServicoGet
from backend.app.crud import ordemservico as ordemservico_crud

async def listar_servicos(session: AsyncSession) -> List[ServicoGet]:
    """
    Retorna uma lista de todas as servicos cadastradas no banco de dados.
    Args:
        session (AsyncSession): Sessão ativa com o banco de dados.
    Returns:
        List[ServicoGet]: Lista de objetos do tipo ServicoGet contendo os dados de cada servico.
    """
    # Preparando a expressão SQL
    query = text("""
        SELECT
            id_servico, id_ordem_servico, valor, dt_emissao, dt_vencimento, quilometros, horas, dt_pagamento, descricao
        FROM servico
    """)
    
    # Executando a query e salvando o resultado
    result = (await session.execute(query)).mappings().all()
    if result is None: return list()
    
    # Retornando lista de ServicoGet
    return [ ServicoGet(**row) for row in result ]

async def criar_servico(session: AsyncSession, servico: Servico) -> Optional[int]:
    """
    Insere uma nova servico na tabela `servico`.
    Args:
        session (AsyncSession): Sessão ativa com o banco de dados.
        servico (Servico): Objeto contendo os dados da servico a ser inserida.
    Returns:
        Optional[int]: ID da servico criada, ou None em caso de falha.
    Raises:
        SQLAlchemyError: Caso ocorra algum erro durante a execução ou commit da transação.
    """    
    # Validação de chaves estrangeiras
    if ordemservico_crud.buscar_ordemservico(session, servico.id_ordem_servico) is None: 
        return None
    
    # Preparando a expressão SQL
    param = servico.dict()
    query = text("""
        INSERT INTO servico (id_ordem_servico, valor, dt_emissao, dt_vencimento, quilometros, horas, dt_pagamento, descricao)
        VALUES (:id_ordem_servico, :valor, :dt_emissao, :dt_vencimento, :quilometros, :horas, :dt_pagamento, :descricao)
        RETURNING id_servico
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

async def atualizar_servico(session: AsyncSession, servico: Servico, id_servico: int) -> Optional[int]:
    """
    Atualiza os dados de uma servico existente com base no ID informado.
    Args:
        session (AsyncSession): Sessão ativa com o banco de dados.
        servico (Servico): Objeto contendo os novos dados da servico.
        id_servico (int): ID da servico a ser atualizada.
    Returns:
        Optional[int]: ID da servico atualizada, ou None em caso de falha.
    Raises:
        SQLAlchemyError: Caso ocorra algum erro durante a execução ou commit da transação.
    """
    # Validação de chaves estrangeiras
    if ordemservico_crud.buscar_ordemservico(session, servico.id_ordem_servico) is None: 
        return None
    
    # Preparando a expressão SQL
    param = servico.dict()
    param.update({"id_servico": id_servico})
    query = text("""
        UPDATE servico
        SET 
            id_ordem_servico=:id_ordem_servico, valor=:valor, dt_emissao=:dt_emissao, dt_vencimento=:dt_vencimento, quilometros=:quilometros, horas=:horas, dt_pagamento=:dt_pagamento, descricao=:descricao
        WHERE id_servico=:id_servico
        RETURNING id_servico
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

async def remover_servico(session: AsyncSession, id_servico: int) -> Optional[int]:
    """
    Remove uma servico da tabela `servico` com base no ID informado.
    Args:
        session (AsyncSession): Sessão ativa com o banco de dados.
        id_servico (int): ID da servico a ser removida.
    Returns:
        Optional[int]: ID da servico removida, ou None caso não exista.
    Raises:
        SQLAlchemyError: Caso ocorra algum erro durante a execução ou commit da transação.
    """
    # Preparando a expressão SQL
    query = text("""
        DELETE FROM servico WHERE id_servico=:id_servico RETURNING id_servico
    """)

    # Protegendo de excessões
    try:
        # Executando a query e salvando o resultado
        result = (await session.execute(query, {"id_servico": id_servico}))
        await session.commit()
        return result.scalar()      # Retorna o id em caso de sucesso
    except SQLAlchemyError as e:
        await session.rollback()    # Reverte a transação em caso de erro
        raise e

async def buscar_servico(session: AsyncSession, id_servico: int) -> Optional[ServicoGet]:
    """
    Busca uma servico pelo ID na tabela `servico`.
    Args:
        session (AsyncSession): Sessão ativa com o banco de dados.
        id_servico (int): ID da servico a ser consultada.
    Returns:
        Optional[ServicoGet]: Objeto contendo os dados da servico, ou None se não encontrada.
    """
    # Preparando a expressão SQL
    query = text("""
        SELECT 
            id_servico, id_ordem_servico, valor, dt_emissao, dt_vencimento, quilometros, horas, dt_pagamento, descricao
        FROM servico
        WHERE id_servico=:id_servico
        LIMIT 1
    """)
    
    # Executando a query e salvando o resultado
    result = (await session.execute(query, {"id_servico": id_servico})).mappings().fetchone()

    # Retornando ServicoGet
    return None if result is None else ServicoGet(**result)
