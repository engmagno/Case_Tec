-- Criando as tabelas com estrutura ampliada
CREATE TABLE clientes (
    id_cliente SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    email VARCHAR(100),
    telefone VARCHAR(20),
    data_cadastro DATE NOT NULL,
    cidade VARCHAR(50),
    uf CHAR(2),
    segmento VARCHAR(50),
    tamanho_empresa VARCHAR(20)
);

CREATE TABLE produtos (
    id_produto SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    categoria VARCHAR(50) NOT NULL,
    subcategoria VARCHAR(50),
    preco NUMERIC(10,2) NOT NULL,
    fornecedor VARCHAR(100)
);

CREATE TABLE pedidos (
    id_pedido SERIAL PRIMARY KEY,
    data_pedido DATE NOT NULL,
    valor_total NUMERIC(12,2) NOT NULL,
    id_cliente INT REFERENCES clientes(id_cliente),
    status_pedido VARCHAR(20),
    forma_pagamento VARCHAR(30)
);

CREATE TABLE itens_pedido (
    id_item SERIAL PRIMARY KEY,
    id_pedido INT REFERENCES pedidos(id_pedido),
    id_produto INT REFERENCES produtos(id_produto),
    quantidade INT NOT NULL,
    preco_unitario NUMERIC(10,2) NOT NULL
);

-- Inserção de clientes com dados completos
INSERT INTO clientes (nome, email, telefone, data_cadastro, cidade, uf, segmento, tamanho_empresa) VALUES
('Agropecuária São Lucas', 'contato@saolucas.com.br', '(11) 98765-4321', '2024-01-05', 'São Paulo', 'SP', 'Agricultura', 'Médio'),
('Grãos do Cerrado LTDA', 'vendas@graoscerrado.com', '(61) 99876-5432', '2024-01-10', 'Brasília', 'DF', 'Comércio', 'Grande'),
('Transportes Oliveira', 'faleconosco@transoliveira.com', '(31) 98765-1234', '2024-02-15', 'Belo Horizonte', 'MG', 'Logística', 'Pequeno'),
('Cooperativa Agro Verde', 'cooperativa@agroverde.org', '(19) 98765-6789', '2024-03-01', 'Campinas', 'SP', 'Cooperativa', 'Grande'),
('Fazenda Bom Futuro', 'fazenda@bomfuturo.com', '(67) 99876-5432', '2024-03-20', 'Dourados', 'MS', 'Agricultura', 'Grande'),
('Agronegócio Paulista', 'contato@agropaulista.com', '(11) 98765-9876', '2024-04-10', 'Ribeirão Preto', 'SP', 'Comércio', 'Médio'),
('Cerealista Mineira', 'vendas@cerealistamineira.com', '(31) 98765-4567', '2024-05-15', 'Uberlândia', 'MG', 'Comércio', 'Médio'),
('Logística Agrícola', 'logistica@logagri.com', '(41) 99876-1234', '2024-06-01', 'Curitiba', 'PR', 'Logística', 'Pequeno'),
('Silos Guarulhos', 'contato@silosguarulhos.com', '(11) 98765-2345', '2024-07-22', 'Guarulhos', 'SP', 'Armazenagem', 'Médio'),
('Armazéns Rurais', 'vendas@armazensrurais.com', '(51) 99876-6543', '2024-08-30', 'Porto Alegre', 'RS', 'Armazenagem', 'Grande'),
('Comércio de Grãos RS', 'contato@graosrs.com', '(51) 98765-3456', '2024-09-05', 'Pelotas', 'RS', 'Comércio', 'Pequeno'),
('Distribuidora de Insumos', 'vendas@distribuidorainsumos.com', '(41) 98765-5678', '2024-10-12', 'Londrina', 'PR', 'Distribuição', 'Médio'),
('Produtos Agrícolas SC', 'contato@agricolasc.com', '(48) 99876-7654', '2024-11-20', 'Florianópolis', 'SC', 'Comércio', 'Pequeno'),
('Tratores e Colheitadeiras', 'vendas@tratoresecolheitadeiras.com', '(11) 98765-6789', '2025-01-08', 'Sorocaba', 'SP', 'Máquinas', 'Médio'),
('Irrigação Moderna', 'contato@irrigmoderna.com', '(19) 99876-8765', '2025-02-14', 'Piracicaba', 'SP', 'Irrigação', 'Pequeno'),
('Agropecuária Nordeste', 'contato@agrone.com', '(81) 98765-7890', '2024-02-20', 'Recife', 'PE', 'Agricultura', 'Médio'),
('Sementes Premium', 'vendas@sementespremium.com', '(51) 99876-9876', '2024-03-15', 'Passo Fundo', 'RS', 'Sementes', 'Pequeno'),
('Fertilizantes Naturais', 'contato@fertinatural.com', '(31) 98765-8901', '2024-05-10', 'Uberaba', 'MG', 'Insumos', 'Médio'),
('Transportadora Rural', 'fretes@transrural.com', '(11) 99876-0987', '2024-07-05', 'Bauru', 'SP', 'Logística', 'Pequeno'),
('Cooperativa Agrícola PR', 'coop@coopagripr.com', '(41) 98765-9012', '2024-09-18', 'Maringá', 'PR', 'Cooperativa', 'Grande');

