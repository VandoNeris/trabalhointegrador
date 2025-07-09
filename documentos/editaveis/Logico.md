### Conversão Lógico/Conceitual

usuario (
    <u>codusuario</u>,
    senha,
    tipo
)

pessoa (
    <u>codpessoa</u>, 
    tipo, 
    nome, 
    endereco, 
    email, 
    telefone,
    <u style="text-decoration: underline dashed;">cpf*</u>,
    <u style="text-decoration: underline dashed;">cnpj*</u>,
    <u style="text-decoration: underline dashed;">razaosocial</u>
)

cobranca (
    <u>codcobranca</u>,
    dtemissao,
    dtvencimento,
    <u style="text-decoration: underline dashed;">dtpagamento</u>,
    statuspag,
    valor
)

maquina (
    <u>codmaquina</u>,
    nome,
    <u style="text-decoration: underline dashed;">descricao</u>
)

compra (
    <u>codcompra</u>,
    dtemissao,
    dtvencimento,
    <u style="text-decoration: underline dashed;">dtpagamento</u>,
    locentrega,
    statuspag,
    valor,
    codpessoa(pessoa)                                                       <!-- AtribuicaoCompra (1:N) -->
)

ordemserv (
    <u>codos</u>,
    data,
    local,
    <u style="text-decoration: underline dashed;">descricao</u>,
    codpessoa(pessoa)                                                       <!-- AtribuicaoServico (1:N) -->
)

servico (
    <u>codservico</u>,
    horas,
    quilometros,
    <u style="text-decoration: underline dashed;">descricao</u>,
    codordemserv(ordemserv),                                                <!-- Execução (1:N) -->
    <u style="text-decoration: underline dashed;">codcobranca(cobranca)</u> <!-- Gera (1:N) -->
)

produtos (
    <u>codproduto</u>,
    nome,
    quantidade,
    valor,
    <u style="text-decoration: underline dashed;">descricao</u>,
    categoria,
    marca
)

compatibilidade (                                                           <!-- Compatibilidade (N:N) -->
    <u>codcompatibilidade</u>,
    codproduto(produtos),
    codmaquina(maquina)
)

consumocompra (                                                             <!-- ConsumoCompra (N:N) -->
    <u>codconsumocompra</u>,
    quantidade,
    codproduto(produtos),
    codcompra(compra)
)

consumoservico (                                                            <!-- ConsumoServico (N:N) -->
    <u>codconsumoservico</u>,
    quantidade,
    codproduto(produtos),
    codservico(servico)
)

### [Modelo Lógico Relacional - Tractomaq](https://dbdiagram.io/d/Tractomaq-6862e705f413ba350896d9cf)

```
Project project_name {
  database_type: 'PostgreSQL'
  Note: 'Tractomaq'
}

Table usuario {
    id_usuario varchar(60) [pk]
    senha varchar(60) [not null]
    tipo boolean [not null]
}

Table pessoa {
    id_pessoa integer [pk, increment]
    tipo boolean [not null, note:'0-Fisica\n1-Juridica']
    nome varchar(60) [not null]
    endereco varchar(100) [not null]
    email varchar(60) [not null]
    telefone varchar(13) [not null]
    cpf varchar(11) [unique]
    cnpj varchar(14) [unique]
    razaosocial varchar(60)
}

Table cobranca {
    id_cobranca integer [pk, increment]
    dt_emissao date [not null]
    dt_vencimento date [not null]
    dt_pagamento date
    statuspag smallint [not null]
    valor numeric(12,2) [not null]
}

Table maquina {
    id_maquina integer [pk, increment]
    nome varchar(60) [not null]
    descricao text
}

Table compra {
    id_compra integer [pk, increment]
    dt_emissao date [not null]
    dt_vencimento date [not null]
    dt_pagamento date
    loc_entrega varchar(100) [not null]
    statuspag smallint [not null]
    valor numeric(12,2) [not null]
    id_pessoa integer [not null]            // AtribuicaoCompra (1:N)
}
Ref registracompra: compra.id_pessoa > pessoa.id_pessoa

Table ordem_servico {
    id_ordem_servico integer [pk, increment]
    dt_ordem_servico date [not null]
    local varchar(100) [not null]
    descricao text
    id_pessoa integer [not null]            // AtribuicaoServico (1:N)
}
Ref registraordemservico: ordem_servico.id_pessoa > pessoa.id_pessoa

Table servico {
    id_servico integer [pk, increment]
    horas numeric(5,2) [not null]
    quilometros numeric(6, 2) [not null]
    descricao text
    id_ordem_servico integer [not null]                // Execução (1:N)
    id_cobranca integer                     // Gera (1:N)
}
Ref execução: servico.id_ordem_servico > ordem_servico.id_ordem_servico
Ref gera: servico.id_cobranca > cobranca.id_cobranca

Table produtos {
    id_produto integer [pk, increment]
    nome varchar(60) [not null]
    quantidade integer [not null]
    valor numeric(12,2) [not null]
    descricao text
    categoria varchar(60) [not null]
    marca varchar(60) [not null]
}

Table compatibilidade {                     // Compatibilidade (N:N)
    id_compatibilidade integer [pk, increment]
    id_produto integer [not null]
    id_maquina integer [not null]
}
Ref compatibilidade: compatibilidade.id_produto <> produtos.id_produto
Ref compatibilidade: compatibilidade.id_maquina <> maquina.id_maquina

Table consumocompra {                       // ConsumoCompra (N:N)
    id_consumocompra integer [pk, increment]
    quantidade integer [not null]
    id_produto integer [not null]
    id_compra integer [not null]
}
Ref consumocompra: consumocompra.id_produto <> produtos.id_produto
Ref consumocompra: consumocompra.id_compra <> compra.id_compra

Table consumoservico {                      // ConsumoServico (N:N)
    id_consumoservico integer [pk, increment]
    quantidade integer [not null]
    id_produto integer [not null]
    id_servico integer [not null]
}
Ref consumoservico: consumoservico.id_produto <> produtos.id_produto
Ref consumoservico: consumoservico.id_servico <> servico.id_servico
```
