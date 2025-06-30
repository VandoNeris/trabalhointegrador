CREATE TABLE "pessoa" (
  "id" varchar PRIMARY KEY DEFAULT (uuid()),
  "nome" varchar NOT NULL,
  "email" varchar,
  "endereco" varchar,
  "telefone" varchar,
  "tipo_pessoa" varchar,
  "cpf" varchar UNIQUE,
  "cnpj" varchar UNIQUE,
  "created_at" datetime DEFAULT (now()),
  "updated_at" datetime DEFAULT (now())
);

CREATE TABLE "ordem_servico" (
  "codigo" varchar PRIMARY KEY DEFAULT (uuid()),
  "data" datetime NOT NULL,
  "local" varchar,
  "descricao" text,
  "pessoa_id" varchar NOT NULL,
  "created_at" datetime DEFAULT (now()),
  "updated_at" datetime DEFAULT (now())
);

CREATE TABLE "compra" (
  "codigo" varchar PRIMARY KEY DEFAULT (uuid()),
  "data_emissao" datetime NOT NULL,
  "data_validade" datetime,
  "local_entrega" varchar,
  "data_final" datetime,
  "created_at" datetime DEFAULT (now()),
  "updated_at" datetime DEFAULT (now())
);

CREATE TABLE "produto" (
  "codigo" varchar PRIMARY KEY DEFAULT (uuid()),
  "nome" varchar NOT NULL,
  "quantidade" integer NOT NULL,
  "valor" decimal(10,2) NOT NULL,
  "descricao" text,
  "categoria" varchar,
  "marca" varchar,
  "created_at" datetime DEFAULT (now()),
  "updated_at" datetime DEFAULT (now())
);

CREATE TABLE "maquina" (
  "codigo" varchar PRIMARY KEY DEFAULT (uuid()),
  "nome" varchar NOT NULL,
  "descricao" text,
  "created_at" datetime DEFAULT (now()),
  "updated_at" datetime DEFAULT (now())
);

CREATE TABLE "servico" (
  "codigo" varchar PRIMARY KEY DEFAULT (uuid()),
  "horas" decimal(5,2),
  "quilometros" decimal(10,2),
  "descricao" text,
  "created_at" datetime DEFAULT (now()),
  "updated_at" datetime DEFAULT (now())
);

CREATE TABLE "cobranca" (
  "codigo" varchar PRIMARY KEY DEFAULT (uuid()),
  "data_emissao" datetime NOT NULL,
  "data_validade" datetime,
  "data_final" datetime,
  "status_pagamento" varchar NOT NULL,
  "valor_final" decimal(10,2) NOT NULL,
  "desconto" decimal(10,2) DEFAULT 0,
  "created_at" datetime DEFAULT (now()),
  "updated_at" datetime DEFAULT (now())
);

CREATE TABLE "compra_produto" (
  "id" varchar PRIMARY KEY DEFAULT (uuid()),
  "compra_codigo" varchar,
  "produto_codigo" varchar,
  "quantidade" integer NOT NULL,
  "valor_unitario" decimal(10,2) NOT NULL
);

CREATE TABLE "ordem_servico_maquina" (
  "id" varchar PRIMARY KEY DEFAULT (uuid()),
  "ordem_servico_codigo" varchar,
  "maquina_codigo" varchar,
  "horas_utilizadas" decimal(5,2)
);

CREATE TABLE "ordem_servico_servico" (
  "id" varchar PRIMARY KEY DEFAULT (uuid()),
  "ordem_servico_codigo" varchar,
  "servico_codigo" varchar
);

CREATE TABLE "cobranca_ordem_servico" (
  "id" varchar PRIMARY KEY DEFAULT (uuid()),
  "cobranca_codigo" varchar,
  "ordem_servico_codigo" varchar
);

COMMENT ON COLUMN "pessoa"."tipo_pessoa" IS 'fisica ou juridica';

COMMENT ON COLUMN "cobranca"."status_pagamento" IS 'pendente, pago, vencido, cancelado';

ALTER TABLE "ordem_servico" ADD FOREIGN KEY ("pessoa_id") REFERENCES "pessoa" ("id");

ALTER TABLE "compra_produto" ADD FOREIGN KEY ("compra_codigo") REFERENCES "compra" ("codigo");

ALTER TABLE "compra_produto" ADD FOREIGN KEY ("produto_codigo") REFERENCES "produto" ("codigo");

ALTER TABLE "ordem_servico_maquina" ADD FOREIGN KEY ("ordem_servico_codigo") REFERENCES "ordem_servico" ("codigo");

ALTER TABLE "ordem_servico_maquina" ADD FOREIGN KEY ("maquina_codigo") REFERENCES "maquina" ("codigo");

ALTER TABLE "ordem_servico_servico" ADD FOREIGN KEY ("ordem_servico_codigo") REFERENCES "ordem_servico" ("codigo");

ALTER TABLE "ordem_servico_servico" ADD FOREIGN KEY ("servico_codigo") REFERENCES "servico" ("codigo");

ALTER TABLE "cobranca_ordem_servico" ADD FOREIGN KEY ("cobranca_codigo") REFERENCES "cobranca" ("codigo");

ALTER TABLE "cobranca_ordem_servico" ADD FOREIGN KEY ("ordem_servico_codigo") REFERENCES "ordem_servico" ("codigo");
