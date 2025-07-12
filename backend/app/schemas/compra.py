from pydantic import BaseModel, model_validator, StringConstraints, Field
from typing import Optional, Annotated
import datetime as dt

class Compra(BaseModel):
    loc_entrega: Annotated[ str, StringConstraints(min_length=1, max_length=100) ]
    valor: Annotated[ float, Field(gt=0, lt=10**8) ]
    dt_emissao: dt.date
    dt_vencimento: dt.date
    dt_entrega: Optional[ dt.date ] = None
    dt_pagamento: Optional[ dt.date ] = None
    id_pessoa: Annotated[ int, Field(gt=0) ]

    @model_validator(mode='after')
    @classmethod
    def checar_datas(cls, model):
        # Validação entre datas
        if model.dt_vencimento < model.dt_emissao:
            raise ValueError('Data de vencimento não pode ser anterior à data de emissão')
        if model.dt_pagamento is not None and model.dt_pagamento < model.dt_emissao:
            raise ValueError('Data de pagamento não pode ser anterior à data de emissão')
        if model.dt_entrega is not None and model.dt_entrega < model.dt_emissao:
            raise ValueError('Data de entrega não pode ser anterior à data de emissão')
        
        return model
    
class CompraGet(Compra):
    id_pessoa: Annotated[ int, Field(gt=0) ]
