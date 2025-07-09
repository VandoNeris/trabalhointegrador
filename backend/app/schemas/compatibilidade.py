from pydantic import BaseModel, model_validator, StringConstraints, IntConstraints, FloatConstraints, DateConstraints
from typing import Optional, Annotated
import datetime as dt

class Compatibilidade(BaseModel):
    id_produto: Annotated[
        int,
        IntConstraints(gt=0)
    ]
    id_maquina: Annotated[
        int,
        IntConstraints(gt=0)
    ]
class CompatibilidadeGet(Compatibilidade):
    id_compatibilidade: Annotated[
        int,
        IntConstraints(gt=0)
    ]
