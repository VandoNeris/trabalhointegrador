from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.app.schemas.pessoa import Pessoa, PessoaGet
from backend.app.crud import pessoa as pessoa_crud
from typing import List

router = APIRouter()

@router.get("/pessoas", response_model=List[PessoaGet])
def get_pessoas(db: Session = Depends(get_db)):
    return pessoa_crud.listar_pessoas(db)

@router.post("/pessoas")
def post_pessoa(pessoa: Pessoa, db: Session = Depends(get_db)):
    pessoa_crud.criar_pessoa(db, pessoa)
    return {"message": "Pessoa cadastrada"}
