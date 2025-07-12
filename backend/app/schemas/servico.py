from pydantic import BaseModel, model_validator, StringConstraints, Field
from typing import Optional, Annotated
import datetime as dt

class Servico(BaseModel):
    id_ordem_servico: Annotated[ int, Field(gt=0) ]
    valor: Annotated[ float, Field(gt=0, lt=10**8) ]
    dt_emissao: dt.date
    dt_vencimento: dt.date
    quilometros: Annotated[ float, Field(gt=0, lt=10**5) ]
    horas: Annotated[ float, Field(gt=0, lt=10**4) ]
    dt_pagamento: Optional[ dt.date ] = None
    descricao: Optional[ str ] = None
    
    @model_validator(mode='after')
    @classmethod
    def checar_datas(cls, model):
        # Validação entre datas
        if model.dt_vencimento < model.dt_emissao:
            raise ValueError('Data de vencimento não pode ser anterior à data de emissão')
        if model.dt_pagamento is not None and model.dt_pagamento < model.dt_emissao:
            raise ValueError('Data de pagamento não pode ser anterior à data de emissão')
        
        return model

class ServicoGet(Servico):
    id_servico: Annotated[ int, Field(gt=0) ]
