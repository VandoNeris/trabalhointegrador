from pydantic import BaseModel, model_validator, StringConstraints, IntConstraints, FloatConstraints, DateConstraints
from typing import Optional, Annotated
import datetime as dt

class ConsumoCompra(BaseModel):
    quantidade: Annotated[
        int,
        IntConstraints(gt=0)
    ]
    id_produto: Annotated[
        int,
        IntConstraints(gt=0)
    ]
    id_compra: Annotated[
        int,
        IntConstraints(gt=0)
    ]
class ConsumoCompraGet(ConsumoCompra):
    id_consumocompra: Annotated[
        int,
        IntConstraints(gt=0)
    ]
