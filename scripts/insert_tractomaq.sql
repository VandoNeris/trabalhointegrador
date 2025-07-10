-- Conecta ao banco de dados tractomaq
\c tractomaq;

-- Inserção de usuários
INSERT INTO usuario (id_usuario, senha, tipo) VALUES
('admin1', 'senha123', FALSE),
('user1', 'senha123', TRUE),
('user2', 'senha123', TRUE);

-- Inserção de pessoas
INSERT INTO pessoa (tipo, nome, endereco, email, telefone, cpf, cnpj, razaosocial) VALUES
(FALSE, 'João da Silva', 'Rua A, 100', 'joao@email.com', '11999990000', '12345678901', NULL, NULL),
(FALSE, 'Felipe Rocha', 'Rua E, 500', 'felipe@email.com', '11999990004', '12345678905', NULL, NULL),
(TRUE, 'MaqTools Ltda', 'Av I, 1300', 'maq@tools.com', '11333330003', NULL, '12345678000104', 'MaqTools Ltda'),
(FALSE, 'Carlos Lima', 'Rua C, 300', 'carlos@email.com', '11999990002', '12345678903', NULL, NULL),
(TRUE, 'TratorTech LTDA', 'Av F, 1000', 'contato@trator.com', '11333330000', NULL, '12345678000101', 'TratorTech LTDA'),
(FALSE, 'Ana Paula', 'Rua D, 400', 'ana@email.com', '11999990003', '12345678904', NULL, NULL),
(TRUE, 'AgroMáquinas SA', 'Av G, 1100', 'agro@maq.com', '11333330001', NULL, '12345678000102', 'AgroMáquinas SA'),
(TRUE, 'RuralPro ME', 'Av H, 1200', 'vendas@ruralpro.com', '11333330002', NULL, '12345678000103', 'RuralPro ME'),
(TRUE, 'CampoForte', 'Av J, 1400', 'suporte@campoforte.com', '11333330004', NULL, '12345678000105', 'CampoForte SA'),
(FALSE, 'Maria Souza', 'Rua B, 200', 'maria@email.com', '11999990001', '12345678902', NULL, NULL);

-- Inserção de máquinas
INSERT INTO maquina (nome, descricao) VALUES
('Trator X100', 'Trator agrícola de pequeno porte'),
('Colheitadeira Z200', 'Ideal para grãos finos'),
('Plantadeira P300', 'Equipamento para plantio de precisão'),
('Niveladora F70', 'Correção de terrenos agrícolas');

-- Inserção de produtos
INSERT INTO produtos (nome, quantidade, valor, descricao, categoria, marca) VALUES
('Filtro de Óleo', 50, 30.00, 'Filtro para trator', 'Peça', 'TratorTech'),
('Correia V', 100, 15.00, 'Correia de borracha', 'Peça', 'AgroPart'),
('Pneu Agrícola 18.4-30', 20, 1200.00, 'Pneu para colheitadeira', 'Pneu', 'Goodyear'),
('Sensor de Umidade', 30, 250.00, 'Sensor eletrônico', 'Eletrônico', 'SensAgro'),
('Bico Pulverizador', 150, 5.00, 'Peça para pulverizador', 'Peça', 'SprayMaster'),
('Óleo Lubrificante', 80, 60.00, 'Óleo sintético', 'Lubrificante', 'Shell'),
('Válvula de Pressão', 40, 75.00, 'Válvula de controle', 'Peça', 'HydroControl'),
('Filtro de Ar', 60, 40.00, 'Filtro para motor', 'Peça', 'TratorTech'),
('Cilindro Hidráulico', 25, 900.00, 'Cilindro de elevação', 'Hidráulico', 'PowerLift'),
('Bateria 12V', 35, 300.00, 'Bateria para máquinas', 'Elétrico', 'Bosch');

