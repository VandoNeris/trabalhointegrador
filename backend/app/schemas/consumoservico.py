from pydantic import BaseModel, model_validator, StringConstraints, Field
from typing import Optional, Annotated
import datetime as dt

class ConsumoServico(BaseModel):
    quantidade: Annotated[
        int,
        Field(gt=0)
    ]
    id_produto: Annotated[
        int,
        Field(gt=0)
    ]
    id_servico: Annotated[
        int,
        Field(gt=0)
    ]
class ConsumoServicoGet(ConsumoServico):
    id_consumoservico: Annotated[
        int,
        Field(gt=0)
    ]
