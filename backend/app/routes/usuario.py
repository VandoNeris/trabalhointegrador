from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from backend.database import get_session
from backend.app.schemas.usuario import Usuario, UsuarioGet
from backend.app.schemas.MensagemResposta import MensagemResposta
from backend.app.crud import usuario as usuario_crud
from typing import List

router = APIRouter()

# Definindo excessão personalidada
http_exc_pk = HTTPException(status_code=404, detail="Usuario com o ID informado não foi encontrada.")

@router.get("/usuarios", response_model=List[UsuarioGet])
async def get_usuarios(session: AsyncSession = Depends(get_session)):
    result = await usuario_crud.listar_usuarios(session)

    return result

@router.post("/usuario", response_model=MensagemResposta, status_code=status.HTTP_201_CREATED)
async def post_usuario(usuario: Usuario, session: AsyncSession = Depends(get_session)):
    result = await usuario_crud.criar_usuario(session, usuario)

    return MensagemResposta(message="Usuario criada", id=result)

@router.put("/usuario/{id_usuario}", response_model=MensagemResposta)
async def put_usuario(id_usuario: int, usuario: Usuario, session: AsyncSession = Depends(get_session)):
    result = await usuario_crud.atualizar_usuario(session, usuario, id_usuario)
    if result is None: raise http_exc_pk
    
    return MensagemResposta(message="Usuario atualizada", id=result)

@router.delete("/usuario/{id_usuario}", response_model=MensagemResposta)
async def delete_usuario(id_usuario: int, session: AsyncSession = Depends(get_session)):
    result = await usuario_crud.remover_usuario(session, id_usuario)
    if result is None: raise http_exc_pk
    
    return MensagemResposta(message="Usuario removida", id=result)

@router.get("/usuario/{id_usuario}", response_model=UsuarioGet)
async def get_usuario(id_usuario: int, session: AsyncSession = Depends(get_session)):
    result = await usuario_crud.buscar_usuario(session, id_usuario)
    if result is None: raise http_exc_pk
    
    return result
