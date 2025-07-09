from pydantic import BaseModel, model_validator, StringConstraints, IntConstraints, FloatConstraints, DateConstraints
from typing import Optional, Annotated
import datetime as dt

class Cobranca(BaseModel):
    dt_emissao: Annotated[
        dt.date,
        DateConstraints(le=dt.now().date())
    ]
    dt_vencimento: Annotated[
        dt.date,
        DateConstraints(le=dt.now().date())
    ]
    dt_pagamento: Optional[Annotated[
        dt.date,
        DateConstraints(le=dt.now().date())
    ]] = None
    status_pag: Annotated[
        int,
        IntConstraints(gt=0)
    ]
    valor: Annotated[
        float,
        FloatConstraints(gt=0, le=9999999999.99)
    ]
    
    @model_validator(mode='after')
    @classmethod
    def checar_datas(cls, model):
        if model.dt_vencimento < model.dt_emissao:
            raise ValueError('Data de vencimento não pode ser anterior à data de emissão')
        if model.dt_pagamento and model.dt_pagamento < model.dt_emissao:
            raise ValueError('Data de pagamento não pode ser anterior à data de emissão')
        return model

class CobrancaGet(Cobranca):
    id_cobranca: Annotated[
        int,
        IntConstraints(gt=0)
    ]