-- Inserção de produtos com dados completos
INSERT INTO produtos (nome, categoria, subcategoria, preco, fornecedor) VALUES
('Soja em Grão 60kg', 'Grãos', 'Soja', 150.00,'Fornecedor A'),
('Milho em Grão 60kg', 'Grãos', 'Milho', 120.00, 'Fornecedor B'),
('Arroz em Casca 50kg', 'Grãos', 'Arroz', 110.00, 'Fornecedor C'),
('Semente de Soja 40kg', 'Grãos', 'Soja', 200.00, 'Fornecedor I'),
('Frete Local', 'Transporte', 'Frete', 500.00, 'Transportadora X'),
('Frete Interestadual', 'Transporte', 'Frete', 1500.00, 'Transportadora Y'),
('Serviço de Armazenagem', 'Logística', 'Armazenagem', 300.00, 'Armazém Z'),
('Sementes de Trigo 50kg', 'Grãos', 'Trigo', 180.00, 'Fornecedor D'),
('Transporte de Grãos', 'Transporte', 'Frete', 1000.00, 'Transportadora W'),
('Fertilizante NPK', 'Insumos', 'Fertilizante', 250.00, 'Fornecedor E'),
('Defensivo Agrícola', 'Insumos', 'Defensivo', 350.00, 'Fornecedor F'),
('Adubo Orgânico 20kg', 'Insumos', 'Fertilizante', 120.00, 'Fornecedor G'),
('Herbicida 5L', 'Insumos', 'Defensivo', 280.00,'Fornecedor H');

