from pydantic import BaseModel, constr
from typing import Optional
import datetime as dt

class ConsumoCompra(BaseModel):
    quantidade: int
    id_produto: int
    id_compra: int
class ConsumoCompraGet(ConsumoCompra):
    id_consumocompra: int
