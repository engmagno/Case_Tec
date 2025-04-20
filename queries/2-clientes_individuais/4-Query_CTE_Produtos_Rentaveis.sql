WITH receita_geral AS (
    -- Calcula a receita total de todos os pedidos individuais
    SELECT 
        COALESCE(SUM(ip.quantidade * ip.preco_unitario), 0) AS receita_total_geral
    FROM 
        itens_pedido ip
    JOIN 
        pedidos p ON ip.id_pedido = p.id_pedido
    WHERE 
        p.status_pedido = 'Concluído'
        AND p.eh_compartilhado = FALSE
),

receita_produtos AS (
    -- Calcula a receita para cada produto em pedidos individuais
    SELECT 
        pr.id_produto,
        pr.nome,
        pr.categoria,
        pr.subcategoria,
        COALESCE(SUM(ip.quantidade * ip.preco_unitario), 0) AS receita_total,
        COUNT(DISTINCT ip.id_pedido) AS qtd_pedidos,
        COALESCE(SUM(ip.quantidade), 0) AS unidades_vendidas,
        COALESCE(AVG(ip.preco_unitario), 0) AS preco_medio
    FROM 
        produtos pr
    LEFT JOIN 
        itens_pedido ip ON pr.id_produto = ip.id_produto
    LEFT JOIN 
        pedidos p ON ip.id_pedido = p.id_pedido
        AND p.status_pedido = 'Concluído'
        AND p.eh_compartilhado = FALSE
    GROUP BY 
        pr.id_produto, pr.nome, pr.categoria, pr.subcategoria
)

-- Resultado final com cálculo de percentual
SELECT 
    rp.id_produto,
    rp.nome,
    rp.categoria,
    rp.subcategoria,
    rp.receita_total,
    rp.qtd_pedidos,
    rp.unidades_vendidas,
    rp.preco_medio,
    CASE 
        WHEN rg.receita_total_geral > 0 
        THEN ROUND((rp.receita_total * 100.0 / rg.receita_total_geral), 2)
        ELSE 0 
    END AS percentual_receita,
    rg.receita_total_geral,
    DENSE_RANK() OVER (ORDER BY rp.receita_total DESC) AS ranking_rentabilidade
FROM 
    receita_produtos rp
CROSS JOIN 
    receita_geral rg
ORDER BY 
    rp.receita_total DESC
LIMIT 5;