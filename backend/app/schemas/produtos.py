from pydantic import BaseModel, model_validator, StringConstraints, IntConstraints, FloatConstraints, DateConstraints
from typing import Optional, Annotated
import datetime as dt

class Produtos(BaseModel):
    nome: Annotated[
        str,
        StringConstraints(max_length=60)
    ]
    quantidade: Annotated[
        int,
        IntConstraints(gt=0)
    ]
    valor: Annotated[
        float,
        FloatConstraints(gt=0, le=9999999999.99)
    ]
    descricao: Optional[str] = None
    categoria: Annotated[
        str,
        StringConstraints(max_length=60)
    ]
    marca: Annotated[
        str,
        StringConstraints(max_length=60)
    ]
class ProdutosGet(Produtos):
    id_produto: Annotated[
        int,
        IntConstraints(gt=0)
    ]
