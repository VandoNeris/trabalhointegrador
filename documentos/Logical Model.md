### Conversão Lógico - Conceitual

pessoa (
    <u>codigo</u>, 
    tipo, 
    nome, 
    ender, 
    <u style="text-decoration: underline dashed;">cpf*</u>,
    <u style="text-decoration: underline dashed;">cnpj*</u>,
    <u style="text-decoration: underline dashed;">razaosocial</u>
)

ordemserv (
    <u>codigo</u>,
    data,
    local,
    descricao,
    codpessoa(pessoa)           <!-- Registra (1:N) -->
)

servico (
    <u>codigo</u>,
    horas,
    quilometros,
    descricao,
    codordemserv(ordemserv),    <!-- Execução (1:N) -->
    codcobranca(cobranca)       <!-- Gera (1:N) -->
)

cobranca (
    <u>codigo</u>,
    dtemissao,
    dtvalidade,
    dtfinal,
    statuspag,
    valorfinal,
    descontos
)

produto (
    <u>codigo</u>,
    nome,
    quantidade,
    condicao,
    valor,
    descricao,
    categoria,
    marca
    codservico(servico),        <!-- Consome (1:N) -->
)

funcionamento (                 <!-- Funcionamento (N:N) -->
    <u>codigo</u>,
    codproduto(produto),
    codmaquina(maquina), 
)

consumo (                       <!-- Consome (N:N) -->
    <u>codigo</u>,
    codproduto(produto),
    codcompra(compra),
)

maquina (
    <u>codigo</u>,
    nome,
    descricao
)

compra (
    <u>codigo</u>,
    dtemissao,
    dtvalidade,
    dtfinal,
    locentrega,
    codpessoa(pessoa)           <!-- Registra (1:N) -->
)


### Modelo Lógico Relacional - Traqtomac

#### Link dbdiagram: [https://dbdiagram.io/d/Traqtomac-6862e705f413ba350896d9cf]

```
Project project_name {
  database_type: 'PostgreSQL'
  Note: 'Traqtomac'
}

Table pessoa {
    id_pessoa integer [pk, increment]
    tipo integer [not null, note:'0-Fisica\n1-Juridica']
    nome varchar(50) [not null]
    ender varchar(100) [not null]
    cpf varchar(11) [unique]
    cnpj varchar(14) [unique]
    razaosocial varchar(20)
}

Table ordem_servico {
    id_os integer [pk, increment]
    dt_os date [not null]
    local varchar(100) [not null]
    descricao text [not null]
    id_pessoa integer [not null]    // Registra (1:N)
}
Ref: ordem_servico.id_pessoa > pessoa.id_pessoa

Table servico {
    id_servico integer [pk, increment]
    horas decimal(2,2) [not null]
    quilometros decimal(10, 2) [not null]
    descricao text [not null]
    id_os integer [not null]        // Execução (1:N)
    id_cobranca integer [not null]  // Gera (1:N)
}
Ref: servico.id_os > ordem_servico.id_os
Ref: servico.id_cobranca > cobranca.id_cobranca

Table cobranca {
    id_cobranca integer [pk, increment]
    dt_emissao date [not null]
    dt_validade date [not null]
    dt_final date [not null]
    status_pag integer [not null, note:'0-Pendente\n1-Pago\n2-Cancelado']
    valor_final decimal(10,2) [not null]
    descontos decimal(10,2) [not null]
}

Table produto {
    id_produto integer [pk, increment]
    nome varchar(50) [not null]
    quantidade integer [not null]
    condicao integer [not null, note:'0-Pessimo\n1-Mediano\n2-Excelente']
    valor decimal(10,2) [not null]
    descricao text [not null]
    categoria varchar(20) [not null]
    marca varchar(20) [not null]
    id_servico integer [not null]   // Consome (1:N)
}
Ref: produto.id_servico > servico.id_servico

Table funcionamento {               // Funcionamento (N:N)
    id_funcionamento integer [pk, increment]
    id_produto integer [not null]
    id_maquina integer [not null]
}
Ref: funcionamento.id_produto <> produto.id_produto
Ref: funcionamento.id_maquina <> maquina.id_maquina

Table consumocompra {               // Consome (N:N)
    id_consumoc integer [pk, increment]
    id_produto integer [not null]
    id_compra integer [not null]
}
Ref: consumocompra.id_produto <> produto.id_produto
Ref: consumocompra.id_compra <> compra.id_compra

Table maquina {
    id_maquina integer [pk, increment]
    nome varchar(50) [not null]
    descricao text [not null]
}

Table compra {
    id_compra integer [pk, increment]
    dt_emissao date [not null]
    dt_validade date [not null]
    dt_final date [not null]
    loc_entrega varchar(100) [not null]
    id_pessoa integer [not null]   // Registra (1:N)
}
Ref: compra.id_pessoa > pessoa.id_pessoa
```
