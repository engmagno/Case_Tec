WITH pedidos_cliente AS (
    SELECT 
        p.id_cliente,
        c.nome,
        c.segmento,
        c.tamanho_empresa,
        p.id_pedido,
        p.data_pedido,
        p.valor_total,
        p.status_pedido,
        p.forma_pagamento,
        -- Usando LAG para obter a data do pedido anterior do mesmo cliente
        LAG(p.data_pedido) OVER (PARTITION BY p.id_cliente ORDER BY p.data_pedido) AS data_pedido_anterior,
        -- Calculando o número de pedidos por cliente
        COUNT(p.id_pedido) OVER (PARTITION BY p.id_cliente) AS total_pedidos,
        -- Calculando o ticket médio por cliente
        AVG(p.valor_total) OVER (PARTITION BY p.id_cliente) AS ticket_medio
    FROM 
        pedidos p
    JOIN 
        clientes c ON p.id_cliente = c.id_cliente
    WHERE 
        p.status_pedido <> 'Cancelado'  -- Utilizando o novo campo status_pedido para filtrar
)

SELECT DISTINCT
    id_cliente,
    nome,
    segmento,
    tamanho_empresa,
    -- Calculando dias desde o último pedido
    CURRENT_DATE - MAX(data_pedido) OVER (PARTITION BY id_cliente) AS dias_desde_ultimo_pedido,
    total_pedidos,
    ticket_medio,
    -- Adicionando informações adicionais baseadas nos novos campos
    LAST_VALUE(forma_pagamento) OVER (PARTITION BY id_cliente ORDER BY data_pedido 
                                     ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING) AS ultima_forma_pagamento
FROM 
    pedidos_cliente
ORDER BY 
    dias_desde_ultimo_pedido DESC NULLS LAST, 
    total_pedidos DESC;