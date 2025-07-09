from pydantic import BaseModel, model_validator, StringConstraints, IntConstraints, FloatConstraints, DateConstraints
from typing import Optional, Annotated
import datetime as dt

class Usuario(BaseModel):
    senha: Annotated[
        str,
        StringConstraints(min_length=8, max_length=60)
    ]
    tipo: bool

class UsuarioGet(Usuario):
    id_usuario: Annotated[
        str,
        StringConstraints(max_length=60)
    ]
