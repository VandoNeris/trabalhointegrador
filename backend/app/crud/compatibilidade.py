from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import text
from typing import Optional, List
from backend.app.schemas.compatibilidade import Compatibilidade, CompatibilidadeGet
from backend.app.crud import produtos as produto_crud, maquina as maquina_crud

async def listar_compatibilidades(session: AsyncSession) -> List[CompatibilidadeGet]:
    """
    Retorna uma lista de todas as compatibilidades cadastradas no banco de dados.
    Args:
        session (AsyncSession): Sessão ativa com o banco de dados.
    Returns:
        List[CompatibilidadeGet]: Lista de objetos do tipo CompatibilidadeGet contendo os dados de cada compatibilidade.
    """
    # Preparando a expressão SQL
    query = text("""
        SELECT
            id_compatibilidade, id_produto, id_maquina
        FROM compatibilidade
    """)
    
    # Executando a query e salvando o resultado
    result = (await session.execute(query)).mappings().all()
    if result is None: return list()
    
    # Retornando lista de CompatibilidadeGet
    return [ CompatibilidadeGet(**row) for row in result ]

async def criar_compatibilidade(session: AsyncSession, compatibilidade: Compatibilidade) -> Optional[int]:
    """
    Insere uma nova compatibilidade na tabela `compatibilidade`.
    Args:
        session (AsyncSession): Sessão ativa com o banco de dados.
        compatibilidade (Compatibilidade): Objeto contendo os dados da compatibilidade a ser inserida.
    Returns:
        Optional[int]: ID da compatibilidade criada, ou None em caso de falha.
    Raises:
        SQLAlchemyError: Caso ocorra algum erro durante a execução ou commit da transação.
    """    
    # Validação de chaves estrangeiras
    if produto_crud.buscar_produto(session, compatibilidade.id_produto) is None: 
        return None
    if maquina_crud.buscar_maquina(session, compatibilidade.id_maquina) is None: 
        return None
    
    # Preparando a expressão SQL
    param = compatibilidade.model_dump()
    query = text("""
        INSERT INTO compatibilidade (id_produto, id_maquina)
        VALUES (:id_produto, :id_maquina)
        RETURNING id_compatibilidade
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

async def atualizar_compatibilidade(session: AsyncSession, compatibilidade: Compatibilidade, id_compatibilidade: int) -> Optional[int]:
    """
    Atualiza os dados de uma compatibilidade existente com base no ID informado.
    Args:
        session (AsyncSession): Sessão ativa com o banco de dados.
        compatibilidade (Compatibilidade): Objeto contendo os novos dados da compatibilidade.
        id_compatibilidade (int): ID da compatibilidade a ser atualizada.
    Returns:
        Optional[int]: ID da compatibilidade atualizada, ou None em caso de falha.
    Raises:
        SQLAlchemyError: Caso ocorra algum erro durante a execução ou commit da transação.
    """
    # Validação de chaves estrangeiras
    if produto_crud.buscar_produto(session, compatibilidade.id_produto) is None: 
        return None
    if maquina_crud.buscar_maquina(session, compatibilidade.id_maquina) is None: 
        return None
    
    # Preparando a expressão SQL
    param = compatibilidade.model_dump()
    param.update({"id_compatibilidade": id_compatibilidade})
    query = text("""
        UPDATE compatibilidade
        SET 
            id_produto=:id_produto, id_maquina=:id_maquina
        WHERE id_compatibilidade=:id_compatibilidade
        RETURNING id_compatibilidade
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

async def remover_compatibilidade(session: AsyncSession, id_compatibilidade: int) -> Optional[int]:
    """
    Remove uma compatibilidade da tabela `compatibilidade` com base no ID informado.
    Args:
        session (AsyncSession): Sessão ativa com o banco de dados.
        id_compatibilidade (int): ID da compatibilidade a ser removida.
    Returns:
        Optional[int]: ID da compatibilidade removida, ou None caso não exista.
    Raises:
        SQLAlchemyError: Caso ocorra algum erro durante a execução ou commit da transação.
    """
    # Preparando a expressão SQL
    param = {"id_compatibilidade": id_compatibilidade}
    query = text("""
        DELETE FROM compatibilidade WHERE id_compatibilidade=:id_compatibilidade RETURNING id_compatibilidade
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

async def buscar_compatibilidade(session: AsyncSession, id_compatibilidade: int) -> Optional[CompatibilidadeGet]:
    """
    Busca uma compatibilidade pelo ID na tabela `compatibilidade`.
    Args:
        session (AsyncSession): Sessão ativa com o banco de dados.
        id_compatibilidade (int): ID da compatibilidade a ser consultada.
    Returns:
        Optional[CompatibilidadeGet]: Objeto contendo os dados da compatibilidade, ou None se não encontrada.
    """
    # Preparando a expressão SQL
    param = {"id_compatibilidade": id_compatibilidade}
    query = text("""
        SELECT 
            id_compatibilidade, id_produto, id_maquina
        FROM compatibilidade
        WHERE id_compatibilidade=:id_compatibilidade
        LIMIT 1
    """)
    
    # Executando a query e salvando o resultado
    result = (await session.execute(query, param)).mappings().fetchone()

    # Retornando CompatibilidadeGet
    return None if result is None else CompatibilidadeGet(**result)
