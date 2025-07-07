from pydantic import BaseModel
from typing import Optional
import datetime as dt

class Cobranca(BaseModel):
    dt_emissao: dt.date
    dt_vencimento: dt.date
    dt_pagamento: Optional[dt.date] = None
    status_pag: int
    valor: float

class CobrancaGet(Cobranca):
    id_cobranca: int
