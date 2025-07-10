from pydantic import BaseModel, model_validator, StringConstraints, Field
from typing import Optional, Annotated
import datetime as dt

class Compatibilidade(BaseModel):
    id_produto: Annotated[ int, Field(gt=0) ]
    id_maquina: Annotated[ int, Field(gt=0) ]

class CompatibilidadeGet(Compatibilidade):
    id_compatibilidade: Annotated[ int, Field(gt=0) ]
