from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from backend.database import get_session
from backend.app.schemas.usuario import Usuario, UsuarioGet
from backend.app.schemas.MensagemResposta import MensagemResposta
from backend.app.crud import usuario as usuario_crud
from typing import List
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel

from core.security import verify_password, create_access_token

router = APIRouter()

# Definindo excessão personalidada
http_exc_pk = HTTPException(status_code=404, detail="Usuario com o ID informado não foi encontrada.")

class Token(BaseModel):
    access_token: str
    token_type: str

# Define que o token deve ser buscado na URL /usuario/token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/usuario/token")

@router.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(), 
    session: AsyncSession = Depends(get_session)
):

    usuario = await usuario_crud.buscar_usuario_por_nome(session, form_data.username)
    
    if not usuario or not verify_password(form_data.password, usuario.senha_hashed):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuário ou senha incorretos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = create_access_token(
        data={"sub": usuario.nome_usuario}  # "sub" é o sujeito do token
    )
    
    return {"access_token": access_token, "token_type": "bearer"}

# @router.get("/usuarios", response_model=List[UsuarioGet])
# async def get_usuarios(session: AsyncSession = Depends(get_session)):
#     result = await usuario_crud.listar_usuarios(session)

#     return result

# @router.post("/usuario", response_model=MensagemResposta, status_code=status.HTTP_201_CREATED)
# async def post_usuario(usuario: Usuario, session: AsyncSession = Depends(get_session)):
#     result = await usuario_crud.criar_usuario(session, usuario)

#     return MensagemResposta(message="Usuario criada", id=result)

# @router.put("/usuario/{id_usuario}", response_model=MensagemResposta)
# async def put_usuario(id_usuario: int, usuario: Usuario, session: AsyncSession = Depends(get_session)):
#     result = await usuario_crud.atualizar_usuario(session, usuario, id_usuario)
#     if result is None: raise http_exc_pk
    
#     return MensagemResposta(message="Usuario atualizada", id=result)

# @router.delete("/usuario/{id_usuario}", response_model=MensagemResposta)
# async def delete_usuario(id_usuario: int, session: AsyncSession = Depends(get_session)):
#     result = await usuario_crud.remover_usuario(session, id_usuario)
#     if result is None: raise http_exc_pk
    
#     return MensagemResposta(message="Usuario removida", id=result)

# @router.get("/usuario/{id_usuario}", response_model=UsuarioGet)
# async def get_usuario(id_usuario: int, session: AsyncSession = Depends(get_session)):
#     result = await usuario_crud.buscar_usuario(session, id_usuario)
#     if result is None: raise http_exc_pk
    
#     return result
