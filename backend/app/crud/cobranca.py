from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import text
from typing import Optional, List
from backend.app.crud import cobranca as cobranca_crud

async def listar_cobrancas(session: AsyncSession) -> List[cobranca_crud.CobrancaGet]:
    """
    Retorna uma lista de todas as cobranças cadastradas no banco de dados.
    Args:
        session (AsyncSession): Sessão ativa com o banco de dados.
    Returns:
        List[CobrancaGet]: Lista de objetos do tipo CobrancaGet contendo os dados de cada cobrança.
    """
    # Preparando a expressão SQL
    query = text("""
        SELECT
            id_cobranca, dt_emissao, dt_vencimento, dt_pagamento, statuspag, valor
        FROM cobranca
    """)
    
    # Executando a query e salvando o resultado
    result = (await session.execute(query)).mappings().all()
    
    # Retornando lista de CobrancaGet
    return [ cobranca_crud.CobrancaGet(**row) for row in result ]

async def criar_cobranca(session: AsyncSession, cobranca: cobranca_crud.Cobranca) -> Optional[int]: