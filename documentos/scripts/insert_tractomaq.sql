-- Pessoas físicas e jurídicas
INSERT INTO pessoa (tipo, nome, ender, cpf)
VALUES 
  (FALSE, 'João da Silva', 'Rua das Palmeiras, 100', '12345678901'),
  (FALSE, 'Maria Oliveira', 'Rua das Acácias, 300', '98765432100');
INSERT INTO pessoa (tipo, nome, ender, cnpj, razaosocial)
VALUES 
  (TRUE, 'TratorMaq Ltda.', 'Av. Industrial, 500', '12345678000199', 'TratorMaq Equipamentos'),
  (TRUE, 'AgroForte S/A', 'Rodovia BR-101, Km 45', '22334455000188', 'AgroForte S/A');

-- Cobranças
INSERT INTO cobranca (dt_emissao, dt_validade, dt_final, status_pag, valor_final)
VALUES 
  ('2025-06-01', '2025-06-10', NULL, 0, 1500.00),
  ('2025-06-05', '2025-06-15', '2025-06-14', 1, 2300.00),
  ('2025-06-10', '2025-06-20', NULL, 0, 980.00),
  ('2025-06-12', '2025-06-22', '2025-06-21', 1, 1890.00);

-- Máquinas
INSERT INTO maquina (nome, descricao)
VALUES 
  ('Trator X500', 'Trator agrícola de médio porte'),
  ('Colheitadeira Z1000', 'Colheitadeira com motor de 300cv'),
  ('Plantadeira R300', 'Plantadeira de 12 linhas com GPS');

-- Compras
INSERT INTO compra (dt_emissao, dt_validade, dt_final, loc_entrega, id_pessoa)
VALUES 
  ('2025-06-01', '2025-06-10', NULL, 'Armazém Central', 3),
  ('2025-06-02', '2025-06-12', '2025-06-10', 'Fazenda Boa Vista', 1),
  ('2025-06-07', '2025-06-17', NULL, 'Depósito AgroForte', 4);

-- Ordens de serviço
INSERT INTO ordem_servico (dt_os, local, descricao, id_pessoa)
VALUES 
  ('2025-06-03', 'Oficina TratorMaq', 'Manutenção preventiva', 3),
  ('2025-06-04', 'Fazenda São José', 'Reparo no sistema hidráulico', 1),
  ('2025-06-11', 'Oficina Central', 'Atualização de software e troca de peças', 4);

-- Serviços
INSERT INTO servico (horas, quilometros, descricao, id_os, id_cobranca)
VALUES 
  (3.5, 15.2, 'Troca de óleo e filtros', 1, 1),
  (5.0, 23.0, 'Reparo completo no sistema hidráulico', 2, 2),
  (2.0, 10.0, 'Revisão geral', 3, 3),
  (4.5, 18.0, 'Atualização do módulo eletrônico e substituição de sensor', 3, 4);

-- Produtos
INSERT INTO produtos (nome, quantidade, condicao, valor, descricao, categoria, marca)
VALUES 
  ('Filtro de óleo', 50, 2, 30.00, 'Filtro para trator série X', 'Filtros', 'AgroParts'),
  ('Mangueira hidráulica', 20, 1, 120.00, 'Mangueira resistente a alta pressão', 'Hidráulica', 'Hidron'),
  ('Sensor de rotação', 15, 2, 450.00, 'Sensor para sistema eletrônico', 'Eletrônica', 'TractoTec'),
  ('Óleo lubrificante', 100, 2, 25.00, 'Óleo mineral 15W40', 'Lubrificantes', 'MaxOil'),
  ('Módulo eletrônico', 10, 1, 890.00, 'Central eletrônica de controle', 'Eletrônica', 'AgroChip'),
  ('Correia dentada', 30, 2, 65.00, 'Correia reforçada para motor diesel', 'Transmissão', 'BeltMax');

-- Compatibilidades
INSERT INTO compatibilidade (id_produto, id_maquina)
VALUES 
  (1, 1), -- Filtro com Trator
  (2, 2), -- Mangueira com Colheitadeira
  (3, 2), -- Sensor com Colheitadeira
  (4, 1), -- Óleo com Trator
  (5, 3), -- Módulo com Plantadeira
  (6, 1); -- Correia com Trator

-- Produtos usados em compras
INSERT INTO consumocompra (id_produto, id_compra)
VALUES 
  (1, 1),
  (2, 2),
  (4, 1),
  (5, 3),
  (6, 3);

-- Produtos usados em serviços
INSERT INTO consumoservico (id_produto, id_servico)
VALUES 
  (1, 1),
  (2, 1),
  (4, 1),
  (3, 4),
  (5, 4),
  (6, 2);
