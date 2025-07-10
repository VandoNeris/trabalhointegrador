from pydantic import BaseModel, model_validator, StringConstraints, Field
from typing import Optional, Annotated
import datetime as dt
from enum import IntEnum

class StatusPag(IntEnum):
    PENDENTE = 0
    PAGO = 1
    VENCIDO = 2
    
    def __str__(self):
        return self.name.capitalize()
    
    @classmethod
    def choices(cls):
        return [(member.value, member.name.capitalize()) for member in cls]

class Cobranca(BaseModel):
    dt_emissao: dt.date
    dt_vencimento: dt.date
    dt_pagamento: Optional[ dt.date ] = None
    status_pag: StatusPag
    valor: Annotated[ float, Field(gt=0, lt=10**9) ]
    
    @model_validator(mode='after')
    @classmethod
    def checar_datas(cls, model):
        # Validação entre datas
        if model.dt_vencimento < model.dt_emissao:
            raise ValueError('Data de vencimento não pode ser anterior à data de emissão')
        if model.dt_pagamento and model.dt_pagamento < model.dt_emissao:
            raise ValueError('Data de pagamento não pode ser anterior à data de emissão')
        
        # Validação de acordo com status de pagamento
        if model.status_pag == StatusPag.PAGO:
            if model.dt_pagamento is None:
                raise ValueError('Data de pagamento deve ser informada se o status for Pago')
        elif model.dt_pagamento is not None:
            raise ValueError('Data de pagamento não deve ser informada se o status for Pendente ou Vencido')
        
        return model

class CobrancaGet(Cobranca):
    id_cobranca: Annotated[ int, Field(gt=0) ]
