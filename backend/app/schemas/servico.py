from pydantic import BaseModel, constr
from typing import Optional
import datetime as dt

class Servico(BaseModel):
    horas: float
    quilometros: float
    descricao: Optional[str] = None
    id_ordem_servico: int
    id_cobranca: Optional[int] = None
class ServicoGet(Servico):
    id_servico: int
