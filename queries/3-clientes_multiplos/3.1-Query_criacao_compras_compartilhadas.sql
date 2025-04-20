-- 1. Remover a tabela existente se houver (com CASCADE para remover dependências)
DROP TABLE IF EXISTS pedido_clientes CASCADE;

-- 2. Criar a tabela pedido_clientes com estrutura completa
CREATE TABLE pedido_clientes (
    id_pedido INT NOT NULL,
    id_cliente INT NOT NULL,
    percentual_participacao NUMERIC(5,2) NOT NULL,
    eh_responsavel_pagamento BOOLEAN NOT NULL,
    PRIMARY KEY (id_pedido, id_cliente),
    CONSTRAINT fk_pedido FOREIGN KEY (id_pedido) REFERENCES pedidos(id_pedido) ON DELETE CASCADE,
    CONSTRAINT fk_cliente FOREIGN KEY (id_cliente) REFERENCES clientes(id_cliente) ON DELETE RESTRICT,
    CONSTRAINT chk_percentual CHECK (percentual_participacao > 0 AND percentual_participacao <= 100)
);

-- 3. Criar índices para melhor performance
CREATE INDEX idx_pedido_clientes_pedido ON pedido_clientes(id_pedido);
CREATE INDEX idx_pedido_clientes_cliente ON pedido_clientes(id_cliente);

-- 4. Atribuição aleatória de porcentagens com lógica aprimorada
WITH pedidos_para_processar AS (
    SELECT 
        p.id_pedido,
        p.id_cliente AS cliente_original,
        -- Distribuição ajustada: 70% individual, 25% 2 clientes, 5% 3 clientes
        CASE 
            WHEN RANDOM() < 0.7 THEN 1 
            WHEN RANDOM() < 0.96 THEN 2
            ELSE 3 
        END AS total_clientes,
        -- Seleciona clientes adicionais com filtros por segmento/região
        CASE WHEN RANDOM() >= 0.7 THEN 
            (SELECT id_cliente FROM clientes 
             WHERE id_cliente != p.id_cliente 
             AND segmento = (SELECT segmento FROM clientes WHERE id_cliente = p.id_cliente)
             ORDER BY RANDOM() LIMIT 1)
        END AS cliente_adicional_1,
        CASE WHEN RANDOM() >= 0.95 THEN 
            (SELECT id_cliente FROM (
                SELECT id_cliente FROM clientes 
                WHERE id_cliente != p.id_cliente 
                AND id_cliente NOT IN (
                    SELECT id_cliente FROM clientes 
                    WHERE id_cliente != p.id_cliente 
                    AND segmento = (SELECT segmento FROM clientes WHERE id_cliente = p.id_cliente)
                    LIMIT 1
                )
                AND uf = (SELECT uf FROM clientes WHERE id_cliente = p.id_cliente)
                ORDER BY RANDOM() LIMIT 1
            ) AS subquery)
        END AS cliente_adicional_2
    FROM 
        pedidos p
    WHERE 
        p.id_cliente IS NOT NULL
        AND p.data_pedido >= '2023-01-01'  -- Foco em pedidos mais recentes
)

-- 5. Inserção dos relacionamentos com porcentagens dinâmicas
INSERT INTO pedido_clientes (id_pedido, id_cliente, percentual_participacao, eh_responsavel_pagamento)
-- Pedidos individuais (100%)
SELECT 
    id_pedido,
    cliente_original,
    100.00,
    TRUE
FROM 
    pedidos_para_processar
WHERE 
    total_clientes = 1

UNION ALL

-- Pedidos com 2 clientes (percentual varia com valor do pedido)
SELECT 
    id_pedido,
    cliente_original,
    CASE 
        WHEN (SELECT valor_total FROM pedidos WHERE id_pedido = ppp.id_pedido) > 2000 THEN 70.00
        ELSE 60.00
    END,
    TRUE
FROM 
    pedidos_para_processar ppp
WHERE 
    total_clientes = 2

UNION ALL

SELECT 
    id_pedido,
    cliente_adicional_1,
    CASE 
        WHEN (SELECT valor_total FROM pedidos WHERE id_pedido = ppp.id_pedido) > 2000 THEN 30.00
        ELSE 40.00
    END,
    FALSE
FROM 
    pedidos_para_processar ppp
WHERE 
    total_clientes = 2 AND cliente_adicional_1 IS NOT NULL

UNION ALL

-- Pedidos com 3 clientes (50%/30%/20%)
SELECT 
    id_pedido,
    cliente_original,
    50.00,
    TRUE
FROM 
    pedidos_para_processar
WHERE 
    total_clientes = 3

UNION ALL

SELECT 
    id_pedido,
    cliente_adicional_1,
    30.00,
    FALSE
FROM 
    pedidos_para_processar
WHERE 
    total_clientes = 3 AND cliente_adicional_1 IS NOT NULL

UNION ALL

SELECT 
    id_pedido,
    cliente_adicional_2,
    20.00,
    FALSE
FROM 
    pedidos_para_processar
WHERE 
    total_clientes = 3 AND cliente_adicional_2 IS NOT NULL;

-- 6. Atualização do status dos pedidos com mais informações
-- Verifica se a coluna já existe antes de adicionar
DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
                  WHERE table_name = 'pedidos' AND column_name = 'eh_compartilhado') THEN
        ALTER TABLE pedidos ADD COLUMN eh_compartilhado BOOLEAN DEFAULT FALSE;
    END IF;
    
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
                  WHERE table_name = 'pedidos' AND column_name = 'total_participantes') THEN
        ALTER TABLE pedidos ADD COLUMN total_participantes INT DEFAULT 1;
    END IF;
END $$;

UPDATE pedidos p
SET 
    eh_compartilhado = (SELECT COUNT(*) > 1 FROM pedido_clientes pc WHERE pc.id_pedido = p.id_pedido),
    total_participantes = (SELECT COUNT(*) FROM pedido_clientes pc WHERE pc.id_pedido = p.id_pedido);