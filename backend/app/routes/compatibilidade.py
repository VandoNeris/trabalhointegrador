from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from backend.database import get_session
from backend.app.schemas.compatibilidade import Compatibilidade, CompatibilidadeGet
from backend.app.schemas.MensagemResposta import MensagemResposta
from backend.app.crud import compatibilidade as compatibilidade_crud
from typing import List

router = APIRouter()

# Definindo excessão personalidada
http_exc_pk = HTTPException(status_code=404, detail="Compatibilidade com o ID informado não foi encontrada.")
http_exc_fk = HTTPException(status_code=422, detail="Não foi possível criar a compatibilidade: vínculo com outra tabela é inválido ou inexistente.")

@router.get("/compatibilidades", response_model=List[CompatibilidadeGet])
async def get_compatibilidades(session: AsyncSession = Depends(get_session)):
    result = await compatibilidade_crud.listar_compatibilidades(session)

    return result

@router.post("/compatibilidade", response_model=MensagemResposta, status_code=status.HTTP_201_CREATED)
async def post_compatibilidade(compatibilidade: Compatibilidade, session: AsyncSession = Depends(get_session)):
    result = await compatibilidade_crud.criar_compatibilidade(session, compatibilidade)
    if result is None: raise http_exc_fk

    return MensagemResposta(message="Compatibilidade criada", id=result)

@router.put("/compatibilidade/{id_compatibilidade}", response_model=MensagemResposta)
async def put_compatibilidade(id_compatibilidade: int, compatibilidade: Compatibilidade, session: AsyncSession = Depends(get_session)):
    result = await compatibilidade_crud.atualizar_compatibilidade(session, compatibilidade, id_compatibilidade)
    if result is None: raise http_exc_pk
    
    return MensagemResposta(message="Compatibilidade atualizada", id=result)

@router.delete("/compatibilidade/{id_compatibilidade}", response_model=MensagemResposta)
async def delete_compatibilidade(id_compatibilidade: int, session: AsyncSession = Depends(get_session)):
    result = await compatibilidade_crud.remover_compatibilidade(session, id_compatibilidade)
    if result is None: raise http_exc_pk
    
    return MensagemResposta(message="Compatibilidade removida", id=result)

@router.get("/compatibilidade/{id_compatibilidade}", response_model=CompatibilidadeGet)
async def get_compatibilidade(id_compatibilidade: int, session: AsyncSession = Depends(get_session)):
    result = await compatibilidade_crud.buscar_compatibilidade(session, id_compatibilidade)
    if result is None: raise http_exc_pk
    
    return result
