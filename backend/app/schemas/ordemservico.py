from pydantic import BaseModel, constr
from typing import Optional
import datetime as dt

class OrdemServico(BaseModel):
    dt_ordem_servico: dt.date
    local: str
    descricao: Optional[str] = None
    id_pessoa: int
class OrdemServicoGet(OrdemServico):
    id_ordem_servico: int
