from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from backend.database import get_session
from backend.app.schemas.consumocompra import ConsumoCompra, ConsumoCompraGet
from backend.app.schemas.MensagemResposta import MensagemResposta
from backend.app.crud import consumocompra as consumocompra_crud
from typing import List

router = APIRouter()

# Definindo excessão personalidada
http_exc_pk = HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="ConsumoCompra com o ID informado não foi encontrada.")
http_exc_fk = HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Não foi possível criar a consumocompra: vínculo com outra tabela é inválido ou inexistente.")

@router.get("/consumocompras", response_model=List[ConsumoCompraGet])
async def get_consumocompras(session: AsyncSession = Depends(get_session)):
    result = await consumocompra_crud.listar_consumocompras(session)

    return result

@router.post("/consumocompra", response_model=MensagemResposta, status_code=status.HTTP_201_CREATED)
async def post_consumocompra(consumocompra: ConsumoCompra, session: AsyncSession = Depends(get_session)):
    result = await consumocompra_crud.criar_consumocompra(session, consumocompra)
    if result is None: raise http_exc_fk

    return MensagemResposta(message="ConsumoCompra criada", id=result)

@router.put("/consumocompra/{id_consumo_compra}", response_model=MensagemResposta)
async def put_consumocompra(id_consumo_compra: int, consumocompra: ConsumoCompra, session: AsyncSession = Depends(get_session)):
    result = await consumocompra_crud.atualizar_consumocompra(session, consumocompra, id_consumo_compra)
    if result is None: raise http_exc_pk
    
    return MensagemResposta(message="ConsumoCompra atualizada", id=result)

@router.delete("/consumocompra/{id_consumo_compra}", response_model=MensagemResposta)
async def delete_consumocompra(id_consumo_compra: int, session: AsyncSession = Depends(get_session)):
    result = await consumocompra_crud.remover_consumocompra(session, id_consumo_compra)
    if result is None: raise http_exc_pk
    
    return MensagemResposta(message="ConsumoCompra removida", id=result)

@router.get("/consumocompra/{id_consumo_compra}", response_model=ConsumoCompraGet)
async def get_consumocompra(id_consumo_compra: int, session: AsyncSession = Depends(get_session)):
    result = await consumocompra_crud.buscar_consumocompra(session, id_consumo_compra)
    if result is None: raise http_exc_pk
    
    return result
