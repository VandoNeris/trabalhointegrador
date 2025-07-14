from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import text
from fastapi import Depends, HTTPException, status
from typing import Optional, Annotated, List
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
# from jwt.exceptions import InvalidTokenError

from backend.app.schemas.usuario import Usuario, UsuarioGet, TokenData 
from backend.database import get_session
from backend.app.core.config import settings
from backend.app.core.security import hash_password

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/usuario/token")

# Definindo excessão personalidada
http_exc_unauthn = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Usuário ou senha incorretos", headers={"WWW-Authenticate": "Bearer"})
http_exc_unauthz = HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Não autorizado, tipo de usuário não têm permissão necessária")

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
    param = usuario.model_dump()
    query = """
        INSERT INTO usuario (nome, senha, tipo)
        VALUES (:nome, :senha, 0)
        RETURNING id_usuario
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
    
async def buscar_usuario(session: AsyncSession, nome_filter: str) -> Optional[UsuarioGet]:
    """
    Busca uma usuario pelo nome na tabela `usuario`.
    Args:
        session (AsyncSession): Sessão ativa com o banco de dados.
        nome (str): nome do usuario a ser consultada.
    Returns:
        Optional[UsuarioGet]: Objeto contendo os dados da usuario, ou None se não encontrada.
    """
    # Preparando a expressão SQL
    param = {"nome_filter": nome_filter}
    query = """
        SELECT 
            id_usuario,
            nome,
            senha,
            tipo
        FROM usuario
        WHERE nome=:nome_filter
    """
     
    # Executando a query e salvando o resultado
    result = (await session.execute(text(query), param)).mappings().fetchone()

    # Retornando UsuarioGet
    return None if result is None else UsuarioGet(**result)

async def buscar_usuario_por_tipo(session: AsyncSession, nome_filter: str, tipo_filter: Optional[int]) -> Optional[UsuarioGet]:
    """
    Busca uma usuario pelo nome na tabela `usuario`.
    Args:
        session (AsyncSession): Sessão ativa com o banco de dados.
        nome (str): nome do usuario a ser consultada.
        tipo (Optional[int]): Tipo do usuário (0 = admin; 1 = regular). Se None, ignora o tipo.
    Returns:
        Optional[UsuarioGet]: Objeto contendo os dados da usuario, ou None se não encontrada.
    """
    # Preparando a expressão SQL
    param = {"nome_filter": nome_filter, "tipo_filter": tipo_filter}
    query = """
        SELECT 
            id_usuario,
            nome,
            senha,
            tipo
        FROM usuario
        WHERE nome=:nome_filter
    """
    
    # Aplicando filtragem
    if tipo_filter is not None:
        query += " AND tipo=:tipo_filter"
    query += " LIMIT 1"
    
    # Executando a query e salvando o resultado
    result = (await session.execute(text(query), param)).mappings().fetchone()

    # Retornando UsuarioGet
    return None if result is None else UsuarioGet(**result)

def get_current_user(allowed_types: Optional[int | List[int]] = None):
    async def dependency(token: Annotated[ str, Depends(oauth2_scheme) ], session: AsyncSession = Depends(get_session)) -> Usuario:
        nonlocal allowed_types
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
            username = payload.get("sub")
            tipo = payload.get("tipo")
            if username is None: raise http_exc_unauthn
            token_data = TokenData(username=username, tipo=tipo)
        except (JWTError):  #, InvalidTokenError):
            raise http_exc_unauthn
        
        user = await buscar_usuario_por_tipo(session=session, nome_filter=token_data.username, tipo_filter=token_data.tipo)
        if user is None:
            raise http_exc_unauthn
        
        # Verificando permissões do usuário:
        if allowed_types is not None:
            if isinstance(allowed_types, int): allowed_types = [allowed_types]
            if user.tipo not in allowed_types:
                raise http_exc_unauthz

        return user
    return dependency
