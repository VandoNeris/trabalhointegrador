from pydantic import BaseModel, constr
from typing import Optional
import datetime as dt

class Compatibilidade(BaseModel):
    id_produto: int
    id_maquina: int
class CompatibilidadeGet(Compatibilidade):
    id_compatibilidade: int
