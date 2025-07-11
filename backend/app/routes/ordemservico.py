from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from backend.database import get_session
from backend.app.schemas.ordemservico import OrdemServico, OrdemServicoGet
from backend.app.schemas.MensagemResposta import MensagemResposta
from backend.app.crud import ordemservico as ordemservico_crud
from typing import List

router = APIRouter()

# Definindo excessão personalidada
http_exc_pk = HTTPException(status_code=404, detail="OrdemServico com o ID informado não foi encontrada.")
http_exc_fk = HTTPException(status_code=422, detail="Não foi possível criar a ordemservico: vínculo com outra tabela é inválido ou inexistente.")

@router.get("/ordemservicos", response_model=List[OrdemServicoGet])
async def get_ordemservicos(session: AsyncSession = Depends(get_session)):
    result = await ordemservico_crud.listar_ordemservicos(session)
    
    return result

@router.post("/ordemservico", response_model=MensagemResposta, status_code=status.HTTP_201_CREATED)
async def post_ordemservico(ordemservico: OrdemServico, session: AsyncSession = Depends(get_session)):
    result = await ordemservico_crud.criar_ordemservico(session, ordemservico)
    if result is None: raise http_exc_fk

    return MensagemResposta(message="OrdemServico criada", id=result)

@router.put("/ordemservico/{id_ordemservico}", response_model=MensagemResposta)
async def put_ordemservico(id_ordemservico: int, ordemservico: OrdemServico, session: AsyncSession = Depends(get_session)):
    result = await ordemservico_crud.atualizar_ordemservico(session, ordemservico, id_ordemservico)
    if result is None: raise http_exc_pk
    
    return MensagemResposta(message="OrdemServico atualizada", id=result)

@router.delete("/ordemservico/{id_ordemservico}", response_model=MensagemResposta)
async def delete_ordemservico(id_ordemservico: int, session: AsyncSession = Depends(get_session)):
    result = await ordemservico_crud.remover_ordemservico(session, id_ordemservico)
    if result is None: raise http_exc_pk
    
    return MensagemResposta(message="OrdemServico removida", id=result)

@router.get("/ordemservico/{id_ordemservico}", response_model=OrdemServicoGet)
async def get_ordemservico(id_ordemservico: int, session: AsyncSession = Depends(get_session)):
    result = await ordemservico_crud.buscar_ordemservico(session, id_ordemservico)
    if result is None: raise http_exc_pk
    
    return result
