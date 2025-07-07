from pydantic import BaseModel, constr
from typing import Optional
import datetime as dt

class Maquina(BaseModel):
    nome: str
    descricao: str
class MaquinaGet(Maquina):
    id_maquina: int
