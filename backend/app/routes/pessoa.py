from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from backend.database import get_session
from backend.app.schemas.pessoa import Pessoa, PessoaGet
from backend.app.schemas.MensagemResposta import MensagemResposta
from backend.app.crud import pessoa as pessoa_crud
from backend.app.crud.usuario import get_current_user
from backend.app.schemas.usuario import Usuario, TipoUsuario

from typing import List

router = APIRouter()

# Definindo excessão personalidada
http_exc_pk = HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pessoa com o ID informado não foi encontrada.")

@router.get("/pessoas", response_model=List[PessoaGet])
async def get_pessoas(
    session: AsyncSession = Depends(get_session),
    current_user: Usuario = Depends(get_current_user([TipoUsuario.ADMIN, TipoUsuario.REGULAR]))
):
    result = await pessoa_crud.listar_pessoas(session)

    return result

@router.post("/pessoa", response_model=MensagemResposta, status_code=status.HTTP_201_CREATED)
async def post_pessoa(
    pessoa: Pessoa, 
    session: AsyncSession = Depends(get_session),
    current_user: Usuario = Depends(get_current_user([TipoUsuario.ADMIN]))
):
    result = await pessoa_crud.criar_pessoa(session, pessoa)

    return MensagemResposta(message="Pessoa criada", id=result)

@router.put("/pessoa/{id_pessoa}", response_model=MensagemResposta)
async def put_pessoa(
    id_pessoa: int, 
    pessoa: Pessoa, 
    session: AsyncSession = Depends(get_session),
    current_user: Usuario = Depends(get_current_user([TipoUsuario.ADMIN]))
):
    result = await pessoa_crud.atualizar_pessoa(session, pessoa, id_pessoa)
    if result is None: raise http_exc_pk
    
    return MensagemResposta(message="Pessoa atualizada", id=result)

@router.delete("/pessoa/{id_pessoa}", response_model=MensagemResposta)
async def delete_pessoa(
    id_pessoa: int, 
    session: AsyncSession = Depends(get_session),
    current_user: Usuario = Depends(get_current_user([TipoUsuario.ADMIN]))
):
    result = await pessoa_crud.remover_pessoa(session, id_pessoa)
    if result is None: raise http_exc_pk
    
    return MensagemResposta(message="Pessoa removida", id=result)

@router.get("/pessoa/{id_pessoa}", response_model=PessoaGet)
async def get_pessoa(
    id_pessoa: int, 
    session: AsyncSession = Depends(get_session),
    current_user: Usuario = Depends(get_current_user([TipoUsuario.ADMIN, TipoUsuario.REGULAR]))
):
    result = await pessoa_crud.buscar_pessoa(session, id_pessoa)
    if result is None: raise http_exc_pk
    
    return result

@router.get("/pessoas/{tipo}", response_model=List[PessoaGet])
async def get_pessoas(
    tipo:int, 
    session: AsyncSession = Depends(get_session), 
    current_user: Usuario = Depends(get_current_user([TipoUsuario.ADMIN, TipoUsuario.REGULAR]))
):
    print(tipo)
    result = await pessoa_crud.listar_pessoas_por_tipo(session, tipo)

    return result

@router.get("/dashboard/users/type")
async def get_pessoas_type(
    session: AsyncSession = Depends(get_session),
    current_user: Usuario = Depends(get_current_user([TipoUsuario.ADMIN, TipoUsuario.REGULAR]))
):
    result = await pessoa_crud.get_totais_por_tipo(session)

    return result
