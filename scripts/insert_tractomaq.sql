-- Conecta ao banco de dados tractomaq
\c tractomaq;

-- Inserção de dados na tabela usuario
INSERT INTO usuario (id_usuario, senha, tipo) VALUES
('admin@tractomaq.com', 'admin123', FALSE),
('user1@example.com', 'user1pass', TRUE),
('user2@example.com', 'user2pass', TRUE);

-- Inserção de dados na tabela pessoa
INSERT INTO pessoa (tipo, nome, endereco, telefone, cpf, cnpj, razaosocial) VALUES
(FALSE, 'João Silva', 'Rua A, 123', '49912345678', '11122233344', NULL, NULL),
(TRUE, 'ABC Máquinas Ltda.', 'Av. B, 456', '49987654321', NULL, '11222333000144', 'ABC Maquinas Peças e Serviços Ltda'),
(FALSE, 'Maria Souza', 'Rua C, 789', '49998761234', '55566677788', NULL, NULL),
(TRUE, 'Máquinas Pesadas SA', 'Rodovia D, km 10', '49911223344', NULL, '44555666000177', 'Maquinas Pesadas SA');

-- Inserção de dados na tabela cobranca
INSERT INTO cobranca (dt_emissao, dt_vencimento, dt_pagamento, status_pag, valor) VALUES
('2025-06-01', '2025-07-01', '2025-06-25', 1, 1500.00),
('2025-06-10', '2025-07-10', NULL, 0, 250.50),
('2025-05-01', '2025-05-15', NULL, 2, 75.20),
('2025-06-20', '2025-07-20', NULL, 0, 1200.00);

-- Inserção de dados na tabela maquina
INSERT INTO maquina (nome, descricao) VALUES
('Escavadeira Caterpillar 320', 'Escavadeira hidráulica de médio porte para diversas aplicações.'),
('Trator John Deere 6100J', 'Trator agrícola versátil para preparo de solo e plantio.'),
('Retroescavadeira Case 580N', 'Máquina compacta ideal para pequenas e médias obras.'),
('Motoniveladora Komatsu GD655-6', 'Equipamento para nivelamento de solos em grandes obras.');

-- Inserção de dados na tabela compra
INSERT INTO compra (dt_emissao, dt_vencimento, dt_pagamento, loc_entrega, status_pag, valor, id_pessoa) VALUES
('2025-05-15', '2025-06-15', '2025-06-10', 'Armazém Principal', 1, 5000.00, 2),
('2025-06-05', '2025-07-05', NULL, 'Obra Central', 0, 350.75, 4),
('2025-04-20', '2025-05-20', NULL, 'Depósito Filial', 2, 120.00, 2);

-- Inserção de dados na tabela ordem_servico
INSERT INTO ordem_servico (dt_ordem_servico, local, descricao, id_pessoa) VALUES
('2025-06-05', 'Fazenda São Jorge', 'Serviço de preparo de solo para plantio de milho.', 1),
('2025-06-12', 'Condomínio Residencial Vista Alegre', 'Escavação para fundação de novo bloco.', 3),
('2025-06-18', 'Rodovia Estadual SC-XXX', 'Nivelamento de trecho para recapeamento.', 1);

-- Inserção de dados na tabela servico
INSERT INTO servico (horas, quilometros, descricao, id_ordem_servico, id_cobranca) VALUES
(10.5, 50.2, 'Aração e gradagem de 10 hectares.', 1, 1),
(8.0, 15.0, 'Escavação de valas para tubulação de esgoto.', 2, 2),
(5.0, 30.0, 'Terraplanagem para construção de pátio.', 3, 4),
(2.5, 10.0, 'Remoção de entulho e limpeza de terreno.', 2, NULL);

-- Inserção de dados na tabela produtos
INSERT INTO produtos (nome, quantidade, valor, descricao, categoria, marca) VALUES
('Óleo Hidráulico ISO 46', 50, 85.00, 'Óleo hidráulico de alta performance para máquinas pesadas.', 'Lubrificantes', 'Petrobrás'),
('Filtro de Ar Primário', 20, 120.00, 'Filtro de ar para motores diesel.', 'Filtros', 'Mann Filter'),
('Pneu 18.4-26', 5, 1200.00, 'Pneu para máquinas agrícolas e de construção.', 'Pneus', 'Goodyear'),
('Pastilha de Freio', 30, 45.00, 'Pastilha de freio para sistema de freio a disco.', 'Peças de Freio', 'Fras-le');

-- Inserção de dados na tabela compatibilidade
INSERT INTO compatibilidade (id_produto, id_maquina) VALUES
(1, 1),
(1, 2),
(1, 3),
(2, 1),
(2, 2),
(3, 2),
(4, 3);

-- Inserção de dados na tabela consumocompra
INSERT INTO consumocompra (quantidade, id_produto, id_compra) VALUES
(10, 1, 1),
(5, 2, 1),
(2, 3, 2),
(15, 4, 3);

-- Inserção de dados na tabela consumoservico
INSERT INTO consumoservico (quantidade, id_produto, id_servico) VALUES
(5, 1, 1),
(1, 2, 1),
(2, 4, 2),
(3, 1, 3);