from pydantic import BaseModel, model_validator, StringConstraints, Field
from typing import Optional, Annotated
import datetime as dt

class Compra(BaseModel):
    dt_emissao: dt.date
    dt_vencimento: dt.date
    dt_pagamento: Optional[dt.date] = None
    status_pag: Annotated[
        int,
        Field(gt=0)
    ]
    valor: Annotated[
        float,
        Field(gt=0, le=9999999999.99)
    ]
    loc_entrega: Annotated[
        str,
        StringConstraints(max_length=100)
    ]
    id_pessoa: Annotated[
        int,
        Field(gt=0)
    ]

    @model_validator(mode='after')
    @classmethod
    def checar_datas(cls, model):
        if model.dt_vencimento < model.dt_emissao:
            raise ValueError('Data de vencimento não pode ser anterior à data de emissão')
        if model.dt_pagamento and model.dt_pagamento < model.dt_emissao:
            raise ValueError('Data de pagamento não pode ser anterior à data de emissão')
        return model
    
class CompraGet(Compra):
    id_pessoa: Annotated[
        int,
        Field(gt=0)
    ]
