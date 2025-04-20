WITH base_pedidos AS (
    -- Filtra apenas pedidos individuais concluídos com data válida
    SELECT
        id_pedido,
        valor_total,
        data_pedido,
        id_cliente,
        forma_pagamento
    FROM
        pedidos
    WHERE
        status_pedido = 'Entregue'
        AND eh_compartilhado = FALSE
        AND data_pedido IS NOT NULL
),

vendas_mensais AS (
    -- Agregação mensal básica
    SELECT
        TO_CHAR(data_pedido, 'YYYY-MM') AS mes_ano,
        SUM(valor_total) AS total_vendas,
        COUNT(id_pedido) AS quantidade_pedidos,
        COUNT(DISTINCT id_cliente) AS clientes_ativos
    FROM
        base_pedidos
    GROUP BY
        TO_CHAR(data_pedido, 'YYYY-MM')
),

vendas_com_analise AS (
    -- Adiciona cálculos de crescimento e métricas derivadas
    SELECT
        vm.mes_ano,
        vm.total_vendas,
        vm.quantidade_pedidos,
        vm.clientes_ativos,
        vm.total_vendas / NULLIF(vm.quantidade_pedidos, 0) AS ticket_medio,
        -- Cálculo seguro do crescimento percentual
        CASE
            WHEN LAG(vm.total_vendas) OVER (ORDER BY vm.mes_ano) IS NULL THEN NULL
            WHEN LAG(vm.total_vendas) OVER (ORDER BY vm.mes_ano) = 0 THEN NULL
            ELSE ROUND(
                (vm.total_vendas - LAG(vm.total_vendas) OVER (ORDER BY vm.mes_ano)) * 100.0 / 
                LAG(vm.total_vendas) OVER (ORDER BY vm.mes_ano),
                2
            )
        END AS crescimento_percentual,
        -- Forma de pagamento mais comum (alternativa mais compatível)
        (SELECT bp.forma_pagamento
         FROM base_pedidos bp
         WHERE TO_CHAR(bp.data_pedido, 'YYYY-MM') = vm.mes_ano
         GROUP BY bp.forma_pagamento
         ORDER BY COUNT(*) DESC
         LIMIT 1) AS forma_pagamento_mais_comum
    FROM
        vendas_mensais vm
)

-- Resultado final garantindo retorno de valores
SELECT
    va.mes_ano,
    va.total_vendas,
    va.crescimento_percentual,
    va.quantidade_pedidos,
    va.ticket_medio,
    va.clientes_ativos,
    va.forma_pagamento_mais_comum,
    -- Verificação adicional para garantir que a consulta retorne dados
    CASE 
        WHEN EXISTS (SELECT 1 FROM base_pedidos) THEN 'Dados Disponíveis'
        ELSE 'Sem pedidos no período' 
    END AS status_dados
FROM
    vendas_com_analise va
ORDER BY
    va.mes_ano;