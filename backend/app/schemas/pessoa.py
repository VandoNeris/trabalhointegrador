from pydantic import BaseModel
from typing import Optional
import datetime as dt

class Pessoa(BaseModel):
    tipo: bool
    nome: str
    endereco: str
    telefone: str
    cpf: Optional[str] = None
    cnpj: Optional[str] = None
    razaosocial: Optional[str] = None

class PessoaGet(Pessoa):
    id_pessoa: int
