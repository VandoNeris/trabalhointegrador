from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.app.schemas.compra import Compra, CompraGet
from backend.app.schemas.MensagemResposta import MensagemResposta
from backend.app.crud import compra as compra_crud
from typing import List

router = APIRouter()

# Definindo excessão personalidada
http_exc_pk = HTTPException(status_code=404, detail="Compra com o ID informado não foi encontrada.")
http_exc_fk = HTTPException(status_code=422, detail="Não foi possível criar a compra: vínculo com outra tabela é inválido ou inexistente.")

@router.get("/compras", response_model=List[CompraGet])
def get_compras(db: Session = Depends(get_db)):
    result = compra_crud.listar_compras(db)

    return result

@router.post("/compra", response_model=MensagemResposta, status_code=status.HTTP_201_CREATED)
def post_compra(compra: Compra, db: Session = Depends(get_db)):
    result = compra_crud.criar_compra(db, compra)
    if result is None: raise http_exc_fk

    return MensagemResposta(message="Compra criada", id=result)

@router.put("/compra/{id_compra}", response_model=MensagemResposta)
def put_compra(id_compra: int, compra: Compra, db: Session = Depends(get_db)):
    result = compra_crud.atualizar_compra(db, compra, id_compra)
    if result is None: raise http_exc_pk
    
    return MensagemResposta(message="Compra atualizada", id=result)

@router.delete("/compra/{id_compra}", response_model=MensagemResposta)
def delete_compra(id_compra: int, db: Session = Depends(get_db)):
    result = compra_crud.remover_compra(db, id_compra)
    if result is None: raise http_exc_pk
    
    return MensagemResposta(message="Compra removida", id=result)

@router.get("/compra/{id_compra}", response_model=CompraGet)
def get_compra(id_compra: int, db: Session = Depends(get_db)):
    result = compra_crud.buscar_compra(db, id_compra)
    if result is None: raise http_exc_pk
    
    return result
