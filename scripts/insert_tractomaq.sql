-- Acessando o banco de dados: tractomaq
\c tractomaq

-- Populando usuario (6 entradas)
INSERT INTO usuario (nome, senha, tipo) VALUES
('admin', 'senha123', 0),
('joao', 'senha123', 1),
('maria', 'senha123', 1),
('carlos', 'senha123', 1),
('ana', 'senha123', 1),
('pedro', 'senha123', 1);

-- Populando pessoa (8 entradas)
INSERT INTO pessoa (tipo, nome, endereco, telefone, email, cpf, cnpj, razao_social) VALUES
(0, 'João Silva', 'Rua A, 123', '11999990001', 'joao@email.com', '12345678901', NULL, NULL),
(0, 'Maria Souza', 'Rua B, 456', '11999990002', 'maria@email.com', '23456789012', NULL, NULL),
(0, 'Carlos Lima', 'Rua C, 789', '11999990003', 'carlos@email.com', '34567890123', NULL, NULL),
(0, 'Ana Paula', 'Rua D, 101', '11999990004', 'ana@email.com', '45678901234', NULL, NULL),
(1, 'Tracto LTDA', 'Av. Industrial, 333', '1122223333', 'contato@tracto.com', NULL, '12345678000199', 'Tracto Máquinas LTDA'),
(1, 'AgroTools S/A', 'Av. Campo, 456', '1133344444', 'suporte@agrotools.com', NULL, '22345678000199', 'AgroTools Soluções'),
(1, 'TecAgro Equipamentos', 'Rua Tratores, 88', '1144455555', 'vendas@tecagro.com', NULL, '32345678000199', 'TecAgro Ltda'),
(1, 'AgroMais Brasil', 'Rodovia 101', '1155566666', 'contato@agromais.com', NULL, '42345678000199', 'AgroMais Brasil S/A');

-- Populando produtos (8 entradas)
INSERT INTO produtos (nome, quantidade, valor_uni, descricao, categoria, marca) VALUES
('Filtro de óleo', 100, 45.90, 'Filtro para tratores pequenos', 'Peças', 'Tracto'),
('Pneu agrícola', 50, 890.00, 'Pneu para trator médio', 'Rodas', 'Firestone'),
('Correia dentada', 200, 75.00, 'Correia universal', 'Transmissão', 'Gates'),
('Bateria 150Ah', 30, 580.00, 'Bateria para tratores grandes', 'Elétrica', 'Moura'),
('Óleo hidráulico', 300, 120.00, 'Óleo para sistemas hidráulicos', 'Lubrificantes', 'Lubrax'),
('Embreagem', 20, 1300.00, 'Kit de embreagem completo', 'Transmissão', 'Valtra'),
('Radiador', 15, 950.00, 'Radiador para motor diesel', 'Refrigeração', 'Case IH'),
('Filtro de ar', 100, 39.00, 'Filtro de ar para colheitadeira', 'Peças', 'New Holland');

-- Populando maquina (6 entradas)
INSERT INTO maquina (nome, descricao) VALUES
('Trator MF 290', 'Trator médio agrícola'),
('Colheitadeira JD S550', 'Colheitadeira de grãos'),
('Plantadeira Baldan', 'Equipamento de plantio'),
('Pulverizador Jacto', 'Pulverizador autopropelido'),
('Trator Valtra A750', 'Trator compacto'),
('Colhedora Cana', 'Máquina para corte de cana');

-- Populando compra (10 entradas)
INSERT INTO compra (loc_entrega, valor, dt_emissao, dt_vencimento, dt_entrega, dt_pagamento, id_pessoa) VALUES
('Centro de Distribuição', 1200.00, '2025-06-01', '2025-06-10', '2025-06-05', '2025-06-10', 5),
('Fazenda Rio Azul', 850.00, '2025-06-02', '2025-06-12', '2025-06-07', '2025-06-12', 6),
('Fazenda Boa Vista', 3300.00, '2025-06-03', '2025-06-15', '2025-06-10', '2025-06-15', 7),
('Armazém Central', 2200.00, '2025-06-04', '2025-06-14', '2025-06-08', '2025-06-14', 8),
('Oficina do Zé', 670.00, '2025-06-05', '2025-06-13', '2025-06-09', '2025-06-13', 1),
('Depósito Rural', 950.00, '2025-06-06', '2025-06-16', '2025-06-11', '2025-06-16', 2),
('Tratores do Sul', 1570.00, '2025-06-07', '2025-06-17', '2025-06-12', '2025-06-17', 3),
('Auto Peças Sul', 760.00, '2025-06-08', '2025-06-18', '2025-06-13', '2025-06-18', 4),
('Fazenda Luz Divina', 2000.00, '2025-06-09', '2025-06-19', '2025-06-14', '2025-06-19', 5),
('Serviços Gerais LTDA', 1110.00, '2025-06-10', '2025-06-20', '2025-06-15', '2025-06-20', 1);

