from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import text
from typing import Optional, List
from backend.app.schemas.consumoservico import ConsumoServico, ConsumoServicoGet
from backend.app.crud import produtos as produto_crud, servico as servico_crud

async def listar_consumoservicos(session: AsyncSession) -> List[ConsumoServicoGet]:
    """
    Retorna uma lista de todas as consumoservicos cadastradas no banco de dados.
    Args:
        session (AsyncSession): Sessão ativa com o banco de dados.
    Returns:
        List[ConsumoServicoGet]: Lista de objetos do tipo ConsumoServicoGet contendo os dados de cada consumoservico.
    """
    # Preparando a expressão SQL
    query = text("""
        SELECT
            id_consumo_servico, quantidade, id_produto, id_servico
        FROM consumoservico
    """)
    
    # Executando a query e salvando o resultado
    result = (await session.execute(query)).mappings().all()
    if result is None: return list()
    
    # Retornando lista de ConsumoServicoGet
    return [ ConsumoServicoGet(**row) for row in result ]

async def criar_consumoservico(session: AsyncSession, consumoservico: ConsumoServico) -> Optional[int]:
    """
    Insere uma nova consumoservico na tabela `consumoservico`.
    Args:
        session (AsyncSession): Sessão ativa com o banco de dados.
        consumoservico (ConsumoServico): Objeto contendo os dados da consumoservico a ser inserida.
    Returns:
        Optional[int]: ID da consumoservico criada, ou None em caso de falha.
    Raises:
        SQLAlchemyError: Caso ocorra algum erro durante a execução ou commit da transação.
    """    
    # Validação de chaves estrangeiras
    if produto_crud.buscar_produto(session, consumoservico.id_produto) is None: 
        return None
    if servico_crud.buscar_servico(session, consumoservico.id_servico) is None: 
        return None
    
    # Preparando a expressão SQL
    param = consumoservico.dict()
    query = text("""
        INSERT INTO consumoservico (quantidade, id_produto, id_servico)
        VALUES (:quantidade, :id_produto, :id_servico)
        RETURNING id_consumo_servico
    """)

    # Protegendo de excessões
    try:
        # Executando a query e salvando o resultado
        result = (await session.execute(query, param))
        await session.commit()
        return result.scalar()      # Retorna o id em caso de sucesso
    except SQLAlchemyError as e:
        await session.rollback()               # Reverte a transação em caso de erro
        raise e

async def atualizar_consumoservico(session: AsyncSession, consumoservico: ConsumoServico, id_consumo_servico: int) -> Optional[int]:
    """
    Atualiza os dados de uma consumoservico existente com base no ID informado.
    Args:
        session (AsyncSession): Sessão ativa com o banco de dados.
        consumoservico (ConsumoServico): Objeto contendo os novos dados da consumoservico.
        id_consumo_servico (int): ID da consumoservico a ser atualizada.
    Returns:
        Optional[int]: ID da consumoservico atualizada, ou None em caso de falha.
    Raises:
        SQLAlchemyError: Caso ocorra algum erro durante a execução ou commit da transação.
    """
    # Validação de chaves estrangeiras
    if produto_crud.buscar_produto(session, consumoservico.id_produto) is None: 
        return None
    if servico_crud.buscar_servico(session, consumoservico.id_servico) is None: 
        return None
    
    # Preparando a expressão SQL
    param = consumoservico.dict()
    param.update({"id_consumo_servico": id_consumo_servico})
    query = text("""
        UPDATE consumoservico
        SET 
            quantidade=:quantidade, id_produto=:id_produto, id_servico=:id_servico
        WHERE id_consumo_servico=:id_consumo_servico
        RETURNING id_consumo_servico
    """)

    # Protegendo de excessões
    try:
        # Executando a query e salvando o resultado
        result = (await session.execute(query, param))
        await session.commit()
        return result.scalar()      # Retorna o id em caso de sucesso
    except SQLAlchemyError as e:
        await session.rollback()               # Reverte a transação em caso de erro
        raise e

async def remover_consumoservico(session: AsyncSession, id_consumo_servico: int) -> Optional[int]:
    """
    Remove uma consumoservico da tabela `consumoservico` com base no ID informado.
    Args:
        session (AsyncSession): Sessão ativa com o banco de dados.
        id_consumo_servico (int): ID da consumoservico a ser removida.
    Returns:
        Optional[int]: ID da consumoservico removida, ou None caso não exista.
    Raises:
        SQLAlchemyError: Caso ocorra algum erro durante a execução ou commit da transação.
    """
    # Preparando a expressão SQL
    query = text("""
        DELETE FROM consumoservico WHERE id_consumo_servico=:id_consumo_servico RETURNING id_consumo_servico
    """)

    # Protegendo de excessões
    try:
        # Executando a query e salvando o resultado
        result = (await session.execute(query, {"id_consumo_servico": id_consumo_servico}))
        await session.commit()
        return result.scalar()      # Retorna o id em caso de sucesso
    except SQLAlchemyError as e:
        await session.rollback()               # Reverte a transação em caso de erro
        raise e

async def buscar_consumoservico(session: AsyncSession, id_consumo_servico: int) -> Optional[ConsumoServicoGet]:
    """
    Busca uma consumoservico pelo ID na tabela `consumoservico`.
    Args:
        session (AsyncSession): Sessão ativa com o banco de dados.
        id_consumo_servico (int): ID da consumoservico a ser consultada.
    Returns:
        Optional[ConsumoServicoGet]: Objeto contendo os dados da consumoservico, ou None se não encontrada.
    """
    # Preparando a expressão SQL
    query = text("""
        SELECT 
            id_consumo_servico, quantidade, id_produto, id_servico
        FROM consumoservico
        WHERE id_consumo_servico=:id_consumo_servico
        LIMIT 1
    """)
    
    # Executando a query e salvando o resultado
    result = (await session.execute(query, {"id_consumo_servico": id_consumo_servico})).mappings().fetchone()

    # Retornando ConsumoServicoGet
    return None if result is None else ConsumoServicoGet(**result)
