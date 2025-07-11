from sqlalchemy.orm import Session
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from backend.app.schemas.usuario import Usuario, UsuarioGet
from typing import Optional, List

def listar_usuarios(db: Session) -> List[UsuarioGet]:
    """
    Retorna uma lista de todas as usuarios cadastradas no banco de dados.
    Args:
        db (Session): Sessão ativa com o banco de dados.
    Returns:
        List[UsuarioGet]: Lista de objetos do tipo UsuarioGet contendo os dados de cada usuario.
    """
    # Preparando a expressão SQL
    query = text("""
        SELECT
            id_usuario, senha, tipo
        FROM usuario
    """)
    
    # Executando a query e salvando o resultado
    result = db.execute(query).mappings().all()
    
    # Retornando lista de UsuarioGet
    return [ UsuarioGet(**row) for row in result ]

def criar_usuario(db: Session, usuario: Usuario) -> Optional[int]:
    """
    Insere uma nova usuario na tabela `usuario`.
    Args:
        db (Session): Sessão ativa com o banco de dados.
        usuario (Usuario): Objeto contendo os dados da usuario a ser inserida.
    Returns:
        Optional[int]: ID da usuario criada, ou None em caso de falha.
    Raises:
        SQLAlchemyError: Caso ocorra algum erro durante a execução ou commit da transação.
    """
    # Preparando a expressão SQL
    param = usuario.dict()
    query = text("""
        INSERT INTO usuario (senha, tipo)
        VALUES (:senha, :tipo)
        RETURNING id_usuario
    """)

    # Protegendo de excessões
    try:
        # Executando a query e salvando o resultado
        result = db.execute(query, param)
        db.commit()
        return result.scalar()      # Retorna o id em caso de sucesso
    except SQLAlchemyError as e:
        db.rollback()               # Reverte a transação em caso de erro
        raise e

def atualizar_usuario(db: Session, usuario: Usuario, id_usuario: int) -> Optional[int]:
    """
    Atualiza os dados de uma usuario existente com base no ID informado.
    Args:
        db (Session): Sessão ativa com o banco de dados.
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
            senha=:senha, tipo=:tipo
        WHERE id_usuario = :id_usuario
        RETURNING id_usuario
    """)

    # Protegendo de excessões
    try:
        # Executando a query e salvando o resultado
        result = db.execute(query, param)
        db.commit()
        return result.scalar()      # Retorna o id em caso de sucesso
    except SQLAlchemyError as e:
        db.rollback()               # Reverte a transação em caso de erro
        raise e

def remover_usuario(db: Session, id_usuario: int) -> Optional[int]:
    """
    Remove uma usuario da tabela `usuario` com base no ID informado.
    Args:
        db (Session): Sessão ativa com o banco de dados.
        id_usuario (int): ID da usuario a ser removida.
    Returns:
        Optional[int]: ID da usuario removida, ou None caso não exista.
    Raises:
        SQLAlchemyError: Caso ocorra algum erro durante a execução ou commit da transação.
    """
    # Preparando a expressão SQL
    query = text("""
        DELETE FROM usuario WHERE id_usuario = :id_usuario RETURNING id_usuario
    """)

    # Protegendo de excessões
    try:
        # Executando a query e salvando o resultado
        result = db.execute(query, {"id_usuario": id_usuario})
        db.commit()
        return result.scalar()      # Retorna o id em caso de sucesso
    except SQLAlchemyError as e:
        db.rollback()               # Reverte a transação em caso de erro
        raise e

def buscar_usuario(db: Session, id_usuario: int) -> Optional[UsuarioGet]:
    """
    Busca uma usuario pelo ID na tabela `usuario`.
    Args:
        db (Session): Sessão ativa com o banco de dados.
        id_usuario (int): ID da usuario a ser consultada.
    Returns:
        Optional[UsuarioGet]: Objeto contendo os dados da usuario, ou None se não encontrada.
    """
    # Preparando a expressão SQL
    query = text("""
        SELECT 
            id_usuario, senha, tipo
        FROM usuario
        WHERE id_usuario = :id_usuario
        LIMIT 1
    """)
    
    # Executando a query e salvando o resultado
    result = db.execute(query, {"id_usuario": id_usuario}).mappings().fetchone()

    # Retornando UsuarioGet
    return None if result is None else UsuarioGet(**result)
