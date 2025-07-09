from pydantic import BaseModel, model_validator, StringConstraints, Field
from typing import Optional, Annotated
import datetime as dt

class Servico(BaseModel):
    horas: Annotated[
        float,
        Field(gt=0, le=999.99)
    ]
    quilometros: Annotated[
        float,
        Field(gt=0, le=9999.99)
    ]
    descricao: Optional[str] = None
    id_ordem_servico: Annotated[
        int,
        Field(gt=0)
    ]
    id_cobranca: Optional[Annotated[
        int,
        Field(gt=0)
    ]] = None
class ServicoGet(Servico):
    id_servico: Annotated[
        int,
        Field(gt=0)
    ]
