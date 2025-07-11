from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.app.schemas.usuario import Usuario, UsuarioGet
from backend.app.schemas.MensagemResposta import MensagemResposta
from backend.app.crud import usuario as usuario_crud
from typing import List

router = APIRouter()

# Definindo excessão personalidada
http_exc_pk = HTTPException(status_code=404, detail="Usuario com o ID informado não foi encontrada.")

@router.get("/usuarios", response_model=List[UsuarioGet])
def get_usuarios(db: Session = Depends(get_db)):
    result = usuario_crud.listar_usuarios(db)

    return result

@router.post("/usuario", response_model=MensagemResposta, status_code=status.HTTP_201_CREATED)
def post_usuario(usuario: Usuario, db: Session = Depends(get_db)):
    result = usuario_crud.criar_usuario(db, usuario)

    return MensagemResposta(message="Usuario criada", id=result)

@router.put("/usuario/{id_usuario}", response_model=MensagemResposta)
def put_usuario(id_usuario: int, usuario: Usuario, db: Session = Depends(get_db)):
    result = usuario_crud.atualizar_usuario(db, usuario, id_usuario)
    if result is None: raise http_exc_pk
    
    return MensagemResposta(message="Usuario atualizada", id=result)

@router.delete("/usuario/{id_usuario}", response_model=MensagemResposta)
def delete_usuario(id_usuario: int, db: Session = Depends(get_db)):
    result = usuario_crud.remover_usuario(db, id_usuario)
    if result is None: raise http_exc_pk
    
    return MensagemResposta(message="Usuario removida", id=result)

@router.get("/usuario/{id_usuario}", response_model=UsuarioGet)
def get_usuario(id_usuario: int, db: Session = Depends(get_db)):
    result = usuario_crud.buscar_usuario(db, id_usuario)
    if result is None: raise http_exc_pk
    
    return result
