### Conversão Lógico/Conceitual

usuario (
    <u>codusuario</u>,
    nome,
    senha,
    tipo
)

pessoa (
    <u>codpessoa</u>, 
    tipo, 
    nome, 
    endereco, 
    telefone,
    <u style="text-decoration: underline dashed;">email</u>, 
    <u style="text-decoration: underline dashed;">cpf*</u>,
    <u style="text-decoration: underline dashed;">cnpj*</u>,
    <u style="text-decoration: underline dashed;">razaosocial</u>
)

produtos (
    <u>codproduto</u>,
    nome,
    quantidade,
    valoruni,
    <u style="text-decoration: underline dashed;">descricao</u>,
    <u style="text-decoration: underline dashed;">categoria</u>,
    <u style="text-decoration: underline dashed;">marca</u>
)

maquina (
    <u>codmaquina</u>,
    nome,
    <u style="text-decoration: underline dashed;">descricao</u>
)

compra (
    <u>codcompra</u>,
    codpessoa(pessoa),                                                     <!-- AtribuicaoCompra (1:N) -->
    locentrega,
    valor,
    dtemissao,
    dtvencimento,
    <u style="text-decoration: underline dashed;">dtentrega</u>,
    <u style="text-decoration: underline dashed;">dtpagamento</u>
)

ordemservico (
    <u>codordemservico</u>,
    codpessoa(pessoa),                                                     <!-- AtribuicaoServico (1:N) -->
    dtservico,
    locservico,
    <u style="text-decoration: underline dashed;">descricao</u>
)

servico (
    <u>codservico</u>,
    codordemservico(ordemservico)*,                                       <!-- Execucao (1:1) -->
    valor,
    dtemissao,
    dtvencimento,
    quilometros,
    horas,
    <u style="text-decoration: underline dashed;">dtpagamento</u>,
    <u style="text-decoration: underline dashed;">descricao</u>
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

### [Modelo Lógico Relacional - Tractomaq](https://dbdiagram.io/d/Traqtomac-6862e705f413ba350896d9cf)

```
Project project_name {
  database_type: 'PostgreSQL'
  Note: 'Tractomaq'
}

Table usuario {
    id_usuario integer [pk, increment]
    nome varchar(60) [unique, not null]
    senha varchar(255) [not null]
    tipo smallint [not null, note:'0-Administrador\n1-Regular']
}

Table pessoa {
    id_pessoa integer [pk, increment]
    tipo smallint [not null, note:'0-Fisica\n1-Juridica']
    nome varchar(60) [not null]
    endereco varchar(100) [not null]
    telefone varchar(13) [not null]
    email varchar(60)
    cpf varchar(11) [unique]
    cnpj varchar(14) [unique]
    razao_social varchar(60)
}

Table produtos {
    id_produto integer [pk, increment]
    nome varchar(60) [not null]
    quantidade integer [not null]
    valor_uni numeric(12,2) [not null]
    descricao text
    categoria varchar(60)
    marca varchar(60)
}

Table maquina {
    id_maquina integer [pk, increment]
    nome varchar(60) [not null]
    descricao text
}

Table compra {
    id_compra integer [pk, increment]
    loc_entrega varchar(100) [not null]
    valor numeric(12,2) [not null]
    dt_emissao date [not null]
    dt_vencimento date [not null]
    dt_entrega date
    dt_pagamento date
    id_pessoa integer [not null]            // AtribuicaoCompra (1:N)
}
Ref registracompra: compra.id_pessoa > pessoa.id_pessoa

Table ordemservico {
    id_ordem_servico integer [pk, increment]
    dt_servico date [not null]
    loc_servico varchar(100) [not null]
    descricao text
    id_pessoa integer [not null]            // AtribuicaoServico (1:N)
}
Ref atribuicaoservico: ordemservico.id_pessoa > pessoa.id_pessoa

Table servico {
    id_servico integer [pk, increment]
    id_ordem_servico integer [unique]       // Execucao (1:1)
    valor numeric(12,2) [not null]
    dt_emissao date [not null]
    dt_vencimento date [not null]
    quilometros numeric(6, 2) [not null]
    horas numeric(5,2) [not null]
    dt_pagamento date
    descricao text
}
Ref execução: servico.id_ordem_servico - ordemservico.id_ordem_servico

Table compatibilidade {                     // Compatibilidade (N:N)
    id_compatibilidade integer [pk, increment]
    id_produto integer [not null]
    id_maquina integer [not null]
}
Ref compatibilidade: compatibilidade.id_produto <> produtos.id_produto
Ref compatibilidade: compatibilidade.id_maquina <> maquina.id_maquina

Table consumocompra {                       // ConsumoCompra (N:N)
    id_consumo_compra integer [pk, increment]
    quantidade integer [not null]
    id_produto integer [not null]
    id_compra integer [not null]
}
Ref consumocompra: consumocompra.id_produto <> produtos.id_produto
Ref consumocompra: consumocompra.id_compra <> compra.id_compra

Table consumoservico {                      // ConsumoServico (N:N)
    id_consumo_servico integer [pk, increment]
    quantidade integer [not null]
    id_produto integer [not null]
    id_servico integer [not null]
}
Ref consumoservico: consumoservico.id_produto <> produtos.id_produto
Ref consumoservico: consumoservico.id_servico <> servico.id_servico
```
