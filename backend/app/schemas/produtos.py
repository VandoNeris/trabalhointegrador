from pydantic import BaseModel, constr
from typing import Optional
import datetime as dt

class Produtos(BaseModel):
    nome: str
    quantidade: int
    valor: float
    descricao: Optional[str] = None
    categoria: str
    marca: str
class ProdutosGet(Produtos):
    id_produto: int
