WITH ultima_compra_cliente AS (
    SELECT 
        c.id_cliente,
        c.nome,
        c.email,
        c.telefone,
        c.cidade,
        c.uf,
        c.segmento,
        c.tamanho_empresa,
        MAX(p.data_pedido) AS data_ultimo_pedido
    FROM 
        clientes c
    LEFT JOIN 
        pedidos p ON c.id_cliente = p.id_cliente
        AND p.status_pedido = 'Entregue'
        AND p.eh_compartilhado = FALSE
    GROUP BY 
        c.id_cliente, c.nome, c.email, c.telefone, 
        c.cidade, c.uf, c.segmento, c.tamanho_empresa
)

SELECT 
    ucc.id_cliente,
    ucc.nome,
    ucc.email,
    ucc.telefone,
    ucc.cidade,
    ucc.uf,
    ucc.segmento,
    ucc.tamanho_empresa,
    ucc.data_ultimo_pedido,
    CASE 
        WHEN ucc.data_ultimo_pedido IS NULL THEN 'Nunca comprou'
        ELSE (CURRENT_DATE - ucc.data_ultimo_pedido)::TEXT || ' dias'
    END AS dias_inatividade,
    CASE
        WHEN ucc.data_ultimo_pedido IS NULL THEN 'Nunca comprou'
        WHEN ucc.data_ultimo_pedido < CURRENT_DATE - INTERVAL '6 months' THEN 'Inativo por mais de 6 meses'
        ELSE 'Ativo'
    END AS status_cliente
FROM 
    ultima_compra_cliente ucc
WHERE
    ucc.data_ultimo_pedido IS NULL 
    OR ucc.data_ultimo_pedido < CURRENT_DATE - INTERVAL '6 months'
ORDER BY
    CASE 
        WHEN ucc.data_ultimo_pedido IS NULL THEN 1 
        ELSE 0 
    END,
    ucc.data_ultimo_pedido DESC;