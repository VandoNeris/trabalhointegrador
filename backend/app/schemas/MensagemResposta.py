from pydantic import BaseModel
from typing import Optional
import datetime as dt

class MensagemResposta(BaseModel):
    message: str
    id_pessoa: Optional[int] = None
