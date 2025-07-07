from pydantic import BaseModel, constr
from typing import Optional
import datetime as dt

class ConsumoServico(BaseModel):
    quantidade: int
    id_produto: int
    id_servico: int
class ConsumoServicoGet(ConsumoServico):
    id_consumoservico: int