-- Inserção de cobranças
INSERT INTO cobranca (dt_emissao, dt_vencimento, dt_pagamento, status_pag, valor) VALUES
('2025-07-01', '2025-07-08', '2025-07-07', 1, 120000.00),
('2025-07-01', '2025-07-10', NULL, 0, 30000.00),
('2025-07-02', '2025-07-22', '2025-07-20', 1, 2700000.00),
('2025-07-05', '2025-07-15', '2025-07-10', 1, 180000.00),
('2025-07-09', '2025-07-19', NULL, 2, 10000.00);

-- Inserção de compras
INSERT INTO compra (dt_emissao, dt_vencimento, dt_pagamento, loc_entrega, status_pag, valor, id_pessoa) VALUES
('2025-07-01', '2025-07-10', '2025-07-02', 'Galpão Central', 1, 60000.00, 10),
('2025-07-03', '2025-07-13', '2025-07-05', 'Portal Belo', 1, 18000.00, 3),
('2025-07-04', '2025-07-14', '2025-07-14', 'Matriz', 1, 90000.00, 9),
('2025-07-05', '2025-07-15', NULL, 'Campo Norte', 2, 32000.00, 3),
('2025-07-07', '2025-07-17', '2025-07-16', 'Filial Sul', 1, 24000.00, 7);

-- Inserção de ordens de serviço
INSERT INTO ordemservico (dt_ordemservico, local, descricao, id_pessoa) VALUES
('2025-07-01', 'Sítio São João', 'Revisão completa de trator', 10),
('2025-07-02', 'Fazenda Boa Vista', 'Troca de peças na colheitadeira', 2),
('2025-07-03', 'Sítio Maravilha', 'Manutenção corretiva', 3),
('2025-07-04', 'Fazenda Esperança', 'Verificação elétrica', 9),
('2025-07-05', 'Chácara Bela Vista', 'Instalação de GPS agrícola', 3),
('2025-07-06', 'Fazenda Piucco', 'Troca de filtros', 1),
('2025-07-07', 'Sítio da Vó', 'Lubrificação de implementos', 2),
('2025-07-08', 'Estância Nova', 'Substituição de correias', 3),
('2025-07-09', 'Campo Verde', 'Ajuste de sensor de umidade', 7),
('2025-07-10', 'Fazenda Sul', 'Substituição de baterias', 5);

-- Inserção de serviços
INSERT INTO servico (horas, quilometros, descricao, id_ordemservico, id_cobranca) VALUES
(2.5, 100.0, 'Troca de óleo e filtros', 1, 1),
(1.0, 50.0, 'Troca de correias', 2, 3),
(3.0, 80.5, 'Instalação elétrica', 3, 3),
(4.0, 200.0, 'Manutenção de motor', 4, 2),
(2.5, 15.0, 'Instalação de sensor', 5, 1),
(1.2, 60.0, 'Lubrificação geral', 6, 5),
(3.3, 120.5, 'Reparo hidráulico', 7, 3),
(2.0, 90.0, 'Verificação geral', 8, 1),
(2.7, 104.0, 'Troca de bico', 9, 4),
(1.8, 70.5, 'Troca de bateria', 10, 4);

-- Inserção em consumocompra (combinação entre produtos e compras)
INSERT INTO consumocompra (quantidade, id_produto, id_compra) VALUES
(2, 1, 1), (1, 2, 5), (3, 3, 2), (1, 4, 5), (2, 5, 5),
(4, 6, 3), (1, 7, 2), (2, 8, 1), (2, 9, 5), (1, 10, 4);

-- Inserção em consumoservico (combinação entre produtos e serviços)
INSERT INTO consumoservico (quantidade, id_produto, id_servico) VALUES
(1, 1, 1), (2, 2, 2), (1, 4, 3), (1, 5, 4), (3, 6, 5),
(2, 7, 6), (1, 8, 7), (1, 9, 8), (1, 10, 9), (2, 1, 10);

-- Inserção em compatibilidade (combinação entre produtos e máquinas)
INSERT INTO compatibilidade (id_produto, id_maquina) VALUES
(1, 1), (2, 2), (3, 2), (4, 2), (5, 4), (6, 1), (7, 3), (8, 1), (9, 2), (10, 1);
