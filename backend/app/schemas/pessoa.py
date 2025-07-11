from pydantic import BaseModel, model_validator, StringConstraints, Field, EmailStr
from typing import Optional, Annotated
import datetime as dt
from enum import IntEnum

class TipoPessoa(IntEnum):
    FISICA = 0
    JURIDICA = 1

    def __str__(self):
        return self.name.capitalize()
    
    @classmethod
    def choices(cls):
        return [ (member.value, member.name.capitalize()) for member in cls ]

class Pessoa(BaseModel):
    tipo: TipoPessoa
    nome: Annotated[ str, StringConstraints(min_length=1, max_length=60) ]
    endereco: Annotated[ str, StringConstraints(min_length=1, max_length=100) ]
    email: EmailStr
    telefone: Annotated[ str, StringConstraints(min_length=1, max_length=13) ]
    cpf: Optional[ Annotated[ str, StringConstraints(min_length=1, max_length=11) ] ] = None
    cnpj: Optional[ Annotated[ str, StringConstraints(min_length=1, max_length=14) ] ] = None
    razaosocial: Optional[ Annotated[ str, StringConstraints(min_length=1, max_length=60) ] ] = None
    
    @model_validator(mode='after')
    @classmethod
    def checar_documentos(cls, model):
        if model.cpf and model.cnpj:
            raise ValueError('Uma pessoa não pode ter CPF e CNPJ simultaneamente')
        if model.tipo == TipoPessoa.FISICA and not model.cpf:
            raise ValueError('CPF obrigatório para pessoa física')
        if model.tipo == TipoPessoa.JURIDICA and not model.cnpj:
            raise ValueError('CNPJ obrigatório para pessoa jurídica')
        return model
    
class PessoaGet(Pessoa):
    id_pessoa: Annotated[ int, Field(gt=0) ]
