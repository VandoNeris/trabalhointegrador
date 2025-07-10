from pydantic import BaseModel, model_validator, StringConstraints, Field
from typing import Optional, Annotated
import datetime as dt

class OrdemServico(BaseModel):
    dt_ordemservico: dt.date
    local: Annotated[ str, StringConstraints(min_length=1, max_length=100) ]
    descricao: Optional[ str ] = None
    id_pessoa: Annotated[ int, Field(gt=0) ]

class OrdemServicoGet(OrdemServico):
    id_ordemservico: Annotated[ int, Field(gt=0) ]