-- Adicionando mais pedidos (ordenados por data desde 01/02/2022)
-- Pedidos ordenados por data
INSERT INTO pedidos (id_pedido, data_pedido, valor_total, id_cliente, status_pedido, forma_pagamento) VALUES
(1, '2022-02-01', 1800.00, 1, 'Entregue', 'Boleto'),
(2, '2022-02-10', 300.00, 1, 'Entregue', 'Pix'),
(3, '2022-02-15', 2200.00, 3, 'Entregue', 'Transferência'),
(4, '2022-03-05', 1500.00, 2, 'Entregue', 'Cartão de Crédito'),
(5, '2022-03-15', 240.00, 2, 'Entregue', 'Cartão de Crédito'),
(6, '2022-04-05', 110.00, 3, 'Entregue', 'Boleto'),
(7, '2022-04-10', 3200.00, 4, 'Entregue', 'Boleto'),
(8, '2022-05-10', 250.00, 4, 'Entregue', 'Transferência'),
(9, '2022-05-12', 1900.00, 5, 'Entregue', 'Cartão de Crédito'),
(10, '2022-06-01', 180.00, 5, 'Entregue', 'Pix'),
(11, '2022-06-08', 2500.00, 6, 'Entregue', 'Transferência'),
(12, '2022-07-12', 120.00, 6, 'Entregue', 'Cartão de Crédito'),
(13, '2022-07-15', 1800.00, 7, 'Entregue', 'Boleto'),
(14, '2022-08-08', 480.00, 7, 'Entregue', 'Pix'),
(15, '2022-08-20', 3100.00, 8, 'Entregue', 'Cartão de Crédito'),
(16, '2022-09-05', 2700.00, 9, 'Entregue', 'Boleto'),
(17, '2022-09-20', 110.00, 8, 'Entregue', 'Boleto'),
(18, '2022-10-12', 3500.00, 10, 'Entregue', 'Transferência'),
(19, '2022-10-18', 200.00, 9, 'Entregue', 'Transferência'),
(20, '2022-11-18', 2200.00, 11, 'Entregue', 'Cartão de Crédito'),
(21, '2022-11-25', 350.00, 10, 'Entregue', 'Pix'),
(22, '2022-12-05', 110.00, 1, 'Entregue', 'Cartão de Crédito'),
(23, '2022-12-22', 2900.00, 12, 'Entregue', 'Boleto'),
(24, '2023-01-10', 3100.00, 13, 'Entregue', 'Cartão de Crédito'),
(25, '2023-01-14', 500.00, 2, 'Entregue', 'Transferência'),
(26, '2023-02-15', 1800.00, 14, 'Entregue', 'Boleto'),
(27, '2023-02-22', 110.00, 3, 'Entregue', 'Pix'),
(28, '2023-03-20', 4200.00, 15, 'Entregue', 'Transferência'),
(29, '2023-03-30', 150.00, 4, 'Entregue', 'Boleto'),
(30, '2023-04-05', 2500.00, 16, 'Entregue', 'Cartão de Crédito'),
(31, '2023-04-17', 320.00, 5, 'Entregue', 'Cartão de Crédito'),
(32, '2023-05-09', 420.00, 6, 'Entregue', 'Pix'),
(33, '2023-05-12', 3800.00, 17, 'Entregue', 'Boleto'),
(34, '2023-06-11', 110.00, 7, 'Entregue', 'Transferência'),
(35, '2023-06-18', 1900.00, 18, 'Entregue', 'Transferência'),
(36, '2023-07-22', 3100.00, 19, 'Entregue', 'Cartão de Crédito'),
(37, '2023-07-27', 320.00, 8, 'Entregue', 'Boleto'),
(38, '2023-08-15', 180.00, 9, 'Entregue', 'Pix'),
(39, '2023-08-25', 2700.00, 20, 'Entregue', 'Boleto'),
(40, '2023-09-03', 530.00, 10, 'Entregue', 'Cartão de Crédito'),
(41, '2023-09-30', 3600.00, 1, 'Entregue', 'Transferência'),
(42, '2023-10-05', 2200.00, 3, 'Entregue', 'Cartão de Crédito'),
(43, '2023-10-12', 150.00, 1, 'Entregue', 'Pix'),
(44, '2023-11-10', 2900.00, 5, 'Entregue', 'Boleto'),
(45, '2023-11-29', 350.00, 2, 'Entregue', 'Transferência'),
(46, '2023-12-15', 4100.00, 7, 'Entregue', 'Transferência'),
(47, '2023-12-20', 110.00, 3, 'Entregue', 'Cartão de Crédito'),
(48, '2024-01-05', 3200.00, 9, 'Entregue', 'Cartão de Crédito'),
(49, '2024-01-18', 1000.00, 4, 'Entregue', 'Pix'),
(50, '2024-02-10', 1800.00, 11, 'Entregue', 'Boleto'),
(51, '2024-02-25', 110.00, 5, 'Entregue', 'Boleto'),
(52, '2024-03-10', 270.00, 6, 'Entregue', 'Cartão de Crédito'),
(53, '2024-03-15', 4200.00, 13, 'Entregue', 'Transferência'),
(54, '2024-04-02', 180.00, 7, 'Entregue', 'Pix'),
(55, '2024-04-20', 2500.00, 15, 'Entregue', 'Cartão de Crédito'),
(56, '2024-05-15', 370.00, 8, 'Entregue', 'Transferência'),
(57, '2024-05-25', 3800.00, 17, 'Entregue', 'Boleto'),
(58, '2024-06-22', 120.00, 9, 'Entregue', 'Cartão de Crédito'),
(59, '2024-06-30', 1900.00, 19, 'Entregue', 'Transferência'),
(60, '2024-07-05', 3100.00, 2, 'Entregue', 'Cartão de Crédito'),
(61, '2024-07-30', 480.00, 10, 'Entregue', 'Pix'),
(62, '2024-08-10', 2700.00, 4, 'Entregue', 'Boleto'),
(63, '2024-08-12', 290.00, 1, 'Entregue', 'Boleto'),
(64, '2024-09-15', 3600.00, 6, 'Entregue', 'Transferência'),
(65, '2024-10-18', 240.00, 3, 'Entregue', 'Cartão de Crédito'),
(66, '2024-10-20', 2200.00, 8, 'Entregue', 'Cartão de Crédito'),
(67, '2024-11-21', 150.00, 4, 'Entregue', 'Pix'),
(68, '2024-11-25', 2900.00, 10, 'Entregue', 'Boleto'),
(69, '2024-12-10', 390.00, 5, 'Entregue', 'Boleto'),
(70, '2024-12-30', 4100.00, 12, 'Entregue', 'Transferência'),
(71, '2025-01-05', 3200.00, 14, 'Entregue', 'Cartão de Crédito'),
(72, '2025-01-15', 1000.00, 6, 'Entregue', 'Transferência'),
(73, '2025-02-10', 1800.00, 16, 'Entregue', 'Boleto'),
(74, '2025-02-28', 120.00, 7, 'Processando', 'Cartão de Crédito'),
(75, '2025-03-10', 480.00, 8, 'Entregue', 'Pix'),
(76, '2025-03-15', 4200.00, 18, 'Entregue', 'Transferência'),
(77, '2025-04-05', 180.00, 9, 'Entregue', 'Boleto');

