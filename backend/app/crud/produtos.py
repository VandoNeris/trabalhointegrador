from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import text
from typing import Optional, List
from backend.app.schemas.produtos import Produto, ProdutoGet

async def listar_produtos(session: AsyncSession) -> List[ProdutoGet]:
    """
    Retorna uma lista de todas as produtos cadastradas no banco de dados.
    Args:
        session (AsyncSession): Sessão ativa com o banco de dados.
    Returns:
        List[ProdutoGet]: Lista de objetos do tipo ProdutoGet contendo os dados de cada produto.
    """
    # Preparando a expressão SQL
    query = """
        SELECT
            id_produto, nome, quantidade, valor_uni, descricao, categoria, marca
        FROM produtos 
    """
    
    # Executando a query e salvando o resultado
    result = (await session.execute(text(query))).mappings().all()
    
    # Retornando lista de ProdutoGet
    return [ ProdutoGet(**row) for row in result ]

async def criar_produto(session: AsyncSession, produto: Produto) -> Optional[int]:
    """
    Insere uma nova produto na tabela `produto`.
    Args:
        session (AsyncSession): Sessão ativa com o banco de dados.
        produto (Produto): Objeto contendo os dados da produto a ser inserida.
    Returns:
        Optional[int]: ID da produto criada, ou None em caso de falha.
    Raises:
        SQLAlchemyError: Caso ocorra algum erro durante a execução ou commit da transação.
    """
    # Preparando a expressão SQL
    param = produto.model_dump()
    query = """
        INSERT INTO produto (nome, quantidade, valor_uni, descricao, categoria, marca)
        VALUES (:nome, :quantidade, :valor_uni, :descricao, :categoria, :marca)
        RETURNING id_produto
    """

    # Protegendo de excessões
    try:
        # Executando a query e salvando o resultado
        result = (await session.execute(text(query), param))
        await session.commit()
        return result.scalar()      # Retorna o id em caso de sucesso
    except SQLAlchemyError as e:
        await session.rollback()    # Reverte a transação em caso de erro
        raise e

async def atualizar_produto(session: AsyncSession, produto: Produto, id_produto: int) -> Optional[int]:
    """
    Atualiza os dados de uma produto existente com base no ID informado.
    Args:
        session (AsyncSession): Sessão ativa com o banco de dados.
        produto (Produto): Objeto contendo os novos dados da produto.
        id_produto (int): ID da produto a ser atualizada.
    Returns:
        Optional[int]: ID da produto atualizada, ou None em caso de falha.
    Raises:
        SQLAlchemyError: Caso ocorra algum erro durante a execução ou commit da transação.
    """
    # Preparando a expressão SQL
    param = produto.model_dump()
    param.update({"id_produto": id_produto})
    query = """
        UPDATE produto
        SET 
            nome=:nome, quantidade=:quantidade, valor_uni=:valor_uni, descricao=:descricao, categoria=:categoria, marca=:marca
        WHERE id_produto=:id_produto
        RETURNING id_produto
    """

    # Protegendo de excessões
    try:
        # Executando a query e salvando o resultado
        result = (await session.execute(text(query), param))
        await session.commit()
        return result.scalar()      # Retorna o id em caso de sucesso
    except SQLAlchemyError as e:
        await session.rollback()    # Reverte a transação em caso de erro
        raise e

async def remover_produto(session: AsyncSession, id_produto: int) -> Optional[int]:
    """
    Remove uma produto da tabela `produto` com base no ID informado.
    Args:
        session (AsyncSession): Sessão ativa com o banco de dados.
        id_produto (int): ID da produto a ser removida.
    Returns:
        Optional[int]: ID da produto removida, ou None caso não exista.
    Raises:
        SQLAlchemyError: Caso ocorra algum erro durante a execução ou commit da transação.
    """
    # Preparando a expressão SQL
    param = {"id_produto": id_produto}
    query = """
        DELETE FROM produtos WHERE id_produto=:id_produto RETURNING id_produto
    """

    # Protegendo de excessões
    try:
        # Executando a query e salvando o resultado
        result = (await session.execute(text(query), param))
        await session.commit()
        return result.scalar()      # Retorna o id em caso de sucesso
    except SQLAlchemyError as e:
        await session.rollback()    # Reverte a transação em caso de erro
        raise e

async def buscar_produto(session: AsyncSession, id_produto: int) -> Optional[ProdutoGet]:
    """
    Busca uma produto pelo ID na tabela `produto`.
    Args:
        session (AsyncSession): Sessão ativa com o banco de dados.
        id_produto (int): ID da produto a ser consultada.
    Returns:
        Optional[ProdutoGet]: Objeto contendo os dados da produto, ou None se não encontrada.
    """
    # Preparando a expressão SQL
    param = {"id_produto": id_produto}
    query = """
        SELECT 
            id_produto, nome, quantidade, valor_uni, descricao, categoria, marca
        FROM produtos
        WHERE id_produto=:id_produto
        LIMIT 1
    """
    
    # Executando a query e salvando o resultado
    result = (await session.execute(text(query), param)).mappings().fetchone()

    # Retornando ProdutoGet
    return None if result is None else ProdutoGet(**result)
