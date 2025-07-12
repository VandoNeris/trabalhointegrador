from pydantic import BaseModel, model_validator, StringConstraints, Field
from typing import Optional, Annotated
import datetime as dt

class Produto(BaseModel):
    nome: Annotated[ str, StringConstraints(min_length=1, max_length=60) ]
    quantidade: Annotated[ int, Field(gt=0) ]
    valor_uni: Annotated[ float, Field(gt=0, lt=10**8) ]
    descricao: Optional[ str ] = None
    categoria: Optional[ Annotated[ str, StringConstraints(min_length=1, max_length=60) ] ] = None
    marca: Optional[ Annotated[ str, StringConstraints(min_length=1, max_length=60) ] ] = None

class ProdutoGet(Produto):
    id_produto: Annotated[ int, Field(gt=0) ]
