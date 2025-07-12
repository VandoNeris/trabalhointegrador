from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import text
from typing import Optional, List
from backend.app.schemas.pessoa import Pessoa, PessoaGet

async def listar_pessoas(session: AsyncSession) -> List[PessoaGet]:
    """
    Retorna uma lista de todas as pessoas cadastradas no banco de dados.
    Args:
        session (AsyncSession): Sessão ativa com o banco de dados.
    Returns:
        List[PessoaGet]: Lista de objetos do tipo PessoaGet contendo os dados de cada pessoa.
    """
    # Preparando a expressão SQL
    query = text("""
        SELECT
            id_pessoa, tipo, nome, endereco, telefone, email, cpf, cnpj, razao_social
        FROM pessoa 
    """)
    
    # Executando a query e salvando o resultado
    result = (await session.execute(query)).mappings().all()
    
    # Retornando lista de PessoaGet
    return [ PessoaGet(**row) for row in result ]

async def listar_pessoas_por_tipo(session: AsyncSession, tipo: int) -> List[PessoaGet]:
    """
    Retorna uma lista de pessoas de um tipo específico.

    Args:
        session (AsyncSession): Sessão ativa com o banco de dados.
        tipo (int): O tipo de pessoa a ser filtrado (0 para física, 1 para jurídica).

    Returns:
        List[PessoaGet]: Lista de objetos PessoaGet contendo os dados de cada pessoa encontrada.
    """
    # Preparando a expressão SQL
    query = text("""
        SELECT
            id_pessoa, tipo, nome, endereco, telefone, email, cpf, cnpj, razao_social
        FROM pessoa
        WHERE tipo=:tipo_filtro 
    """)
    
    # Executando a query e salvando o resultado
    result = (await session.execute(query, {"tipo_filtro": tipo})).mappings().all()
    
    # Retornando lista de PessoaGet
    return [PessoaGet(**row) for row in result]

async def criar_pessoa(session: AsyncSession, pessoa: Pessoa) -> Optional[int]:
    """
    Insere uma nova pessoa na tabela `pessoa`.
    Args:
        session (AsyncSession): Sessão ativa com o banco de dados.
        pessoa (Pessoa): Objeto contendo os dados da pessoa a ser inserida.
    Returns:
        Optional[int]: ID da pessoa criada, ou None em caso de falha.
    Raises:
        SQLAlchemyError: Caso ocorra algum erro durante a execução ou commit da transação.
    """
    # Preparando a expressão SQL
    param = pessoa.dict()
    query = text("""
        INSERT INTO pessoa (tipo, nome, endereco, telefone, email, cpf, cnpj, razao_social)
        VALUES (:tipo, :nome, :endereco, :telefone, :email, :cpf, :cnpj, :razao_social)
        RETURNING id_pessoa
    """)

    # Protegendo de excessões
    try:
        # Executando a query e salvando o resultado
        result = (await session.execute(query, param))
        await session.commit()
        return result.scalar()      # Retorna o id em caso de sucesso
    except SQLAlchemyError as e:
        await session.rollback()    # Reverte a transação em caso de erro
        raise e

async def atualizar_pessoa(session: AsyncSession, pessoa: Pessoa, id_pessoa: int) -> Optional[int]:
    """
    Atualiza os dados de uma pessoa existente com base no ID informado.
    Args:
        session (AsyncSession): Sessão ativa com o banco de dados.
        pessoa (Pessoa): Objeto contendo os novos dados da pessoa.
        id_pessoa (int): ID da pessoa a ser atualizada.
    Returns:
        Optional[int]: ID da pessoa atualizada, ou None em caso de falha.
    Raises:
        SQLAlchemyError: Caso ocorra algum erro durante a execução ou commit da transação.
    """
    # Preparando a expressão SQL
    param = pessoa.dict()
    param.update({"id_pessoa": id_pessoa})
    query = text("""
        UPDATE pessoa
        SET 
            tipo=:tipo, nome=:nome, endereco=:endereco, telefone=:telefone, email=:email, cpf=:cpf, cnpj=:cnpj, razao_social=:razao_social
        WHERE id_pessoa=:id_pessoa
        RETURNING id_pessoa
    """)

    # Protegendo de excessões
    try:
        # Executando a query e salvando o resultado
        result = (await session.execute(query, param))
        await session.commit()
        return result.scalar()      # Retorna o id em caso de sucesso
    except SQLAlchemyError as e:
        await session.rollback()    # Reverte a transação em caso de erro
        raise e

async def remover_pessoa(session: AsyncSession, id_pessoa: int) -> Optional[int]:
    """
    Remove uma pessoa da tabela `pessoa` com base no ID informado.
    Args:
        session (AsyncSession): Sessão ativa com o banco de dados.
        id_pessoa (int): ID da pessoa a ser removida.
    Returns:
        Optional[int]: ID da pessoa removida, ou None caso não exista.
    Raises:
        SQLAlchemyError: Caso ocorra algum erro durante a execução ou commit da transação.
    """
    # Preparando a expressão SQL
    query = text("""
        DELETE FROM pessoa WHERE id_pessoa=:id_pessoa RETURNING id_pessoa
    """)

    # Protegendo de excessões
    try:
        # Executando a query e salvando o resultado
        result = (await session.execute(query, {"id_pessoa": id_pessoa}))
        await session.commit()
        return result.scalar()      # Retorna o id em caso de sucesso
    except SQLAlchemyError as e:
        await session.rollback()    # Reverte a transação em caso de erro
        raise e

async def buscar_pessoa(session: AsyncSession, id_pessoa: int) -> Optional[PessoaGet]:
    """
    Busca uma pessoa pelo ID na tabela `pessoa`.
    Args:
        session (AsyncSession): Sessão ativa com o banco de dados.
        id_pessoa (int): ID da pessoa a ser consultada.
    Returns:
        Optional[PessoaGet]: Objeto contendo os dados da pessoa, ou None se não encontrada.
    """
    # Preparando a expressão SQL
    query = text("""
        SELECT 
            id_pessoa, tipo, nome, endereco, telefone, email, cpf, cnpj, razao_social
        FROM pessoa
        WHERE id_pessoa=:id_pessoa
        LIMIT 1
    """)
    
    # Executando a query e salvando o resultado
    result = (await session.execute(query, {"id_pessoa": id_pessoa})).mappings().fetchone()

    # Retornando PessoaGet
    return None if result is None else PessoaGet(**result)
