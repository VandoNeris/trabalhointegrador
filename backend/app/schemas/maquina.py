from pydantic import BaseModel, model_validator, StringConstraints, IntConstraints, FloatConstraints, DateConstraints
from typing import Optional, Annotated
import datetime as dt

class Maquina(BaseModel):
    nome: Annotated[
        str,
        StringConstraints(max_length=60)
    ]
    descricao: Optional[str] = None
class MaquinaGet(Maquina):
    id_maquina: Annotated[
        int,
        IntConstraints(gt=0)
    ]
