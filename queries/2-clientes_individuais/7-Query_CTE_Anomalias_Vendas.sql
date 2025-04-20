WITH calculo_valor_pedidos AS (
    SELECT 
        p.id_pedido,
        p.valor_total AS valor_total_registrado,
        SUM(ip.quantidade * ip.preco_unitario) AS valor_calculado,
        p.forma_pagamento,
        p.status_pedido,
        p.data_pedido,
        c.nome AS nome_cliente,
        -- Diferença absoluta entre os valores
        ABS(p.valor_total - SUM(ip.quantidade * ip.preco_unitario)) AS diferenca_absoluta,
        -- Diferença percentual (com tratamento de divisão por zero)
        CASE 
            WHEN p.valor_total = 0 THEN NULL::numeric
            ELSE ROUND(
                (ABS(p.valor_total - SUM(ip.quantidade * ip.preco_unitario)) / 
                NULLIF(p.valor_total, 0) * 100), 
                2
            )
        END AS diferenca_percentual
    FROM 
        pedidos p
    JOIN 
        itens_pedido ip ON p.id_pedido = ip.id_pedido
    JOIN
        clientes c ON p.id_cliente = c.id_cliente
    WHERE
        p.eh_compartilhado = FALSE
        AND p.status_pedido = 'Entregue'
    GROUP BY 
        p.id_pedido, p.valor_total, p.forma_pagamento, p.status_pedido, p.data_pedido, c.nome
)

SELECT 
    id_pedido,
    valor_total_registrado,
    valor_calculado,
    diferenca_absoluta,
    CASE 
        WHEN diferenca_percentual IS NULL THEN 'N/A' 
        ELSE diferenca_percentual::text || '%' 
    END AS diferenca_percentual,
    forma_pagamento,
    status_pedido,
    data_pedido,
    nome_cliente,
    CASE
        WHEN diferenca_absoluta = 0 THEN 'Valor correto'
        WHEN diferenca_absoluta <= 50 THEN 'Disparidade Pequena'
        WHEN diferenca_absoluta <= 200 THEN 'Disparidade Moderada'
        ELSE 'Disparidade Grande'
    END AS severidade
FROM 
    calculo_valor_pedidos
WHERE 
    valor_total_registrado <> valor_calculado
    OR (valor_total_registrado = 0 AND valor_calculado IS NOT NULL)
    OR (valor_calculado = 0 AND valor_total_registrado IS NOT NULL)
ORDER BY 
    diferenca_absoluta DESC;