-- Populando ordemservico (12 entradas)
INSERT INTO ordemservico (dt_servico, loc_servico, descricao, id_pessoa) VALUES
('2025-06-01', 'Fazenda Primavera', 'Revisão geral', 1),
('2025-06-02', 'Fazenda Boa Terra', 'Troca de óleo e filtros', 2),
('2025-06-03', 'Fazenda Esperança', 'Ajustes na transmissão', 3),
('2025-06-04', 'Fazenda Paraíso', 'Instalação de faróis', 4),
('2025-06-05', 'Fazenda Real', 'Troca de embreagem', 5),
('2025-06-06', 'Fazenda Verde', 'Limpeza de radiador', 6),
('2025-06-07', 'Fazenda do Vale', 'Substituição de correia', 7),
('2025-06-08', 'Fazenda Nova Era', 'Verificação elétrica', 8),
('2025-06-09', 'Fazenda Horizonte', 'Ajuste de sensores', 1),
('2025-06-10', 'Fazenda Luz Divina', 'Manutenção geral', 2),
('2025-06-11', 'Fazenda do Sol', 'Inspeção preventiva', 3),
('2025-06-12', 'Fazenda Boa Fé', 'Reparo em motor', 4);

-- Populando servico (10 entradas)
INSERT INTO servico (id_ordem_servico, valor, dt_emissao, dt_vencimento, quilometros, horas, dt_pagamento, descricao) VALUES
(1, 600.00, '2025-06-01', '2025-06-05', 12.0, 2.5, '2025-06-05', 'Revisão básica'),
(2, 450.00, '2025-06-02', '2025-06-06', 8.0, 1.5, '2025-06-06', 'Troca de óleo e filtros'),
(3, 900.00, '2025-06-03', '2025-06-07', 15.5, 3.0, '2025-06-07', 'Transmissão'),
(4, 250.00, '2025-06-04', '2025-06-08', 6.0, 1.0, '2025-06-08', 'Faróis'),
(5, 1300.00, '2025-06-05', '2025-06-09', 20.0, 4.0, '2025-06-09', 'Embreagem'),
(6, 380.00, '2025-06-06', '2025-06-10', 10.0, 1.2, '2025-06-10', 'Radiador'),
(7, 190.00, '2025-06-07', '2025-06-11', 4.5, 0.8, '2025-06-11', 'Correia'),
(8, 410.00, '2025-06-08', '2025-06-12', 7.0, 1.3, '2025-06-12', 'Elétrica'),
(9, 220.00, '2025-06-09', '2025-06-13', 5.0, 1.1, '2025-06-13', 'Sensores'),
(10, 1000.00, '2025-06-10', '2025-06-14', 18.0, 3.5, '2025-06-14', 'Serviço completo');

-- Populando compatibilidade (8 entradas)
INSERT INTO compatibilidade (id_produto, id_maquina) VALUES
(1, 1),
(2, 1),
(3, 2),
(4, 2),
(5, 3),
(6, 3),
(7, 4),
(8, 5);

-- Populando consumocompra (12 entradas)
INSERT INTO consumocompra (quantidade, id_produto, id_compra) VALUES
(2, 1, 1),
(1, 2, 2),
(3, 3, 3),
(1, 4, 4),
(5, 5, 5),
(1, 6, 6),
(2, 7, 7),
(4, 8, 8),
(1, 2, 9),
(2, 4, 10),
(3, 1, 1),
(1, 5, 2);

-- Populando consumoservico (12 entradas)
INSERT INTO consumoservico (quantidade, id_produto, id_servico) VALUES
(1, 1, 1),
(1, 2, 2),
(1, 3, 3),
(1, 4, 4),
(1, 5, 5),
(1, 6, 6),
(1, 7, 7),
(1, 8, 8),
(1, 1, 9),
(1, 2, 10),
(1, 3, 1),
(1, 4, 2);
