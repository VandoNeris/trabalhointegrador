from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import text
from typing import Optional, List
from backend.app.crud import maquina as maquina_crud

async def listar_maquinas(session: AsyncSession) -> List[maquina_crud.MaquinaGet]:
    """
    Retorna uma lista de todas as máquinas cadastradas no banco de dados.
    Args:
        session (AsyncSession): Sessão ativa com o banco de dados.
    Returns:
        List[MaquinaGet]: Lista de objetos do tipo MaquinaGet contendo os dados de cada máquina.
    """
    # Preparando a expressão SQL
    query = text("""
        SELECT id_maquina, nome, descricao
        FROM maquina
    """)
    
    # Executando a query e salvando o resultado
    result = (await session.execute(query)).mappings().all()
    
    # Retornando lista de MaquinaGet
    return [ maquina_crud.MaquinaGet(**row) for row in result ]

async def criar_maquina(session: AsyncSession, maquina: maquina_crud.Maquina) -> Optional[int]:
    """
    Insere uma nova máquina na tabela `maquina`.
    Args:
        session (AsyncSession): Sessão ativa com o banco de dados.
        maquina (Maquina): Objeto contendo os dados da máquina a ser inserida.
    Returns:
        Optional[int]: ID da máquina criada, ou None em caso de falha.
    Raises:
        SQLAlchemyError: Caso ocorra algum erro durante a execução ou commit da transação.
    """
    # Preparando a expressão SQL
    param = maquina.dict()
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
        await session.rollback()    # Reverte a transação em caso de erro
        raise e