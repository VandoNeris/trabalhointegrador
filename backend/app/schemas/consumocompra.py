from pydantic import BaseModel, model_validator, StringConstraints, Field
from typing import Optional, Annotated
import datetime as dt

class ConsumoCompra(BaseModel):
    quantidade: Annotated[ int, Field(gt=0) ]
    id_produto: Annotated[ int, Field(gt=0) ]
    id_compra: Annotated[ int, Field(gt=0) ]

class ConsumoCompraGet(ConsumoCompra):
    id_consumocompra: Annotated[ int, Field(gt=0) ]
