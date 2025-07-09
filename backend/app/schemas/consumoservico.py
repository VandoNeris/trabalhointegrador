from pydantic import BaseModel, model_validator, StringConstraints, IntConstraints, FloatConstraints, DateConstraints
from typing import Optional, Annotated
import datetime as dt

class ConsumoServico(BaseModel):
    quantidade: Annotated[
        int,
        IntConstraints(gt=0)
    ]
    id_produto: Annotated[
        int,
        IntConstraints(gt=0)
    ]
    id_servico: Annotated[
        int,
        IntConstraints(gt=0)
    ]
class ConsumoServicoGet(ConsumoServico):
    id_consumoservico: Annotated[
        int,
        IntConstraints(gt=0)
    ]
