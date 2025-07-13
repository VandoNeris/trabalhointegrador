from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from backend.database import get_session
from backend.app.schemas.compra import Compra, CompraGet
from backend.app.schemas.MensagemResposta import MensagemResposta
from backend.app.crud import compra as compra_crud
from typing import List

router = APIRouter()

# Definindo excessão personalidada
http_exc_pk = HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Compra com o ID informado não foi encontrada.")
http_exc_fk = HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Não foi possível criar a compra: vínculo com outra tabela é inválido ou inexistente.")

@router.get("/compras", response_model=List[CompraGet])
async def get_compras(session: AsyncSession = Depends(get_session)):
    result = await compra_crud.listar_compras(session)

    return result

@router.post("/compra", response_model=MensagemResposta, status_code=status.HTTP_201_CREATED)
async def post_compra(compra: Compra, session: AsyncSession = Depends(get_session)):
    result = await compra_crud.criar_compra(session, compra)
    if result is None: raise http_exc_fk

    return MensagemResposta(message="Compra criada", id=result)

@router.put("/compra/{id_compra}", response_model=MensagemResposta)
async def put_compra(id_compra: int, compra: Compra, session: AsyncSession = Depends(get_session)):
    result = await compra_crud.atualizar_compra(session, compra, id_compra)
    if result is None: raise http_exc_pk
    
    return MensagemResposta(message="Compra atualizada", id=result)

@router.delete("/compra/{id_compra}", response_model=MensagemResposta)
async def delete_compra(id_compra: int, session: AsyncSession = Depends(get_session)):
    result = await compra_crud.remover_compra(session, id_compra)
    if result is None: raise http_exc_pk
    
    return MensagemResposta(message="Compra removida", id=result)

@router.get("/compra/{id_compra}", response_model=CompraGet)
async def get_compra(id_compra: int, session: AsyncSession = Depends(get_session)):
    result = await compra_crud.buscar_compra(session, id_compra)
    if result is None: raise http_exc_pk
    
    return result
