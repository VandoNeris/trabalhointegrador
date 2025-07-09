from pydantic import BaseModel, model_validator, StringConstraints, IntConstraints, FloatConstraints, DateConstraints, EmailStr
from typing import Optional, Annotated
import datetime as dt

class Pessoa(BaseModel):
    tipo: bool
    nome: Annotated[
        str,
        StringConstraints(max_length=60)
    ]
    endereco: Annotated[
        str,
        StringConstraints(max_length=100)
    ]
    email: Optional[EmailStr] = None
    telefone: Annotated[
        str,
        StringConstraints(max_length=13)
    ]
    cpf: Optional[Annotated[
        str,
        StringConstraints(max_length=11)
    ]] = None
    cnpj: Optional[Annotated[
        str,
        StringConstraints(max_length=14)
    ]] = None
    razaosocial: Optional[Annotated[
        str,
        StringConstraints(max_length=60)
    ]] = None
    
    @model_validator(mode='after')
    @classmethod
    def checar_documentos(cls, model):
        if model.cpf and model.cnpj:
            raise ValueError('Uma pessoa não pode ser física (CPF) e Jurídica (CNPJ) simultaneamente')
        if not model.tipo and not model.cpf:
            raise ValueError('CPF obrigatório para pessoa física')
        if model.tipo and not model.cnpj:
            raise ValueError('CNPJ obrigatório para pessoa jurídica')
        return model
    
class PessoaGet(Pessoa):
    id_pessoa: Annotated[
        int,
        IntConstraints(gt=0)
    ]
