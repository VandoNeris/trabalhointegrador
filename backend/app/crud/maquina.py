from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import text
from typing import Optional, List
from backend.app.schemas.maquina import Maquina, MaquinaGet

async def listar_maquinas(session: AsyncSession) -> List[MaquinaGet]:
    """
    Retorna uma lista de todas as maquinas cadastradas no banco de dados.
    Args:
        session (AsyncSession): Sessão ativa com o banco de dados.
    Returns:
        List[MaquinaGet]: Lista de objetos do tipo MaquinaGet contendo os dados de cada maquina.
    """
    # Preparando a expressão SQL
    query = text("""
        SELECT
            id_maquina, nome, descricao
        FROM maquina
    """)
    
    # Executando a query e salvando o resultado
    result = (await session.execute(query)).mappings().all()
    
    # Retornando lista de MaquinaGet
    return [ MaquinaGet(**row) for row in result ]

async def criar_maquina(session: AsyncSession, maquina: Maquina) -> Optional[int]:
    """
    Insere uma nova maquina na tabela `maquina`.
    Args:
        session (AsyncSession): Sessão ativa com o banco de dados.
        maquina (Maquina): Objeto contendo os dados da maquina a ser inserida.
    Returns:
        Optional[int]: ID da maquina criada, ou None em caso de falha.
    Raises:
        SQLAlchemyError: Caso ocorra algum erro durante a execução ou commit da transação.
    """
    # Preparando a expressão SQL
    param = maquina.model_dump()
    query = text("""
        INSERT INTO maquina (nome, descricao)
        VALUES (:nome, :descricao)
        RETURNING id_maquina
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

async def atualizar_maquina(session: AsyncSession, maquina: Maquina, id_maquina: int) -> Optional[int]:
    """
    Atualiza os dados de uma maquina existente com base no ID informado.
    Args:
        session (AsyncSession): Sessão ativa com o banco de dados.
        maquina (Maquina): Objeto contendo os novos dados da maquina.
        id_maquina (int): ID da maquina a ser atualizada.
    Returns:
        Optional[int]: ID da maquina atualizada, ou None em caso de falha.
    Raises:
        SQLAlchemyError: Caso ocorra algum erro durante a execução ou commit da transação.
    """
    # Preparando a expressão SQL
    param = maquina.model_dump()
    param.update({"id_maquina": id_maquina})
    query = text("""
        UPDATE maquina
        SET 
            nome=:nome, descricao=:descricao
        WHERE id_maquina=:id_maquina
        RETURNING id_maquina
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

async def remover_maquina(session: AsyncSession, id_maquina: int) -> Optional[int]:
    """
    Remove uma maquina da tabela `maquina` com base no ID informado.
    Args:
        session (AsyncSession): Sessão ativa com o banco de dados.
        id_maquina (int): ID da maquina a ser removida.
    Returns:
        Optional[int]: ID da maquina removida, ou None caso não exista.
    Raises:
        SQLAlchemyError: Caso ocorra algum erro durante a execução ou commit da transação.
    """
    # Preparando a expressão SQL
    param = {"id_maquina": id_maquina}
    query = text("""
        DELETE FROM maquina WHERE id_maquina=:id_maquina RETURNING id_maquina
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

async def buscar_maquina(session: AsyncSession, id_maquina: int) -> Optional[MaquinaGet]:
    """
    Busca uma maquina pelo ID na tabela `maquina`.
    Args:
        session (AsyncSession): Sessão ativa com o banco de dados.
        id_maquina (int): ID da maquina a ser consultada.
    Returns:
        Optional[MaquinaGet]: Objeto contendo os dados da maquina, ou None se não encontrada.
    """
    # Preparando a expressão SQL
    param = {"id_maquina": id_maquina}
    query = text("""
        SELECT 
            id_maquina, nome, descricao
        FROM maquina
        WHERE id_maquina=:id_maquina
        LIMIT 1
    """)
    
    # Executando a query e salvando o resultado
    result = (await session.execute(query, param)).mappings().fetchone()

    # Retornando MaquinaGet
    return None if result is None else MaquinaGet(**result)
