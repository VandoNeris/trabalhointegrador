from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import text
from typing import Optional, List
from backend.app.schemas.usuario import Usuario, UsuarioGet
from backend.app.core.security import hash_password 

async def listar_usuarios(session: AsyncSession) -> List[UsuarioGet]:
    """
    Retorna uma lista de todas as usuarios cadastradas no banco de dados.
    Args:
        session (AsyncSession): Sessão ativa com o banco de dados.
    Returns:
        List[UsuarioGet]: Lista de objetos do tipo UsuarioGet contendo os dados de cada usuario.
    """
    # Preparando a expressão SQL
    
    query = text("""
        SELECT
            id_usuario, nome, senha, tipo
        FROM usuario
    """)
    
    # Executando a query e salvando o resultado
    result = (await session.execute(query)).mappings().all()
    
    # Retornando lista de UsuarioGet
    return [ UsuarioGet(**row) for row in result ]

async def criar_usuario(session: AsyncSession, usuario: Usuario) -> Optional[int]:
    """
    Insere uma nova usuario na tabela `usuario`.
    Args:
        session (AsyncSession): Sessão ativa com o banco de dados.
        usuario (Usuario): Objeto contendo os dados da usuario a ser inserida.
    Returns:
        Optional[int]: ID da usuario criada, ou None em caso de falha.
    Raises:
        SQLAlchemyError: Caso ocorra algum erro durante a execução ou commit da transação.
    """
    # Preparando a expressão SQL
    usuario.senha = hash_password(usuario.senha)

    param = usuario.dict()
    print(param)
    query = text("""
        INSERT INTO usuario (nome, senha, tipo)
        VALUES (:nome, :senha, 0)
        RETURNING id_usuario
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

async def atualizar_usuario(session: AsyncSession, usuario: Usuario, id_usuario: int) -> Optional[int]:
    """
    Atualiza os dados de uma usuario existente com base no ID informado.
    Args:
        session (AsyncSession): Sessão ativa com o banco de dados.
        usuario (Usuario): Objeto contendo os novos dados da usuario.
        id_usuario (int): ID da usuario a ser atualizada.
    Returns:
        Optional[int]: ID da usuario atualizada, ou None em caso de falha.
    Raises:
        SQLAlchemyError: Caso ocorra algum erro durante a execução ou commit da transação.
    """
    # Preparando a expressão SQL
    param = usuario.dict()
    param.update({"id_usuario": id_usuario})
    query = text("""
        UPDATE usuario
        SET 
            nome=:nome, senha=:senha, tipo=:tipo
        WHERE id_usuario=:id_usuario
        RETURNING id_usuario
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

async def remover_usuario(session: AsyncSession, id_usuario: int) -> Optional[int]:
    """
    Remove uma usuario da tabela `usuario` com base no ID informado.
    Args:
        session (AsyncSession): Sessão ativa com o banco de dados.
        id_usuario (int): ID da usuario a ser removida.
    Returns:
        Optional[int]: ID da usuario removida, ou None caso não exista.
    Raises:
        SQLAlchemyError: Caso ocorra algum erro durante a execução ou commit da transação.
    """
    # Preparando a expressão SQL
    query = text("""
        DELETE FROM usuario WHERE id_usuario=:id_usuario RETURNING id_usuario
    """)

    # Protegendo de excessões
    try:
        # Executando a query e salvando o resultado
        result = (await session.execute(query, {"id_usuario": id_usuario}))
        await session.commit()
        return result.scalar()      # Retorna o id em caso de sucesso
    except SQLAlchemyError as e:
        await session.rollback()               # Reverte a transação em caso de erro
        raise e

async def buscar_usuario(session: AsyncSession, id_usuario: int) -> Optional[UsuarioGet]:
    """
    Busca uma usuario pelo ID na tabela `usuario`.
    Args:
        session (AsyncSession): Sessão ativa com o banco de dados.
        id_usuario (int): ID da usuario a ser consultada.
    Returns:
        Optional[UsuarioGet]: Objeto contendo os dados da usuario, ou None se não encontrada.
    """
    # Preparando a expressão SQL
    query = text("""
        SELECT 
            id_usuario, nome, senha, tipo
        FROM usuario
        WHERE id_usuario=:id_usuario
        LIMIT 1
    """)
    
    # Executando a query e salvando o resultado
    result = (await session.execute(query, {"id_usuario": id_usuario})).mappings().fetchone()

    # Retornando UsuarioGet
    return None if result is None else UsuarioGet(**result)

async def buscar_usuario_por_nome(session: AsyncSession, nome: int) -> Optional[UsuarioGet]:
    """
    Busca uma usuario pelo nome na tabela `usuario`.
    Args:
        session (AsyncSession): Sessão ativa com o banco de dados.
        nome (str): nome do usuario a ser consultada.
    Returns:
        Optional[UsuarioGet]: Objeto contendo os dados da usuario, ou None se não encontrada.
    """
    # Preparando a expressão SQL
    query = text("""
        SELECT 
            nome
        FROM usuario
        WHERE nome=:nome
        LIMIT 1
    """)
    
    # Executando a query e salvando o resultado
    result = (await session.execute(query, {"nome": nome})).mappings().fetchone()

    # Retornando UsuarioGet
    return None if result is None else UsuarioGet(**result)
