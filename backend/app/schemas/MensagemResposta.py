from pydantic import BaseModel, model_validator, StringConstraints, IntConstraints, FloatConstraints, DateConstraints
from typing import Optional, Annotated
import datetime as dt

class MensagemResposta(BaseModel):
    message: str
    id_pessoa: Optional[int] = None
