from pydantic import BaseModel, constr
from typing import Optional
import datetime as dt

class Compra(BaseModel):
    dt_emissao: dt.date
    dt_vencimento: dt.date
    dt_pagamento: Optional[dt.date] = None
    loc_entrega: str
    status_pag: int
    valor: float
    id_pessoa: int
class CompraGet(Compra):
    id_pessoa: int
