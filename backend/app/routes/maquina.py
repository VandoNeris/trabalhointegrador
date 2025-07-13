from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from backend.database import get_session
from backend.app.schemas.maquina import Maquina, MaquinaGet
from backend.app.schemas.MensagemResposta import MensagemResposta
from backend.app.crud import maquina as maquina_crud
from typing import List

router = APIRouter()

# Definindo excessão personalidada
http_exc_pk = HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Maquina com o ID informado não foi encontrada.")

@router.get("/maquinas", response_model=List[MaquinaGet])
async def get_maquinas(session: AsyncSession = Depends(get_session)):
    result = await maquina_crud.listar_maquinas(session)

    return result

@router.post("/maquina", response_model=MensagemResposta, status_code=status.HTTP_201_CREATED)
async def post_maquina(maquina: Maquina, session: AsyncSession = Depends(get_session)):
    result = await maquina_crud.criar_maquina(session, maquina)

    return MensagemResposta(message="Maquina criada", id=result)

@router.put("/maquina/{id_maquina}", response_model=MensagemResposta)
async def put_maquina(id_maquina: int, maquina: Maquina, session: AsyncSession = Depends(get_session)):
    result = await maquina_crud.atualizar_maquina(session, maquina, id_maquina)
    if result is None: raise http_exc_pk
    
    return MensagemResposta(message="Maquina atualizada", id=result)

@router.delete("/maquina/{id_maquina}", response_model=MensagemResposta)
async def delete_maquina(id_maquina: int, session: AsyncSession = Depends(get_session)):
    result = await maquina_crud.remover_maquina(session, id_maquina)
    if result is None: raise http_exc_pk
    
    return MensagemResposta(message="Maquina removida", id=result)

@router.get("/maquina/{id_maquina}", response_model=MaquinaGet)
async def get_maquina(id_maquina: int, session: AsyncSession = Depends(get_session)):
    result = await maquina_crud.buscar_maquina(session, id_maquina)
    if result is None: raise http_exc_pk
    
    return result
