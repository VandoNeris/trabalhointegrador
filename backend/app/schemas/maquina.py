from pydantic import BaseModel, model_validator, StringConstraints, Field
from typing import Optional, Annotated
import datetime as dt

class Maquina(BaseModel):
    nome: Annotated[ str, StringConstraints(min_length=1, max_length=60) ]
    descricao: Optional[ str ] = None

class MaquinaGet(Maquina):
    id_maquina: Annotated[ int, Field(gt=0) ]
