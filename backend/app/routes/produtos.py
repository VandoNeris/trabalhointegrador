from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from backend.database import get_session
from backend.app.schemas.produtos import Produto, ProdutoGet
from backend.app.schemas.MensagemResposta import MensagemResposta
from backend.app.crud import produtos as produto_crud
from typing import List

router = APIRouter()

# Definindo excessão personalidada
http_exc_pk = HTTPException(status_code=404, detail="Produto com o ID informado não foi encontrada.")

@router.get("/produtos", response_model=List[ProdutoGet])
async def get_produtos(session: AsyncSession = Depends(get_session)):
    result = await produto_crud.listar_produtos(session)

    return result

@router.post("/produto", response_model=MensagemResposta, status_code=status.HTTP_201_CREATED)
async def post_produto(produto: Produto, session: AsyncSession = Depends(get_session)):
    result = await produto_crud.criar_produto(session, produto)

    return MensagemResposta(message="Produto criada", id=result)

@router.put("/produto/{id_produto}", response_model=MensagemResposta)
async def put_produto(id_produto: int, produto: Produto, session: AsyncSession = Depends(get_session)):
    result = await produto_crud.atualizar_produto(session, produto, id_produto)
    if result is None: raise http_exc_pk
    
    return MensagemResposta(message="Produto atualizada", id=result)

@router.delete("/produto/{id_produto}", response_model=MensagemResposta)
async def delete_produto(id_produto: int, session: AsyncSession = Depends(get_session)):
    result = await produto_crud.remover_produto(session, id_produto)
    if result is None: raise http_exc_pk
    
    return MensagemResposta(message="Produto removida", id=result)

@router.get("/produto/{id_produto}", response_model=ProdutoGet)
async def get_produto(id_produto: int, session: AsyncSession = Depends(get_session)):
    result = await produto_crud.buscar_produto(session, id_produto)
    if result is None: raise http_exc_pk
    
    return result
