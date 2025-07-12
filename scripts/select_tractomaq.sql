-- Acessando o banco de dados: tractomaq
\c tractomaq

-- Exibindo todas as tabelas
\dt

-- Exibindo os dados de cada tabela
SELECT * FROM usuario LIMIT 1; 
SELECT * FROM pessoa LIMIT 1; 
SELECT * FROM produtos LIMIT 1; 
SELECT * FROM maquina LIMIT 1; 
SELECT * FROM compra LIMIT 1; 
SELECT * FROM ordemservico LIMIT 1; 
SELECT * FROM servico LIMIT 1; 
SELECT * FROM compatibilidade LIMIT 1; 
SELECT * FROM consumocompra LIMIT 1; 
SELECT * FROM consumoservico LIMIT 1; 
