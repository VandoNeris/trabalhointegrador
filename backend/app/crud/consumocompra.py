from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import text
from typing import Optional, List
from backend.app.schemas.consumocompra import ConsumoCompra, ConsumoCompraGet
from backend.app.crud import produtos as produto_crud, compra as compra_crud

async def listar_consumocompras(session: AsyncSession) -> List[ConsumoCompraGet]:
    """
    Retorna uma lista de todas as consumocompras cadastradas no banco de dados.
    Args:
        session (AsyncSession): Sessão ativa com o banco de dados.
    Returns:
        List[ConsumoCompraGet]: Lista de objetos do tipo ConsumoCompraGet contendo os dados de cada consumocompra.
    """
    # Preparando a expressão SQL
    query = text("""
        SELECT
            id_consumo_compra, quantidade, id_produto, id_compra
        FROM consumocompra
    """)
    
    # Executando a query e salvando o resultado
    result = (await session.execute(query)).mappings().all()
    if result is None: return list()
    
    # Retornando lista de ConsumoCompraGet
    return [ ConsumoCompraGet(**row) for row in result ]

async def criar_consumocompra(session: AsyncSession, consumocompra: ConsumoCompra) -> Optional[int]:
    """
    Insere uma nova consumocompra na tabela `consumocompra`.
    Args:
        session (AsyncSession): Sessão ativa com o banco de dados.
        consumocompra (ConsumoCompra): Objeto contendo os dados da consumocompra a ser inserida.
    Returns:
        Optional[int]: ID da consumocompra criada, ou None em caso de falha.
    Raises:
        SQLAlchemyError: Caso ocorra algum erro durante a execução ou commit da transação.
    """    
    # Validação de chaves estrangeiras
    if produto_crud.buscar_produto(session, consumocompra.id_produto) is None: 
        return None
    if compra_crud.buscar_compra(session, consumocompra.id_compra) is None: 
        return None
    
    # Preparando a expressão SQL
    param = consumocompra.model_dump()
    query = text("""
        INSERT INTO consumocompra (quantidade, id_produto, id_compra)
        VALUES (:quantidade, :id_produto, :id_compra)
        RETURNING id_consumo_compra
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

async def atualizar_consumocompra(session: AsyncSession, consumocompra: ConsumoCompra, id_consumo_compra: int) -> Optional[int]:
    """
    Atualiza os dados de uma consumocompra existente com base no ID informado.
    Args:
        session (AsyncSession): Sessão ativa com o banco de dados.
        consumocompra (ConsumoCompra): Objeto contendo os novos dados da consumocompra.
        id_consumo_compra (int): ID da consumocompra a ser atualizada.
    Returns:
        Optional[int]: ID da consumocompra atualizada, ou None em caso de falha.
    Raises:
        SQLAlchemyError: Caso ocorra algum erro durante a execução ou commit da transação.
    """
    # Validação de chaves estrangeiras
    if produto_crud.buscar_produto(session, consumocompra.id_produto) is None: 
        return None
    if compra_crud.buscar_compra(session, consumocompra.id_compra) is None: 
        return None
    
    # Preparando a expressão SQL
    param = consumocompra.model_dump()
    param.update({"id_consumo_compra": id_consumo_compra})
    query = text("""
        UPDATE consumocompra
        SET 
            quantidade=:quantidade, id_produto=:id_produto, id_compra=:id_compra
        WHERE id_consumo_compra=:id_consumo_compra
        RETURNING id_consumo_compra
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

async def remover_consumocompra(session: AsyncSession, id_consumo_compra: int) -> Optional[int]:
    """
    Remove uma consumocompra da tabela `consumocompra` com base no ID informado.
    Args:
        session (AsyncSession): Sessão ativa com o banco de dados.
        id_consumo_compra (int): ID da consumocompra a ser removida.
    Returns:
        Optional[int]: ID da consumocompra removida, ou None caso não exista.
    Raises:
        SQLAlchemyError: Caso ocorra algum erro durante a execução ou commit da transação.
    """
    # Preparando a expressão SQL
    param = {"id_consumo_compra": id_consumo_compra}
    query = text("""
        DELETE FROM consumocompra WHERE id_consumo_compra=:id_consumo_compra RETURNING id_consumo_compra
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

async def buscar_consumocompra(session: AsyncSession, id_consumo_compra: int) -> Optional[ConsumoCompraGet]:
    """
    Busca uma consumocompra pelo ID na tabela `consumocompra`.
    Args:
        session (AsyncSession): Sessão ativa com o banco de dados.
        id_consumo_compra (int): ID da consumocompra a ser consultada.
    Returns:
        Optional[ConsumoCompraGet]: Objeto contendo os dados da consumocompra, ou None se não encontrada.
    """
    # Preparando a expressão SQL
    param = {"id_consumo_compra": id_consumo_compra}
    query = text("""
        SELECT 
            id_consumo_compra, quantidade, id_produto, id_compra
        FROM consumocompra
        WHERE id_consumo_compra=:id_consumo_compra
        LIMIT 1
    """)
    
    # Executando a query e salvando o resultado
    result = (await session.execute(query, param)).mappings().fetchone()

    # Retornando ConsumoCompraGet
    return None if result is None else ConsumoCompraGet(**result)