-- Adicionando itens de pedido (alguns corretos, outros incorretos)
INSERT INTO itens_pedido (id_pedido, id_produto, quantidade, preco_unitario) VALUES
(1, 1, 10, 150.00),  -- 10x Soja em Grão
(1, 5, 1, 300.00),   -- Frete Local
(2, 1, 2, 150.00),   -- 2x Soja em Grão
(3, 2, 15, 120.00),  -- 15x Milho em Grão
(3, 6, 1, 400.00),   -- Frete Interestadual
(4, 3, 10, 110.00),  -- 10x Arroz em Casca
(4, 7, 1, 400.00),   -- Serviço de Armazenagem
(5, 2, 1, 120.00),   -- 1x Milho em Grão
(5, 12, 1, 120.00),  -- 1x Adubo Orgânico
(6, 3, 1, 110.00),   -- 1x Arroz em Casca
(7, 1, 20, 150.00),  -- 20x Soja em Grão
(7, 5, 1, 200.00),   -- Frete Local
(8, 10, 1, 250.00),  -- 1x Fertilizante NPK
(9, 2, 10, 120.00),  -- 10x Milho em Grão
(9, 8, 2, 350.00),   -- 2x Sementes de Trigo
(10, 8, 1, 180.00),  -- 1x Sementes de Trigo
(11, 3, 15, 110.00), -- 15x Arroz em Casca
(11, 9, 1, 850.00),  -- Transporte de Grãos
(12, 2, 1, 120.00),  -- 1x Milho em Grão
(13, 4, 5, 200.00),  -- 5x Semente de Soja
(13, 10, 2, 400.00), -- 2x Fertilizante NPK
(14, 4, 1, 200.00),  -- 1x Semente de Soja
(14, 13, 1, 280.00), -- 1x Herbicida
(15, 5, 1, 500.00),  -- Frete Local
(15, 11, 5, 520.00), -- 5x Defensivo Agrícola
(16, 6, 1, 1500.00), -- Frete Interestadual
(16, 12, 4, 300.00), -- 4x Adubo Orgânico
(17, 3, 1, 110.00),  -- 1x Arroz em Casca
(18, 7, 10, 300.00), -- 10x Serviço de Armazenagem
(18, 13, 1, 500.00), -- 1x Herbicida
(19, 4, 1, 200.00),  -- 1x Semente de Soja
(20, 8, 10, 180.00), -- 10x Sementes de Trigo
(20, 1, 2, 200.00),  -- 2x Soja em Grão
(21, 11, 1, 350.00), -- 1x Defensivo Agrícola
(22, 3, 1, 110.00),  -- 1x Arroz em Casca
(23, 9, 2, 1000.00), -- 2x Transporte de Grãos
(23, 2, 5, 180.00),  -- 5x Milho em Grão
(24, 10, 8, 250.00), -- 8x Fertilizante NPK
(24, 3, 3, 110.00),  -- 3x Arroz em Casca
(24, 6, 1, 500.00),  -- Frete Interestadual
(25, 5, 1, 500.00),  -- 1x Frete Local
(26, 11, 4, 350.00), -- 4x Defensivo Agrícola
(26, 4, 2, 200.00),  -- 2x Semente de Soja
(27, 3, 1, 110.00),  -- 1x Arroz em Casca
(28, 12, 10, 120.00), -- 10x Adubo Orgânico
(28, 5, 1, 1500.00),  -- Frete Interestadual
(28, 7, 1, 300.00),   -- Serviço de Armazenagem
(29, 1, 1, 150.00),   -- 1x Soja em Grão
(30, 13, 5, 280.00),  -- 5x Herbicida
(30, 8, 3, 180.00),   -- 3x Sementes de Trigo
(31, 4, 1, 200.00),   -- 1x Semente de Soja
(31, 12, 1, 120.00),  -- 1x Adubo Orgânico
(32, 7, 1, 300.00),   -- 1x Serviço de Armazenagem
(32, 12, 1, 120.00),  -- 1x Adubo Orgânico
(33, 1, 15, 150.00),  -- 15x Soja em Grão
(33, 9, 1, 1000.00),  -- Transporte de Grãos
(33, 3, 2, 110.00),   -- 2x Arroz em Casca
(34, 3, 1, 110.00),   -- 1x Arroz em Casca
(35, 2, 10, 120.00), -- 10x Milho em Grão
(35, 10, 2, 350.00),  -- 2x Fertilizante NPK
(36, 3, 20, 110.00),  -- 20x Arroz em Casca
(36, 11, 1, 350.00),  -- 1x Defensivo Agrícola
(36, 5, 1, 500.00),   -- Frete Local
(37, 4, 1, 200.00),   -- 1x Semente de Soja
(37, 2, 1, 120.00),   -- 1x Milho em Grão
(38, 8, 1, 180.00),   -- 1x Sementes de Trigo
(39, 4, 10, 200.00),  -- 10x Semente de Soja
(39, 12, 2, 350.00),  -- 2x Adubo Orgânico
(40, 10, 1, 250.00),  -- 1x Fertilizante NPK
(40, 13, 1, 280.00),  -- 1x Herbicida
(41, 5, 2, 500.00),
(41, 13, 10, 120.00),
(41, 6, 1, 1000.00),
(42, 6, 1, 1000.00),
(42, 7, 4, 300.00),
(43, 1, 1, 150.00),
(44, 7, 5, 300.00),
(44, 8, 4, 180.00),
(44, 9, 1, 800.00),
(45, 11, 1, 350.00),
(46, 8, 10, 180.00),
(46, 10, 5, 250.00),
(46, 11, 2, 350.00),
(47, 3, 1, 110.00),
(48, 9, 3, 1000.00),
(48, 12, 1, 200.00),
(49, 10, 6, 250.00),
(49, 13, 2, 150.00),
(50, 11, 10, 350.00),
(50, 1, 5, 140.00),
(51, 3, 1, 110.00),
(52, 12, 10, 120.00),
(52, 2, 5, 130.00),
(52, 3, 2, 110.00),
(53, 13, 20, 120.00),
(53, 4, 5, 200.00),
(53, 5, 1, 400.00),
(54, 8, 1, 180.00),
(55, 1, 10, 150.00),
(55, 6, 1, 400.00),
(56, 10, 1, 250.00),
(56, 12, 1, 120.00),
(57, 2, 15, 120.00),
(57, 7, 2, 350.00),
(57, 8, 1, 180.00),
(58, 2, 1, 120.00),
(59, 3, 20, 110.00),
(59, 9, 1, 500.00),
(60, 7, 10, 300.00),
(60, 13, 5, 120.00),
(60, 1, 2, 150.00),
(61, 4, 15, 200.00),
(61, 10, 2, 300.00),
(62, 8, 15, 180.00),
(62, 2, 2, 130.00),
(63, 5, 3, 500.00),
(63, 11, 2, 350.00),
(64, 9, 1, 1500.00),
(64, 3, 2, 150.00),
(65, 6, 2, 1000.00),
(65, 12, 3, 300.00),
(66, 10, 10, 250.00),
(66, 4, 5, 200.00),
(66, 5, 1, 500.00),
(67, 11, 6, 350.00),
(67, 6, 1, 400.00),
(68, 1, 10, 150.00),
(68, 2, 1, 120.00),
(69, 3, 1, 110.00),
(70, 4, 1, 200.00),
(71, 5, 1, 500.00),
(72, 6, 1, 1000.00),
(73, 7, 1, 300.00),
(74, 8, 1, 180.00),
(75, 9, 1, 1000.00),
(76, 10, 1, 250.00),
(77, 11, 1, 350.00);