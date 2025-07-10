from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.app.schemas.ordemservico import OrdemServico, OrdemServicoGet
from backend.app.schemas.MensagemResposta import MensagemResposta
from backend.app.crud import ordemservico as ordemservico_crud
from typing import List

router = APIRouter()

# Definindo excessão personalidada
http_exc_pk = HTTPException(status_code=404, detail="OrdemServico com o ID informado não foi encontrada.")
http_exc_fk = HTTPException(status_code=422, detail="Não foi possível criar a ordemservico: vínculo com outra tabela é inválido ou inexistente.")

@router.get("/ordemservicos", response_model=List[OrdemServicoGet])
def get_ordemservicos(db: Session = Depends(get_db)):
    result = ordemservico_crud.listar_ordemservicos(db)
    
    return result

@router.post("/ordemservico", response_model=MensagemResposta, status_code=status.HTTP_201_CREATED)
def post_ordemservico(ordemservico: OrdemServico, db: Session = Depends(get_db)):
    result = ordemservico_crud.criar_ordemservico(db, ordemservico)
    if result is None: raise http_exc_fk

    return MensagemResposta(message="OrdemServico criada", id=result)

@router.put("/ordemservico/{id_ordemservico}", response_model=MensagemResposta)
def put_ordemservico(id_ordemservico: int, ordemservico: OrdemServico, db: Session = Depends(get_db)):
    result = ordemservico_crud.atualizar_ordemservico(db, ordemservico, id_ordemservico)
    if result is None: raise http_exc_pk
    
    return MensagemResposta(message="OrdemServico atualizada", id=result)

@router.delete("/ordemservico/{id_ordemservico}", response_model=MensagemResposta)
def delete_ordemservico(id_ordemservico: int, db: Session = Depends(get_db)):
    result = ordemservico_crud.remover_ordemservico(db, id_ordemservico)
    if result is None: raise http_exc_pk
    
    return MensagemResposta(message="OrdemServico removida", id=result)

@router.get("/ordemservico/{id_ordemservico}", response_model=OrdemServicoGet)
def get_ordemservico(id_ordemservico: int, db: Session = Depends(get_db)):
    result = ordemservico_crud.buscar_ordemservico(db, id_ordemservico)
    if result is None: raise http_exc_pk
    
    return result
