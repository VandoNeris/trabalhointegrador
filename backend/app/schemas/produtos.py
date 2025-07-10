from pydantic import BaseModel, model_validator, StringConstraints, Field
from typing import Optional, Annotated
import datetime as dt

class Produtos(BaseModel):
    nome: Annotated[ str, StringConstraints(min_length=1, max_length=60) ]
    quantidade: Annotated[ int, Field(gt=0) ]
    valor: Annotated[ float, Field(gt=0, lt=10**9) ]
    descricao: Optional[ str ] = None
    categoria: Annotated[ str, StringConstraints(min_length=1, max_length=60) ]
    marca: Annotated[ str, StringConstraints(min_length=1, max_length=60) ]

class ProdutosGet(Produtos):
    id_produto: Annotated[ int, Field(gt=0) ]

