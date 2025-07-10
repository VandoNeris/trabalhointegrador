from pydantic import BaseModel, model_validator, StringConstraints, Field
from typing import Optional, Annotated
import datetime as dt

class Servico(BaseModel):
    horas: Annotated[ float, Field(gt=0, lt=10**3) ]
    quilometros: Annotated[ float, Field(gt=0, lt=10**4) ]
    descricao: Optional[ str ] = None
    id_ordemservico: Annotated[ int, Field(gt=0) ]
    id_cobranca: Optional[ Annotated[ int, Field(gt=0) ] ] = None

class ServicoGet(Servico):
    id_servico: Annotated[ int, Field(gt=0) ]
