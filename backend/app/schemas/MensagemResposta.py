from pydantic import BaseModel, model_validator, StringConstraints, Field
from typing import Optional, Annotated
import datetime as dt

class MensagemResposta(BaseModel):
    message: str
    id: Optional[ int ] = None
