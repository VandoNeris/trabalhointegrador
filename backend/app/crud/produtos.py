from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import text
from typing import Optional, List
from backend.app.schemas.produtos import Produto, ProdutoGet
from backend.app.crud import produtos as produto_crud


async def listar_produtos(session: AsyncSession) -> List[produto_crud.ProdutoGet]:
    """
    Retorna uma lista de todos os produtos cadastrados no banco de dados.
    Args:
        session (AsyncSession): Sessão ativa com o banco de dados.
    Returns:
        List[ProdutoGet]: Lista de objetos do tipo ProdutoGet contendo os dados de cada produto.
    """
    # Preparando a expressão SQL
    query = text("""
        SELECT
            id_produto, nome, descricao, preco, estoque
        FROM produto
    """)
    
    # Executando a query e salvando o resultado
    result = (await session.execute(query)).mappings().all()
    
    # Retornando lista de ProdutoGet
    return [ produto_crud.ProdutoGet(**row) for row in result ]

async def criar_produto(session: AsyncSession, produto: produto_crud.Produto) -> Optional[int]:
    """
    Insere um novo produto na tabela `produto`.
    Args:
        session (AsyncSession): Sessão ativa com o banco de dados.
        produto (Produto): Objeto contendo os dados do produto a ser inserido.
    Returns:
        Optional[int]: ID do produto criado, ou None em caso de falha.
    Raises:
        SQLAlchemyError: Caso ocorra algum erro durante a execução ou commit da transação.
    """
    # Preparando a expressão SQL
    param = produto.dict()
    query = text("""
        INSERT INTO produto (nome, quantidade, valor, descricao, categoria, marca) )
        VALUES (:nome, :quantidade, :valor, :descricao, :categoria, :marca)
        RETURNING id_produto
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
    
async def atualizar_produto(session: AsyncSession, produto: produto_crud.Produto, id_produto: int) -> Optional[int]:
    """
    Atualiza os dados de um produto existente com base no ID informado.
    Args:
        session (AsyncSession): Sessão ativa com o banco de dados.
        produto (Produto): Objeto contendo os novos dados do produto.
        id_produto (int): ID do produto a ser atualizado.
    Returns:
        Optional[int]: ID do produto atualizado, ou None em caso de falha.
    Raises:
        SQLAlchemyError: Caso ocorra algum erro durante a execução ou commit da transação.
    """
    # Preparando a expressão SQL
    param = produto.dict()
    query = text("""
        UPDATE produto
        SET nome = :nome, quantidade = :quantidade, valor = :valor, descricao = :descricao, categoria = :categoria, marca = :marca
        WHERE id_produto = :id_produto
        RETURNING id_produto
    """)
    
    # Protegendo de excessões
    try:
        # Executando a query e salvando o resultado
        result = (await session.execute(query, {**param, 'id_produto': id_produto}))
        await session.commit()
        return result.scalar()      # Retorna o id em caso de sucesso
    except SQLAlchemyError as e:
        await session.rollback()    # Reverte a transação em caso de erro
        raise e
    
async def remover_produto(session: AsyncSession, id_produto: int) -> Optional[int]:
    """
    Remove um produto da tabela `produto` com base no ID informado.
    Args:
        session (AsyncSession): Sessão ativa com o banco de dados.
        id_produto (int): ID do produto a ser removido.
    Returns:
        Optional[int]: ID do produto removido, ou None em caso de falha.
    Raises:
        SQLAlchemyError: Caso ocorra algum erro durante a execução ou commit da transação.
    """
    # Preparando a expressão SQL
    query = text("""
        DELETE FROM produto
        WHERE id_produto = :id_produto
        RETURNING id_produto
    """)
    
    # Protegendo de excessões
    try:
        # Executando a query e salvando o resultado
        result = (await session.execute(query, {'id_produto': id_produto}))
        await session.commit()
        return result.scalar()      # Retorna o id em caso de sucesso
    except SQLAlchemyError as e:
        await session.rollback()    # Reverte a transação em caso de erro
        raise e

async def buscar_produto(session: AsyncSession, id_produto: int) -> Optional[produto_crudProdutoGet]:
    """
    Busca um produto pelo ID informado.
    Args:
        session (AsyncSession): Sessão ativa com o banco de dados.
        id_produto (int): ID do produto a ser buscado.
    Returns:
        Optional[ProdutoGet]: Objeto do tipo ProdutoGet contendo os dados do produto, ou None se não encontrado.
    Raises:
        SQLAlchemyError: Caso ocorra algum erro durante a execução da query.
    """
    # Preparando a expressão SQL
    query = text("""
        SELECT id_produto, nome, quantidade, valor, descricao, categoria, marca
        FROM produto
        WHERE id_produto = :id_produto
    """)
    
    # Executando a query e salvando o resultado
    result = (await session.execute(query, {'id_produto': id_produto})).mappings().first()
    
    # Retornando o ProdutoGet ou None se não encontrado
    return produto_crud.ProdutoGet(**result) if result else None