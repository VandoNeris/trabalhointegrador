from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from backend.database import get_session
from backend.app.schemas.consumoservico import ConsumoServico, ConsumoServicoGet
from backend.app.schemas.MensagemResposta import MensagemResposta
from backend.app.crud import consumoservico as consumoservico_crud
from typing import List

router = APIRouter()

# Definindo excessão personalidada
http_exc_pk = HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="ConsumoServico com o ID informado não foi encontrada.")
http_exc_fk = HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Não foi possível criar a consumoservico: vínculo com outra tabela é inválido ou inexistente.")

@router.get("/consumoservicos", response_model=List[ConsumoServicoGet])
async def get_consumoservicos(session: AsyncSession = Depends(get_session)):
    result = await consumoservico_crud.listar_consumoservicos(session)

    return result

@router.post("/consumoservico", response_model=MensagemResposta, status_code=status.HTTP_201_CREATED)
async def post_consumoservico(consumoservico: ConsumoServico, session: AsyncSession = Depends(get_session)):
    result = await consumoservico_crud.criar_consumoservico(session, consumoservico)
    if result is None: raise http_exc_fk

    return MensagemResposta(message="ConsumoServico criada", id=result)

@router.put("/consumoservico/{id_consumo_servico}", response_model=MensagemResposta)
async def put_consumoservico(id_consumo_servico: int, consumoservico: ConsumoServico, session: AsyncSession = Depends(get_session)):
    result = await consumoservico_crud.atualizar_consumoservico(session, consumoservico, id_consumo_servico)
    if result is None: raise http_exc_pk
    
    return MensagemResposta(message="ConsumoServico atualizada", id=result)

@router.delete("/consumoservico/{id_consumo_servico}", response_model=MensagemResposta)
async def delete_consumoservico(id_consumo_servico: int, session: AsyncSession = Depends(get_session)):
    result = await consumoservico_crud.remover_consumoservico(session, id_consumo_servico)
    if result is None: raise http_exc_pk
    
    return MensagemResposta(message="ConsumoServico removida", id=result)

@router.get("/consumoservico/{id_consumo_servico}", response_model=ConsumoServicoGet)
async def get_consumoservico(id_consumo_servico: int, session: AsyncSession = Depends(get_session)):
    result = await consumoservico_crud.buscar_consumoservico(session, id_consumo_servico)
    if result is None: raise http_exc_pk
    
    return result
