-- 7. Criação de view para análise simplificada
CREATE OR REPLACE VIEW vw_pedidos_compartilhados AS
SELECT 
    p.id_pedido,
    p.data_pedido,
    p.valor_total,
    p.status_pedido,
    p.eh_compartilhado,
    p.total_participantes,
    c1.nome AS cliente_principal,
    (
        SELECT STRING_AGG(
            c2.nome || ' (' || pc.percentual_participacao::numeric(5,2) || '%)', 
            ', ' ORDER BY pc.percentual_participacao DESC
        )
        FROM pedido_clientes pc
        JOIN clientes c2 ON pc.id_cliente = c2.id_cliente
        WHERE pc.id_pedido = p.id_pedido AND NOT pc.eh_responsavel_pagamento
    ) AS outros_participantes
FROM 
    pedidos p
JOIN 
    pedido_clientes pc1 ON p.id_pedido = pc1.id_pedido AND pc1.eh_responsavel_pagamento
JOIN 
    clientes c1 ON pc1.id_cliente = c1.id_cliente
WHERE 
    p.eh_compartilhado = TRUE
ORDER BY 
    p.data_pedido DESC;

-- 8. Consulta de verificação detalhada
SELECT 
    p.id_pedido,
    p.data_pedido,
    p.valor_total,
    p.status_pedido,
    p.total_participantes,
    p.eh_compartilhado,
    c1.nome AS cliente_principal,
    (SELECT SUM(pc.percentual_participacao) FROM pedido_clientes pc WHERE pc.id_pedido = p.id_pedido) AS total_percentual,
    (
        SELECT STRING_AGG(
            c2.nome || ' (' || pc.percentual_participacao::numeric(5,2) || '%)', 
            ', ' ORDER BY pc.percentual_participacao DESC
        )
        FROM pedido_clientes pc
        JOIN clientes c2 ON pc.id_cliente = c2.id_cliente
        WHERE pc.id_pedido = p.id_pedido AND NOT pc.eh_responsavel_pagamento
    ) AS outros_participantes
FROM 
    pedidos p
JOIN 
    pedido_clientes pc1 ON p.id_pedido = pc1.id_pedido AND pc1.eh_responsavel_pagamento
JOIN 
    clientes c1 ON pc1.id_cliente = c1.id_cliente
ORDER BY 
    p.total_participantes DESC, p.id_pedido;