from pydantic import BaseModel, model_validator, StringConstraints, Field
from typing import Optional, Annotated
import datetime as dt
from enum import IntEnum

class TipoUsuario(IntEnum):
    ADMIN = 0
    REGULAR = 1

    def __str__(self):
        return self.name.capitalize()
    
    @classmethod
    def choices(cls):
        return [ (member.value, member.name.capitalize()) for member in cls ]

class Usuario(BaseModel):
    senha: Annotated[ str, StringConstraints(min_length=1, max_length=60) ]
    tipo: TipoUsuario

class UsuarioGet(Usuario):
    id_usuario: Annotated[ str, StringConstraints(min_length=1, max_length=60) ]
