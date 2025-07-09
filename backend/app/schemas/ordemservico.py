from pydantic import BaseModel, model_validator, StringConstraints, IntConstraints, FloatConstraints, DateConstraints
from typing import Optional, Annotated
import datetime as dt

class OrdemServico(BaseModel):
    dt_ordem_servico: Annotated[
        dt.date,
        DateConstraints(le=dt.now().date())
    ]
    local: Annotated[
        str,
        StringConstraints(max_length=100)
    ]
    descricao: Optional[str] = None
    id_pessoa: Annotated[
        int,
        IntConstraints(gt=0)
    ]
class OrdemServicoGet(OrdemServico):
    id_ordem_servico: Annotated[
        int,
        IntConstraints(gt=0)
    ]
