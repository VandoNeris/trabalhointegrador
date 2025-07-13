from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import text
from typing import Optional, List
from backend.app.schemas.ordemservico import OrdemServico, OrdemServicoGet
from backend.app.crud import pessoa as pessoa_crud

async def listar_ordemservicos(session: AsyncSession) -> List[OrdemServicoGet]:
    """
    Retorna uma lista de todas as ordemservicos cadastradas no banco de dados.
    Args:
        session (AsyncSession): Sessão ativa com o banco de dados.
    Returns:
        List[OrdemServicoGet]: Lista de objetos do tipo OrdemServicoGet contendo os dados de cada ordemservico.
    """
    # Preparando a expressão SQL
    query = """
        SELECT
            id_ordem_servico, dt_servico, loc_servico, descricao, id_pessoa
        FROM ordemservico
    """
    
    # Executando a query e salvando o resultado
    result = (await session.execute(text(query))).mappings().all()
    if result is None: return list()
        
    # Retornando lista de OrdemServicoGet
    return [ OrdemServicoGet(**row) for row in result ]

async def criar_ordemservico(session: AsyncSession, ordemservico: OrdemServico) -> Optional[int]:
    """
    Insere uma nova ordemservico na tabela `ordemservico`.
    Args:
        session (AsyncSession): Sessão ativa com o banco de dados.
        ordemservico (OrdemServico): Objeto contendo os dados da ordemservico a ser inserida.
    Returns:
        Optional[int]: ID da ordemservico criada, ou None em caso de falha.
    Raises:
        SQLAlchemyError: Caso ocorra algum erro durante a execução ou commit da transação.
    """    
    # Validação de chaves estrangeiras
    if pessoa_crud.buscar_pessoa(session, ordemservico.id_pessoa) is None: 
        return None
    
    # Preparando a expressão SQL
    param = ordemservico.model_dump()
    query = """
        INSERT INTO ordemservico (dt_servico, loc_servico, descricao, id_pessoa)
        VALUES (:dt_servico, :loc_servico, :descricao, :id_pessoa)
        RETURNING id_ordem_servico
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

async def atualizar_ordemservico(session: AsyncSession, ordemservico: OrdemServico, id_ordem_servico: int) -> Optional[int]:
    """
    Atualiza os dados de uma ordemservico existente com base no ID informado.
    Args:
        session (AsyncSession): Sessão ativa com o banco de dados.
        ordemservico (OrdemServico): Objeto contendo os novos dados da ordemservico.
        id_ordem_servico (int): ID da ordemservico a ser atualizada.
    Returns:
        Optional[int]: ID da ordemservico atualizada, ou None em caso de falha.
    Raises:
        SQLAlchemyError: Caso ocorra algum erro durante a execução ou commit da transação.
    """
    # Validação de chaves estrangeiras
    if pessoa_crud.buscar_pessoa(session, ordemservico.id_pessoa) is None: 
        return None
    
    # Preparando a expressão SQL
    param = ordemservico.model_dump()
    param.update({"id_ordem_servico": id_ordem_servico})
    query = """
        UPDATE ordemservico
        SET 
            dt_servico=:dt_servico, loc_servico=:loc_servico, descricao=:descricao, id_pessoa=:id_pessoa
        WHERE id_ordem_servico=:id_ordem_servico
        RETURNING id_ordem_servico
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

async def remover_ordemservico(session: AsyncSession, id_ordem_servico: int) -> Optional[int]:
    """
    Remove uma ordemservico da tabela `ordemservico` com base no ID informado.
    Args:
        session (AsyncSession): Sessão ativa com o banco de dados.
        id_ordem_servico (int): ID da ordemservico a ser removida.
    Returns:
        Optional[int]: ID da ordemservico removida, ou None caso não exista.
    Raises:
        SQLAlchemyError: Caso ocorra algum erro durante a execução ou commit da transação.
    """
    # Preparando a expressão SQL
    param = {"id_ordem_servico": id_ordem_servico}
    query = """
        DELETE FROM ordemservico WHERE id_ordem_servico=:id_ordem_servico RETURNING id_ordem_servico
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

async def buscar_ordemservico(session: AsyncSession, id_ordem_servico: int) -> Optional[OrdemServicoGet]:
    """
    Busca uma ordemservico pelo ID na tabela `ordemservico`.
    Args:
        session (AsyncSession): Sessão ativa com o banco de dados.
        id_ordem_servico (int): ID da ordemservico a ser consultada.
    Returns:
        Optional[OrdemServicoGet]: Objeto contendo os dados da ordemservico, ou None se não encontrada.
    """
    # Preparando a expressão SQL
    param = {"id_ordem_servico": id_ordem_servico}
    query = """
        SELECT 
            id_ordem_servico, dt_servico, loc_servico, descricao, id_pessoa
        FROM ordemservico
        WHERE id_ordem_servico=:id_ordem_servico
        LIMIT 1
    """
    
    # Executando a query e salvando o resultado
    result = (await session.execute(text(query), param)).mappings().fetchone()

    # Retornando OrdemServicoGet
    return None if result is None else OrdemServicoGet(**result)
