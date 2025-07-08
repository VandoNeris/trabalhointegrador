from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from backend.database import get_db
from backend.app.schemas.pessoa import Pessoa, PessoaGet
from backend.app.schemas.MensagemResposta import MensagemResposta
from backend.app.crud import pessoa as pessoa_crud
from typing import List

router = APIRouter()

# Instancias para controle do status de operação
# http_exc = HTTPException(status_code=404, detail="Pessoa não encontrada")
http_exc = HTTPException(status_code=404, detail="Recurso não encontrado")

@router.get("/pessoas", response_model=List[PessoaGet])
def get_pessoas(db: Session = Depends(get_db)):
    result = pessoa_crud.listar_pessoas(db)

    return result

@router.post("/pessoa", response_model=MensagemResposta)
def post_pessoa(pessoa: Pessoa, db: Session = Depends(get_db)):
    result = pessoa_crud.criar_pessoa(db, pessoa)

    return MensagemResposta(message="Pessoa criada", id_pessoa=result)

@router.put("/pessoa/{id_pessoa}", response_model=MensagemResposta)
def put_pessoa(id_pessoa: int, pessoa: Pessoa, db: Session = Depends(get_db)):
    result = pessoa_crud.atualizar_pessoa(db, pessoa, id_pessoa)
    if result is None: raise http_exc
    
    return MensagemResposta(message="Pessoa atualizada", id_pessoa=result)

@router.delete("/pessoa/{id_pessoa}", response_model=MensagemResposta)
def delete_pessoa(id_pessoa: int, db: Session = Depends(get_db)):
    result = pessoa_crud.remover_pessoa(db, id_pessoa)
    if result is None: raise http_exc
    
    return MensagemResposta(message="Pessoa removida", id_pessoa=result)

@router.get("/pessoa/{id_pessoa}", response_model=PessoaGet)
def get_pessoa(id_pessoa: int, db: Session = Depends(get_db)):
    result = pessoa_crud.buscar_pessoa(db, id_pessoa)
    if result is None: raise http_exc
    
    return result