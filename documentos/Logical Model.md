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
    <u style="text-decoration: underline dashed;">descricao</u>,
    codpessoa(pessoa)           <!-- RegistraOS (1:N) -->
)

servico (
    <u>codigo</u>,
    horas,
    quilometros,
    <u style="text-decoration: underline dashed;">descricao</u>,
    codordemserv(ordemserv),    <!-- Execução (1:N) -->
    codcobranca(cobranca)       <!-- Gera (1:N) -->
)

cobranca (
    <u>codigo</u>,
    dtemissao,
    dtvalidade,
    <u style="text-decoration: underline dashed;">dtfinal</u>,
    statuspag,
    valorfinal
)

produtos (
    <u>codigo</u>,
    nome,
    quantidade,
    condicao,
    valor,
    <u style="text-decoration: underline dashed;">descricao</u>,
    categoria,
    marca
)

compatibilidade (                 <!-- Compatibilidade (N:N) -->
    <u>codigo</u>,
    codprodutos(produtos),
    codmaquina(maquina)
)

consumocompra (                       <!-- ConsumoCompra (N:N) -->
    <u>codigo</u>,
    codprodutos(produtos),
    codcompra(compra)
)

consumoservico (                      <!-- ConsumoServico (N:N) -->
    <u>codigo</u>,
    codprodutos(produtos),
    codservico(servico)
)

maquina (
    <u>codigo</u>,
    nome,
    <u style="text-decoration: underline dashed;">descricao</u>
)

compra (
    <u>codigo</u>,
    dtemissao,
    dtvalidade,
    <u style="text-decoration: underline dashed;">dtfinal</u>,
    locentrega,
    codpessoa(pessoa)           <!-- RegistraCompra (1:N) -->
)


### Modelo Lógico Relacional - Tractomaq

**Link dbdiagram: [https://dbdiagram.io/d/Tractomaq-6862e705f413ba350896d9cf]**

```
Project project_name {
  database_type: 'PostgreSQL'
  Note: 'Tractomaq'
}

Table pessoa {
    id_pessoa integer [pk, increment]
    tipo boolean [not null, note:'0-Fisica\n1-Juridica']
    nome varchar(60) [not null]
    ender varchar(100) [not null]
    cpf varchar(11) [unique]
    cnpj varchar(14) [unique]
    razaosocial varchar(60)
}

Table ordem_servico {
    id_os integer [pk, increment]
    dt_os date [not null]
    local varchar(100) [not null]
    descricao text
    id_pessoa integer [not null]    // RegistraOS (1:N)
}
Ref registraordemservico: ordem_servico.id_pessoa > pessoa.id_pessoa

Table servico {
    id_servico integer [pk, increment]
    horas numeric(4,2) [not null]
    quilometros numeric(6, 2) [not null]
    descricao text
    id_os integer [not null]        // Execução (1:N)
    id_cobranca integer [not null]  // Gera (1:N)
}
Ref execução: servico.id_os > ordem_servico.id_os
Ref gera: servico.id_cobranca > cobranca.id_cobranca

Table cobranca {
    id_cobranca integer [pk, increment]
    dt_emissao date [not null]
    dt_validade date [not null]
    dt_final date
    status_pag boolean [not null, note:'0-Pendente\n1-Pago']
    valor_final numeric(12,2) [not null]
}

Table produtos {
    id_produtos integer [pk, increment]
    nome varchar(60) [not null]
    quantidade integer [not null]
    condicao integer [not null, note:'0-Pessimo\n1-Mediano\n2-Excelente']
    valor numeric(12,2) [not null]
    descricao text
    categoria varchar(60) [not null]
    marca varchar(60) [not null]
}

Table compatibilidade {               // Compatibilidade (N:N)
    id_compatibilidade integer [pk, increment]
    id_produtos integer [not null]
    id_maquina integer [not null]
}
Ref compatibilidade: compatibilidade.id_produtos <> produtos.id_produtos
Ref compatibilidade: compatibilidade.id_maquina <> maquina.id_maquina

Table consumocompra {               // ConsumoCompra (N:N)
    id_consumocompra integer [pk, increment]
    id_produtos integer [not null]
    id_compra integer [not null]
}
Ref consumocompra: consumocompra.id_produtos <> produtos.id_produtos
Ref consumocompra: consumocompra.id_compra <> compra.id_compra

Table consumoservico {              // ConsumoServico (N:N)
    id_consumoservico integer [pk, increment]
    id_produtos integer [not null]
    id_servico integer [not null]
}
Ref consumoservico: consumoservico.id_produtos <> produtos.id_produtos
Ref consumoservico: consumoservico.id_servico <> servico.id_servico

Table maquina {
    id_maquina integer [pk, increment]
    nome varchar(60) [not null]
    descricao text
}

Table compra {
    id_compra integer [pk, increment]
    dt_emissao date [not null]
    dt_validade date [not null]
    dt_final date
    loc_entrega varchar(100) [not null]
    id_pessoa integer [not null]   // RegistraCompra (1:N)
}
Ref registracompra: compra.id_pessoa > pessoa.id_pessoa
```
