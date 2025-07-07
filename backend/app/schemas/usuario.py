from pydantic import BaseModel
from typing import Optional
import datetime as dt

class Usuario(BaseModel):
    senha: str
    tipo: bool

class UsuarioGet(Usuario):
    id_usuario: int
