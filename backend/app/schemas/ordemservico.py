from pydantic import BaseModel, model_validator, StringConstraints, Field
from typing import Optional, Annotated
import datetime as dt

class OrdemServico(BaseModel):
    dt_ordem_servico: dt.date
    local: Annotated[
        str,
        StringConstraints(max_length=100)
    ]
    descricao: Optional[str] = None
    id_pessoa: Annotated[
        int,
        Field(gt=0)
    ]
class OrdemServicoGet(OrdemServico):
    id_ordem_servico: Annotated[
        int,
        Field(gt=0)
    ]
