from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from backend.database import get_session
from backend.app.schemas.servico import Servico, ServicoGet
from backend.app.schemas.MensagemResposta import MensagemResposta
from backend.app.crud import servico as servico_crud
from typing import List

router = APIRouter()

# Definindo excessão personalidada
http_exc_pk = HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Servico com o ID informado não foi encontrada.")
http_exc_fk = HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Não foi possível criar servico: vínculo com outra tabela é inválido ou inexistente.")

@router.get("/servicos", response_model=List[ServicoGet])
async def get_servicos(session: AsyncSession = Depends(get_session)):
    result = await servico_crud.listar_servicos(session)

    return result

@router.post("/servico", response_model=MensagemResposta, status_code=status.HTTP_201_CREATED)
async def post_servico(servico: Servico, session: AsyncSession = Depends(get_session)):
    result = await servico_crud.criar_servico(session, servico)
    if result is None: raise http_exc_fk

    return MensagemResposta(message="Servico criada", id=result)

@router.put("/servico/{id_servico}", response_model=MensagemResposta)
async def put_servico(id_servico: int, servico: Servico, session: AsyncSession = Depends(get_session)):
    result = await servico_crud.atualizar_servico(session, servico, id_servico)
    if result is None: raise http_exc_pk
    
    return MensagemResposta(message="Servico atualizada", id=result)

@router.delete("/servico/{id_servico}", response_model=MensagemResposta)
async def delete_servico(id_servico: int, session: AsyncSession = Depends(get_session)):
    result = await servico_crud.remover_servico(session, id_servico)
    if result is None: raise http_exc_pk
    
    return MensagemResposta(message="Servico removida", id=result)

@router.get("/servico/{id_servico}", response_model=ServicoGet)
async def get_servico(id_servico: int, session: AsyncSession = Depends(get_session)):
    result = await servico_crud.buscar_servico(session, id_servico)
    if result is None: raise http_exc_pk
    
    return result
