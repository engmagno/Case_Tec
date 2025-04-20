# Case Técnico: Sistema de Análise de Dados para Agronegócio

## 1.Visão Geral
Este repositório contém um case técnico completo para análise de dados em uma empresa do agronegócio que atua na compra, venda e transporte de produtos agrícolas. O sistema foi desenvolvido para fornecer insights estratégicos sobre operações comerciais e comportamento de clientes.

## 2.Objetivos Principais
- Monitorar desempenho de produtos agrícolas,
- Identificar padrões de compra dos clientes,
- Garantir precisão nas transações comerciais,
- Mostrar gráficos que suportam os tópicos anteriores.

## 3.Estrutura do Banco de Dados
O modelo inclui:

### Tabelas Principais
- `clientes`: Informações completas dos compradores (incluindo segmento e localização),
- `produtos`: Dados dos produtos agrícolas (categorias, subcategorias, fornecedores),
- `pedidos`: Transações comerciais (com status detalhado e forma de pagamento),
- `pedidos_clientes`: Resultados da alteração de dados para comportar compras com múltiplos clientes,
- `itens_pedido`: Composição detalhada dos pedidos,
- `transportes`: Dados logísticos (para implementação futura).

## 4.Observações Gerais
- Evidencia-se as tarefas tiveram demandas que, posteriormente, foram otimizadas devido à demanda da **Tarefa 8(Otimização e Indexação**), 
- Em cada tópico das tarefas 5.1-5.7, apresentam-se as demandas da **Tarefa 9(Apresentação dos Dados)** e da **Tarefa 10(Análise Exploratória com Pandas e Matplotlib)**,
  - Foram definidas, no arquivo [app.py](./app.py), dois blocos na sidebar, um para casos de compras individuais (utilizado na maior parte do projeto) e outro de compras compartilhadas.
  - O Print da sidebar está localizado no Tópico `5.9.Tarefa 9 - Apresentação dos Dados`, enquanto os prints das páginas estão presentes em cada tópico,
- Especificamente na **Tarefa 10** foi utilizado, fora o `MatplotLib`, o `Plotly` para a disposição de gráficos 3D.
- Ressalta-se que as Tables geradas na **Tarefa 3** foram utilizadas em um caso específico. 

## 5.Tarefas Solicitadas

<details>
<summary><strong>5.1. Tarefa 1 - Modelagem do Banco de Dados </strong></summary>
<br>
 <details>
 <summary><strong>SQL - DEMANDA OTIMIZADA</strong></summary>
  
 No arquivo [1-Query_Criação_Banco_Dados.sql](./queries/1-criacao__geral/1-Query_Criação_Banco_Dados.sql) é possível visualizar o script completo de criação da estrutura do banco de dados.
 Nele, estão presentes a inserção de dados manuais, junto com as melhorias aplicadas à demanda inicial. Sendo elas: 
 
 ###### 1. Aprimoramento da Tabela `clientes`
   **Melhoria**: Adição de campos de contato, localização e segmentação  
   **Justificativa**:  
   - Campos de email e telefone (`VARCHAR`) permitem comunicação direta para confirmação de pedidos e pós-venda  
   - Dados geográficos (cidade/UF) habilitam análises regionais e logística eficiente  
   - Segmentação por tipo e tamanho de empresa possibilita estratégias comerciais personalizadas
   
   **Melhoria**: Tornar campos obrigatórios (`NOT NULL`)  
   **Justificativa**:  
   - Garante completude dos dados cadastrais essenciais  
   - Elimina inconsistências em documentos fiscais e contratos 
 
 ###### 2. Aprimoramento da Tabela  `produtos`  
 **Melhoria**: Adição de subcategoria e fornecedor  
 **Justificativa**:  
 - Classificação detalhada (ex: grãos > soja) para análises precisas por tipo de cultura  
 - Rastreabilidade completa da cadeia de suprimentos agrícolas  
 
 **Melhoria**: Restrições `NOT NULL` e precisão numérica  
 **Justificativa**:  
 - Elimina produtos não identificados no inventário  
 - Padronização monetária com `NUMERIC(10,2)` para cálculos exatos
 
 ###### 3. Aprimoramento da Tabela  `pedidos`  
 **Melhoria**: Novos campos de status e forma de pagamento  
 **Justificativa**:  
 - Visibilidade completa do ciclo do pedido (do transporte à entrega)  
 - Análise de preferências de pagamento por região e perfil de cliente  
 
 **Melhoria**: Campos obrigatórios com maior precisão  
 **Justificativa**:  
 - Registro temporal confiável para análise sazonal  
 - Suporte a transações de alto valor com `NUMERIC(12,2)`  
 
 ###### 4. Consolidação da Tabela `itens_pedido`  
 **Melhoria**: Restrições de integridade  
 **Justificativa**:  
 - Quantidade e preço obrigatórios garantem precisão nos cálculos de:  
   - Volumes transportados  
   - Valores totais por item agrícola  
 </details>

  <details>
  <summary><strong>Print da tabela `clientes`</strong></summary>
  
  ![tabela_clientes](https://github.com/user-attachments/assets/8cec334d-e7ed-4100-919c-2f2e4e3cb93a)

  </details>
  
  <details>
  <summary><strong>Print da tabela `produtos`</strong></summary>
  
  ![tabela_produtos](https://github.com/user-attachments/assets/1cb84af2-02ee-4ebf-8ff1-e5ba193b92c7)

  </details>
  
  <details>
  <summary><strong>Print da tabela `pedidos`</strong></summary>
  
  ![tabela_pedidos_clientes](https://github.com/user-attachments/assets/1cd00e38-6d2e-4d3c-9d68-b1dcb9b67914)

  
  </details>
  
  <details>
  <summary><strong>Print da tabela `itens_pedidos`</strong></summary>
  
  ![tabela_itens_pedidos](https://github.com/user-attachments/assets/0aa16bda-bcbe-44e3-b6d1-d889a21787b2)

  </details>

</details>

---
<details>
<summary><strong>5.2.Tarefa 2 - Análise de Recência, Frequência e Valor (RFM)</strong></summary>
 <br>
 <details>
 <summary><strong>SQL - DEMANDA OTIMIZADA</strong></summary>
  
 No arquivo [2-Query_CTE_Rec_Feq_Valor.sql](./queries/2-clientes_individuais/2-Query_CTE_Rec_Feq_Valor.sql) é possível visualizar o script completo para consulta RFM.
 Nele, estão presentes as melhorias aplicadas à demanda inicial. Sendo elas: 
 
 ###### 1. Segmentação RFM Avançada
 **Melhoria**: Implementação de cálculo em três dimensões (Recência, Frequência, Valor Monetário) com filtros precisos  
 **Justificativa**:  
 - Elimina distorções de pedidos cancelados ou em processamento através do filtro `status_pedido = 'Entregue'`  
 - Considera apenas transações individuais com `eh_compartilhado = FALSE` para análise focada  
 - Cálculo otimizado via CTE melhora performance em grandes volumes de dados  
 
 ###### 2. Classificação por Quintis Padronizada  
 **Melhoria**: Atribuição de scores de 1-5 para cada métrica usando função `NTILE()`  
 **Justificativa**:  
 - Permite comparação relativa entre clientes de diferentes perfis  
 - Escala universal facilita a criação de grupos homogêneos (ex: top 20% em valor)  
 - Adaptável a variações sazonais do agronegócio  
 
 ###### 3. Score RFM Consolidado  
 **Melhoria**: Criação de um código composto (ex: "535") combinando as três dimensões  
 **Justificativa**:  
 - Gera um identificador único para cada segmento de cliente  
 - Simplifica a integração com sistemas de CRM e ferramentas de marketing  
 - Permite rápida identificação de perfis estratégicos (ex: "555" = clientes Premium)  
 
 ###### 4. Enriquecimento com Dados Cadastrais  
 **Melhoria**: Junção com tabela de clientes para adicionar atributos demográficos  
 **Justificativa**:  
 - Possibilita cruzamentos com localização (UF/cidade) para análise geográfica  
 - Incorpora segmento e tamanho da empresa para personalização de ofertas  
 - Facilita a criação de clusters comportamentais  
 
 ###### 5. Filtros de Qualidade de Dados  
 **Melhoria**: Exclusão de registros com valor_total ≤ 0 ou frequência = 0  
 **Justificativa**:  
 - Remove distorções de pedidos teste ou transações inválidas  
 - Garante base limpa para tomada de decisão comercial
 
 </details>
 
 <details>
 <summary><strong>PYTHON - DEMANDA OTIMIZADA</strong></summary>
 
  O script [rfm_analysis.py](./src/analytics/rfm_analysis.py) implementa uma interface interativa com base nos resultados da análise RFM, trazendo insights visuais e filtros avançados.
  
  ###### 1. KPIs Interativos no Topo  
  **Feature**: Painéis de métricas dinâmicos para indicadores-chave (ex: ticket médio, recência, valor total)  
  **Justificativa**:  
  - Apresenta uma visão resumida do comportamento de clientes logo no início  
  - Utiliza `st.metric()` para comunicação clara e visual de valores importantes  
  - Facilita decisões rápidas com base em dados atualizados em tempo real  
  
  ###### 2. Filtros Personalizados para Exploração dos Dados  
  **Feature**: Sliders e multiselect para refinar os dados com base em critérios comportamentais  
  **Justificativa**:  
  - Permite ao usuário focar em clientes inativos, segmentos específicos ou com baixa frequência  
  - Melhora a navegabilidade da aplicação com componentes interativos do `Streamlit`  
  - Garante análises direcionadas com impacto real em estratégias de CRM  
  
  ###### 3. Gráficos Interativos com Plotly  
  **Feature**: Visualizações como histogramas, gráficos de dispersão 3D e treemaps  
  **Justificativa**:  
  - Permite detectar padrões e outliers nos dados de RFM de forma intuitiva  
  - Facilita análises cruzadas com cores e dimensões categóricas como segmento e tamanho da empresa  
  - Enriquecido com `hover_data`, marcadores de filtro (`add_vline`) e agrupamentos hierárquicos  
  
  ###### 4. Dispersão 3D para RFM  
  **Feature**: Gráfico tridimensional para combinar recência, frequência e valor  
  **Justificativa**:  
  - Oferece visão holística dos clientes em um só gráfico  
  - Identifica grupos estratégicos como clientes premium ou inativos com alto valor  
  - Ideal para apresentações e tomadas de decisão com stakeholders  
  
  ###### 5. Identificação de Clientes Inativos de Alto Valor  
  **Feature**: Ranking dos 10 principais clientes inativos com maior ticket médio  
  **Justificativa**:  
  - Gera leads para ações comerciais direcionadas  
  - Visual simplificado em gráfico de barras com destaque por segmento  
  - Facilita reativação de contas valiosas e aumento de receita  
  
  ###### 6. Segmentação Temporal com `pd.cut()`  
  **Feature**: Agrupamento de clientes por tempo desde o último pedido  
  **Justificativa**:  
  - Classifica automaticamente clientes em grupos (ativo, inativo, churn)  
  - Baseado em regras de negócio com faixas customizadas  
  - Alimenta a visualização em treemap para representar a base de clientes de forma hierárquica  
  
  ###### 7. Análise de Formas de Pagamento  
  **Feature**: Gráfico `sunburst` para distribuição de formas de pagamento por segmento  
  **Justificativa**:  
  - Identifica preferências de pagamento por perfil de cliente  
  - Suporte à tomada de decisão em políticas comerciais e negociações financeiras  
  
  ###### 8. Visualização de Dados Brutos e Exportação  
  **Feature**: Tabela de dados completa com opção para download em CSV  
  **Justificativa**:  
  - Proporciona transparência e validação dos dados apresentados  
  - Facilita exportação para análises externas e relatórios personalizados  
  - Interface amigável com `checkbox` para ativação opcional
 
  </details>
  
  <details>
  <summary><strong>Print da Página Análise RFM</strong></summary>
    
  ![Análise RFM](https://github.com/user-attachments/assets/9a77a81b-57ef-4481-99e2-15493adb73d0)

  </details>
</details>

---
<details>
<summary><strong>5.3.Tarefa 3 - Alteração do Modelo de Dados para Compras Compartilhadas</strong></summary>
 <br>
 <details>
 <summary><strong>SQL - DEMANDA OTIMIZADA</strong></summary>
  
   No arquivo [3.1-Query_criacao_compras_compartilhadas.sql](./queries/3-clientes_multiplos/3.1-Query_criacao_compras_compartilhadas.sql), é possível visualizar o script completo para a reestruturação do modelo de dados com suporte a pedidos com múltiplos clientes. Além disso, o arquivo [3.2-Query_visualizacao_completa.sql](./queries/3-clientes_multiplos/3.2-Query_visualizacao_completa.sql) apresenta uma visualização consolidada desses dados. Neles, estão presentes as melhorias aplicadas à demanda inicial. Sendo elas:
 
 ###### 1. Normalização da Relação N:N entre Pedidos e Clientes  
 **Melhoria**: Criação da tabela `pedido_clientes` para permitir associação de múltiplos clientes a um único pedido  
 **Justificativa**:  
 - Substitui a relação 1:N por uma N:N com chave composta (`id_pedido`, `id_cliente`)  
 - Permite rastrear participação proporcional de cada cliente no pedido via `percentual_participacao`  
 - Introduz campo `eh_responsavel_pagamento` para controle financeiro e gestão de cobrança  
 
 ###### 2. Migração Estruturada dos Dados Existentes  
 **Melhoria**: Conversão automatizada dos dados antigos para a nova estrutura de associação  
 **Justificativa**:  
 - Preserva os pedidos existentes com 100% de participação para o cliente original  
 - Evita perda de dados e mantém integridade referencial  
 
 ###### 3. Simulação de Cenários Realistas de Compartilhamento  
 **Melhoria**: Atribuição probabilística de múltiplos clientes por pedido para simular compras compartilhadas  
 **Justificativa**:  
 - Geração de dados com 60% pedidos individuais, 30% com 2 clientes e 10% com 3 clientes  
 - Aplicação de diferentes percentuais de participação (ex: 60/40 e 50/30/20) para realismo na análise  
 - Uso de CTEs para controle e clareza na geração dos dados  
 
 ###### 4. Indicador de Compartilhamento na Tabela de Pedidos  
 **Melhoria**: Inclusão do campo `eh_compartilhado` na tabela `pedidos`  
 **Justificativa**:  
 - Permite rápida identificação e segmentação de pedidos compartilhados  
 - Facilita análises e filtros em dashboards ou relatórios SQL  
 
 ###### 5. Consulta Agregada com Participantes por Pedido  
 **Melhoria**: Query final com `JOINs` e `STRING_AGG` para exibir clientes e participações por pedido  
 **Justificativa**:  
 - Apresenta visão consolidada dos pedidos e seus participantes de forma clara e organizada  
 - Permite validar corretamente os dados migrados e simulados
 </details>

<details>
  <summary><strong>PYTHON - DEMANDA OTIMIZADA</strong></summary>
  
  O script [pedidos_compartilhados.py](./src/analytics/pedidos_compartilhados.py) está a análise especializada em transações com múltiplos participantes.
    
  ###### 1. **KPIs Estratégicos**
  - **Feature**:
  - Total de pedidos compartilhados
  - Média de participantes por pedido
  - Valor médio das transações
  - **Justificativa**: Fornece uma visão instantânea do volume e importância dessas transações

  ###### 2. **Evolução Temporal**
  - **Feature**: Gráfico de linhas mostrando a variação mensal de pedidos
  - **Justificativa**: Identifica tendências e sazonalidade nas compras conjuntas
  
  ###### 3. **Distribuição de Participantes**
  - **Feature**: Gráfico de pizza mostrando proporção de pedidos por quantidade de participantes
  - **Justificativa**: Revela o padrão de compartilhamento mais comum
  
  ###### 4. **Top Clientes Principais**
  - **Feature**: Ranking dos 10 clientes que mais iniciam pedidos compartilhados
  - **Justificativa**: Identifica os líderes naturais de compras coletivas
  
  ###### 5. **Tabela Detalhada**
  - **Feature**: Listagem completa com todos os pedidos e participantes
  - **Justificativa**: Permite análise granular caso a caso

 </details>
 
  <details>
  <summary><strong>Print da Tabela `pedidos_clientes` </strong></summary>
      
  ![tabela_pedidos_clientes](https://github.com/user-attachments/assets/d128bfdc-3092-4718-9a64-64325d9b8a05)

  </details>
  
  <details>
  <summary><strong>Print da Página de Pedidos Compartilhados </strong></summary>
      
   ![Análise de Pedidos Compartilhados](https://github.com/user-attachments/assets/3df48609-080d-4a34-bd7c-4b50f75f34d1)

  </details> 
</details>

---
<details>
<summary><strong>5.4.Tarefa 4 - Top 5 Produtos Mais Rentáveis no Último Ano</strong></summary>
 <br>
 <details>
 <summary><strong>SQL - DEMANDA OTIMIZADA</strong></summary>
  
   No arquivo [4-Query_CTE_Produtos_Rentaveis.sql](./queries/2-clientes_individuais/4-Query_CTE_Produtos_Rentaveis.sql) é possível visualizar o script completo para calcular os 5 produtos mais rentáveis do último ano.  
  Nele, estão presentes as melhorias aplicadas à demanda inicial. Sendo elas:
  
  ###### 1. Cálculo de Receita Total por Produto com CTE  
  **Melhoria**: Utilização de Common Table Expressions (CTE) para calcular a receita total por produto e calcular o percentual de contribuição de cada produto para a receita geral  
  **Justificativa**:  
  - Organiza o cálculo em etapas lógicas, facilitando a manutenção e a leitura  
  - A CTE `receita_geral` calcula a receita total de todos os pedidos concluídos, garantindo que o cálculo da rentabilidade dos produtos seja feito com base na receita total correta  
  - O uso de `COALESCE` assegura que valores nulos sejam tratados como zero, evitando resultados errôneos  
  - A utilização de `DENSE_RANK()` permite classificar os produtos de maneira eficiente, facilitando a extração dos 5 produtos mais rentáveis
  </details>
 <details>
  
 <summary><strong>PYTHON - DEMANDA OTIMIZADA</strong></summary>
 
 No arquivo [top_produtos.py](./scr/analytics/5-top5_produtos_rentaveis/top_produtos.py) é possível visualizar o script em Python que utiliza Streamlit e Plotly para exibir visualmente os 5 produtos mais rentáveis.  
 Nele, estão presentes as seguintes features:
 
 ###### 1. Exibição de KPIs Principais  
 **Feature**: Exibição de indicadores chave de performance (KPIs) para o usuário, incluindo "Total de Produtos", "Receita Total Geral", "Receita Top 5" e outros detalhes importantes  
 **Justificativa**:  
 - Apresenta as métricas mais relevantes de forma clara e acessível  
 - Permite ao usuário visualizar rapidamente a contribuição dos 5 produtos mais rentáveis em relação ao total de receita
 
 ###### 2. Visualização Interativa com Gráficos  
 **Feature**: Utilização de gráficos interativos, como o gráfico de barras (ranking de rentabilidade) e o gráfico de sunburst (distribuição por categoria)  
 **Justificativa**:  
 - Gráficos interativos tornam os dados mais acessíveis e dinâmicos, permitindo ao usuário explorar as informações de maneira mais intuitiva  
 - O gráfico de barras facilita a comparação dos produtos mais rentáveis, enquanto o gráfico de sunburst ajuda a visualizar a distribuição de receita entre categorias e subcategorias
 
 ###### 3. Exibição de Detalhes Expansíveis por Produto  
 **Feature**: Utilização do componente `st.expander` para permitir que o usuário veja detalhes adicionais sobre cada produto, como unidades vendidas, preço médio e percentual da receita geral  
 **Justificativa**:  
 - Oferece uma maneira compacta de acessar informações detalhadas sem sobrecarregar a interface  
 - Permite ao usuário explorar dados específicos sobre cada produto de forma organizada
 
 ###### 4. Relação entre Preço Médio e Unidades Vendidas  
 **Feature**: Gráfico de dispersão que relaciona o preço médio dos produtos com a quantidade de unidades vendidas  
 **Justificativa**:  
 - Ajuda a identificar padrões, como produtos com preços altos e grandes volumes de vendas, ou produtos com preços baixos, mas alta rentabilidade  
 - Fornece uma visão estratégica para decisões de precificação e vendas
 
 ###### 5. Download de Dados Brutos  
 **Feature**: Possibilidade de baixar os dados completos como arquivo CSV  
 **Justificativa**:  
 - Permite ao usuário realizar uma análise mais profunda dos dados fora da plataforma  
 - Facilita a exportação dos dados para relatórios ou outras ferramentas de análise
 </details>

 <details>
 <summary><strong>Print da Análise dos Top 5 produtos mais Rentáveis (Último ANO)</strong></summary>
  
 ![Análise Top 5](https://github.com/user-attachments/assets/9f3b4f6e-a9c6-43d8-827c-fa437bf93f76)

 </details>
</details>

---
<details>
<summary><strong>5.5.Tarefa 5 - Análise de Tendências de Vendas no Último Ano</strong></summary>
 <br>
 <details>
 <summary><strong>SQL - DEMANDA OTIMIZADA</strong></summary>
 
   No arquivo [5-Query_CTE_Tendencias_Vendas.sql](./queries/2-clientes_individuais/5-Query_CTE_Tendencias_Vendas.sql) é possível visualizar o script completo para calcular a análise de tendências de vendas no último ano.  
 Nele, estão presentes as melhorias aplicadas à demanda inicial. Sendo elas:
 
 ###### 1. CTE (Common Table Expressions)  
 **Melhoria**: Uso de CTE para organizar as etapas de cálculo, garantindo clareza e modularidade no código.  
 **Justificativa**:  
 - Organiza o código em blocos lógicos, tornando mais fácil a manutenção e a leitura  
 - A utilização de CTEs permite dividir o processo de agregação e análise de forma clara e eficaz, facilitando a compreensão dos cálculos realizados.
 
 ###### 2. Função de Janela - `LAG()`  
 **Melhoria**: Utilização da função `LAG()` para calcular o crescimento percentual de vendas em comparação ao mês anterior.  
 **Justificativa**:  
 - O uso de `LAG()` permite comparar o valor de vendas de um mês com o anterior de forma eficiente  
 - Essa comparação possibilita o cálculo do crescimento percentual, importante para a análise de tendências ao longo do tempo.
 
 ###### 3. Formatação de Data com `TO_CHAR()`  
 **Melhoria**: Formatação da data no formato 'YYYY-MM' para análise mensal.  
 **Justificativa**:  
 - A função `TO_CHAR()` permite agrupar as vendas por mês, fazendo com que os dados possam ser analisados de maneira temporal (mensal), facilitando a análise de tendências ao longo do tempo.
 
 ###### 4. Cálculo do Crescimento Percentual Seguro  
 **Melhoria**: Cálculo do crescimento percentual de forma robusta, tratando casos onde o mês anterior pode ter vendas nulas ou iguais a zero.  
 **Justificativa**:  
 - Garantir que o cálculo do crescimento percentual seja feito de forma segura e sem causar erros em casos de dados faltantes ou zero, evitando inconsistências nos resultados.
 
 ###### 5. Forma de Pagamento Mais Comum  
 **Melhoria**: Subconsulta para identificar a forma de pagamento mais utilizada em cada mês.  
 **Justificativa**:  
 - Essa informação ajuda a entender o comportamento de compra do cliente ao longo do tempo, o que pode ser útil para estratégias de marketing ou ajustes nos métodos de pagamento.
 
 ###### 6. Resultado Final com Status de Dados  
 **Melhoria**: Inclusão de uma verificação para garantir que a consulta retorne dados e indique se há ou não pedidos no período.  
 **Justificativa**:  
 - A verificação do status de dados assegura que o usuário saiba se os dados estão disponíveis ou se não há pedidos no período analisado, ajudando a evitar confusões na análise.
 </details>
 
 <details>
 <summary><strong>PYTHON - DEMANDA OTIMIZADA</strong></summary>
 
   No arquivo [tendencia_vendas.py](./scr/analytics/tendencia_vendas.py) é possível visualizar o script em Python que utiliza Streamlit e Plotly para exibir visualmente as tendências de vendas.  
 Nele, estão presentes as seguintes features:
 
 ###### 1. Carregamento de Dados com `run_query()`  
 **Feature**: O código carrega os dados da consulta SQL usando a função `run_query()` para obter as informações em formato de DataFrame.  
 **Justificativa**:  
 - A separação entre a consulta SQL e a lógica Python melhora a manutenção do código e facilita a reutilização da consulta em diferentes contextos.
 
 ###### 2. Tratamento de Dados e Verificação de Colunas  
 **Feature**: Verificação se todas as colunas necessárias estão presentes e tratamento de dados para garantir que as colunas numéricas sejam convertidas corretamente.  
 **Justificativa**:  
 - Garantir que os dados estejam formatados corretamente antes de serem analisados ou exibidos  
 - A verificação das colunas ajuda a evitar erros de execução e garante que as métricas essenciais sejam calculadas corretamente.
 
 ###### 3. Exibição de KPIs  
 **Feature**: Exibição de KPIs importantes como "Último Mês", "Vendas Último Mês", "Crescimento", "Clientes Ativos", entre outros.  
 **Justificativa**:  
 - KPIs fornecem informações rápidas e resumidas sobre a performance do mês mais recente, ajudando na análise estratégica das vendas.
 
 ###### 4. Cálculo de Média Móvel de 3 Meses  
 **Feature**: Cálculo da média móvel de 3 meses para suavizar as flutuações mensais e obter uma visão mais estável da tendência de vendas.  
 **Justificativa**:  
 - A média móvel de 3 meses é uma técnica comum para identificar tendências de longo prazo e reduzir a volatilidade dos dados mensais.
 
 ###### 5. Gráfico de Tendência de Vendas  
 **Feature**: Exibição de um gráfico de linha interativo que mostra a evolução das vendas mensais, incluindo a média móvel.  
 **Justificativa**:  
 - A visualização gráfica facilita a interpretação das tendências ao longo do tempo, permitindo que o usuário identifique facilmente períodos de crescimento ou queda nas vendas.
 
 ###### 6. Gráfico de Crescimento Percentual  
 **Feature**: Exibição de barras de crescimento percentual, com uma linha de referência zero para facilitar a comparação entre meses.  
 **Justificativa**:  
 - A representação visual do crescimento percentual ajuda a entender as variações nas vendas de um mês para outro e facilita a identificação de períodos de alto ou baixo crescimento.
 
 ###### 7. Comparativo de Desempenho Multidimensional  
 **Feature**: Gráfico de dispersão interativo que compara várias dimensões de desempenho, como vendas, pedidos e crescimento percentual, ao mesmo tempo.  
 **Justificativa**:  
 - A análise multidimensional permite uma compreensão mais abrangente das tendências, fornecendo uma visão completa de como diferentes fatores impactam as vendas.
 
 ###### 8. Distribuição de Métricas Mensais com Boxplots  
 **Feature**: Boxplots para visualizar a distribuição de vendas, pedidos, ticket médio e clientes ativos ao longo dos meses.  
 **Justificativa**:  
 - Os boxplots ajudam a visualizar a dispersão dos dados e identificar outliers, oferecendo insights sobre a variação dos dados de maneira clara e eficiente.
 
 ###### 9. Formas de Pagamento ao Longo do Tempo  
 **Feature**: Gráfico de barras mostrando as formas de pagamento mais utilizadas ao longo do tempo.  
 **Justificativa**:  
 - A análise das formas de pagamento ajuda a entender o comportamento do consumidor, o que pode ser útil para decisões estratégicas, como quais formas de pagamento promover mais.
 
 ###### 10. Opção de Download de Dados  
 **Feature**: Possibilidade de o usuário baixar os dados brutos em formato CSV.  
 **Justificativa**:  
 - Oferecer a opção de download facilita a análise externa dos dados e permite ao usuário realizar mais profundidade em seus próprios estudos ou relatórios.
 </details>
 
 <details>
 <summary><strong>Print da Página de Tedência de Vendas Mensais</strong></summary>

 ![Análise Tendência](https://github.com/user-attachments/assets/ecc0936e-0aea-4e8b-b4f1-8038e69b3718)

 </details>
</details>

---
<details>
<summary><strong>5.6.Tarefa 6 - Identificação de Clientes Inativos</strong></summary>
 <br>
 <details>
 <summary><strong>SQL - DEMANDA OTIMIZADA</strong></summary>
  
   No arquivo [6-Query_CTE_Clientes_Inativos.sql](./queries/6-Query_CTE_Clientes_Inativos.sql) está o script SQL que identifica os clientes que não realizaram pedidos nos últimos 6 meses.  
  O script apresenta as melhorias realizadas para otimizar a consulta.
  
  ###### 1. CTE (Common Table Expressions)  
  **Melhoria**: Uso de CTE para calcular a data do último pedido de cada cliente.  
  **Justificativa**:  
  - Organiza a consulta em uma estrutura lógica e modular  
  - Facilita a leitura e a manutenção do código
  - Permite cálculo preciso da inatividade considerando apenas pedidos entregues
  
  ###### 2. Função de Janela - `MAX()`  
  **Melhoria**: Utilização da função `MAX()` para calcular a data do último pedido realizado pelo cliente.  
  **Justificativa**:  
  - Identifica precisamente a última interação do cliente
  - Filtra pedidos compartilhados para análise individual
  
  ###### 3. Classificação de Status  
  **Melhoria**: Categorização em:
  - "Nunca comprou" (sem pedidos)
  - "Inativo há mais de 6 meses" 
  - "Ativo" (compras recentes)
  
  **Justificativa**:  
  - Segmentação clara para estratégias de recuperação
  - Diferenciação entre leads nunca convertidos e clientes inativos
  
  ###### 4. Cálculo de Dias de Inatividade  
  **Melhoria**: Diferença em dias entre a data atual e último pedido  
  **Justificativa**:  
  - Métrica quantitativa para priorização
  - Base para filtros interativos no dashboard
 </details>
 
 <details>
  <summary><strong>PYTHON - DASHBOARD INTERATIVO</strong></summary>
  
   No arquivo [clientes_inativos.py](./src/analytics/clientes_inativos.py) está o script em Python que utiliza Streamlit e Plotly para análise avançada.

 ###### 1. Análise Quantitativa  
 **Feature**: 
 - 8 KPIs estratégicos (total, inatividade média, potencial de recuperação)
 - Cálculo de valor potencial estimado (R$ 1.500/cliente)  
 **Justificativa**:  
 - Visão executiva imediata do impacto
 - Priorização por potencial de retorno

 ###### 2. Filtros Avançados  
 **Feature**: 
 - Filtro combinado por status + segmento + faixa de dias
 - Detecção automática de valores únicos  
 **Justificativa**:  
 - Análise segmentada por perfil de cliente
 - Flexibilidade para diferentes cenários

 ###### 3. Visualizações Integradas  
 **Feature**: 4 abas com:
 1. Distribuição (status/segmento)
 2. Análise temporal (mensal/trimestral)
 3. Mapa geográfico interativo
 4. Detalhamento por cliente  
 **Justificativa**:  
 - Análise multivariada em um único painel
 - Identificação de padrões regionais e temporais

 ###### 4. Detalhamento Ação  
 **Feature**: 
 - Top 10 clientes prioritários (maior inatividade)
 - Amostra aleatória de leads não convertidos
 - Linha do tempo interativa  
 **Justificativa**:  
 - Foco em oportunidades específicas
 - Visualização do histórico por cliente

 ###### 5. Exportação Inteligente  
 **Feature**: 
 - Download dos dados filtrados em CSV
 - Formatação condicional nos dados exibidos  
 **Justificativa**:  
 - Integração com outras ferramentas
 - Dados prontos para ações de CRM

 ###### 6. Tratamento de Edge Cases  
 **Feature**: 
 - Verificação de dados vazios
 - Adaptação automática para pequenas amostras
 - Fallbacks para visualizações não disponíveis  
 **Justificativa**:  
 - Robustez em diferentes cenários
 - Experiência do usuário consistente
 </details>

 <details>
 <summary><strong>Print da Página de Análise de Clientes Inativos</strong></summary>

 ![Análise cliente Distribuição](https://github.com/user-attachments/assets/13d656d8-ba3f-4c55-9d47-84ca882a01e0)

 </details>

 <details>
 <summary><strong>Análise Temporal</strong></summary>

 ![Análise cliente Temporal](https://github.com/user-attachments/assets/91c97c10-f72b-4086-9381-d8abd3e86c2a)

 </details>

 <details>
 <summary><strong>Análise Geográfica</strong></summary>

  ![Análise cliente Geográfica](https://github.com/user-attachments/assets/b11a0348-2240-4d4e-bec2-fe2bcf461304)

 </details>

  <details>
 <summary><strong>Análise Detalhada</strong></summary>

  ![Análise cliente Detalhes](https://github.com/user-attachments/assets/82036bd7-f1e3-4ea2-996f-336bd862a23c)

 </details> 

</details>
 
---
<details>
<summary><strong>5.7.Tarefa 7 - Detecção de Anomalias em Vendas</strong></summary>
 <br>
 
 <details>
 <summary><strong>SQL - DEMANDA OTIMIZADA</strong></summary>
 
   No arquivo [7-Query_CTE_Anomalias_Vendas.sql](./queries/2-clientes_individuais/7-Query_CTE_Anomalias_Vendas.sql) está o script SQL que encontra pedidos onde o valor total registrado não bate com a soma dos itens (itens_pedido.quantidade * preco_unitario).
 
 ###### 1. CTE (Common Table Expressions)  
 **Melhoria**: Utilização de uma CTE chamada `calculo_valor_pedidos` para calcular a diferença entre o valor registrado no pedido e o valor calculado com base nos itens.  
 **Justificativa**:  
 - A CTE facilita a organização do código, separando a parte de cálculo da diferença dos valores e agrupando a consulta para identificar as anomalias.
 
 ###### 2. Cálculo da Diferença Absoluta e Percentual  
 **Melhoria**: O cálculo da diferença absoluta entre o valor total registrado e o valor calculado (itens_pedido.quantidade * preco_unitario) e a diferença percentual com tratamento de divisão por zero.  
 **Justificativa**:  
 - A diferença absoluta permite entender a discrepância em termos de valor monetário, enquanto a diferença percentual ajuda a identificar discrepâncias em termos relativos.
 
 ###### 3. Identificação de Anomalias com Base nas Diferenças  
 **Melhoria**: Inclusão de um `CASE` para categorizar as discrepâncias entre os valores como "Valor correto", "Disparidade Pequena", "Disparidade Moderada" ou "Disparidade Grande".  
 **Justificativa**:  
 - Isso permite que a análise seja mais granular, ajudando a priorizar a investigação de anomalias com maior discrepância.
 
 ###### 4. Filtragem de Anomalias  
 **Melhoria**: A consulta filtra os pedidos em que o valor total registrado e o valor calculado são diferentes, considerando também casos onde um dos valores é zero e o outro é diferente de zero.  
 **Justificativa**:  
 - Essa filtragem assegura que estamos analisando apenas os casos de discrepâncias reais, como a ausência de valores registrados ou cálculos errôneos.
</details>

 <details>
 <summary><strong>PYTHON - DEMANDA OTIMIZADA</strong></summary>
 
   No arquivo [anomalias_vendas.py](./src/analytics/anomalias_vendas.py) está o script em Python que utiliza Streamlit e Plotly para exibir a análise de anomalias em vendas.
 
 ###### 1. Carregamento de Dados com `run_query()`  
 **Feature**: O código carrega os dados da consulta SQL usando a função `run_query()` para obter as informações em formato de DataFrame.  
 **Justificativa**:  
 - A separação entre a consulta SQL e a lógica Python melhora a manutenção do código e facilita a reutilização da consulta em diferentes contextos.
 
 ###### 2. Cálculo de Diferença e Severidade  
 **Feature**: O código calcula a diferença entre o valor total registrado e o valor calculado, além de categorizar as anomalias com base na severidade (pequena, moderada ou grande).  
 **Justificativa**:  
 - A categorização da severidade ajuda a priorizar a análise de anomalias mais significativas, permitindo uma ação mais direcionada.
 
 ###### 3. Exibição de KPIs  
 **Feature**: Exibição de KPIs importantes, como o número total de anomalias, a quantidade de pedidos com disparidade pequena, moderada ou grande.  
 **Justificativa**:  
 - Esses KPIs fornecem uma visão rápida sobre a gravidade das discrepâncias, ajudando a monitorar o impacto das anomalias nos pedidos.
 
 ###### 4. Filtros de Severidade e Valor  
 **Feature**: Filtros interativos que permitem selecionar a severidade das discrepâncias (pequena, moderada, grande) e o intervalo de valores das diferenças.  
 **Justificativa**:  
 - O uso de filtros interativos proporciona flexibilidade ao usuário, permitindo refinar a análise e visualizar apenas os pedidos mais críticos.
 
 ###### 5. Visualização de Disparidades por Severidade  
 **Feature**: Exibição de gráficos de barras e pizza para mostrar a distribuição das anomalias por severidade e a comparação entre os valores registrados e calculados.  
 **Justificativa**:  
 - A visualização gráfica facilita a identificação de padrões e facilita a compreensão do impacto das anomalias.
 
 ###### 6. Detalhamento de Anomalias  
 **Feature**: Tabela com os detalhes dos pedidos que apresentaram discrepâncias, exibindo os valores registrados e calculados.  
 **Justificativa**:  
 - O detalhamento permite que o usuário visualize diretamente os pedidos problemáticos, facilitando a correção e acompanhamento.
 
 ###### 7. Exportação de Dados  
 **Feature**: Opção de download dos dados filtrados em formato CSV.  
 **Justificativa**:  
 - A exportação de dados facilita a análise externa e permite que o usuário utilize os dados para relatórios ou outras análises detalhadas.
 </details>

 <details>
 <summary><strong>Print da Página de Análise de Anomalias de Vendas</strong></summary>
    
 ![Análise Anomalias](https://github.com/user-attachments/assets/b00d97fd-0693-4a33-93a7-c917a64136b7)

 </details>
</details>

---
<details>
  <summary><strong>5.9.Tarefa 9 - Apresentação dos Dados</strong></summary>
  <br>
  <details>
    <summary><strong>PYTHON - DEMANDA OTIMIZADA</strong></summary>
    
  No arquivo [app.py](./app.py) está o dashboard principal que integra análises de dados de clientes e vendas, desenvolvido com Streamlit.
  
  ###### 1. **Navegação Hierárquica Intuitiva**
  - **Feature**: Sistema de seleção em dois níveis (tipo de análise > análise específica)
  - **Justificativa**: Organiza as funcionalidades de forma lógica e reduz a sobrecarga de opções
  
  ###### 2. **Análises Individuais Avançadas**
  - **Feature**:
    - RFM (Recência, Frequência, Valor)
    - Top produtos
    - Tendências temporais
    - Detecção de anomalias
  - **Justificativa**: Permite entender profundamente o comportamento individual de cada cliente
  
  ###### 3. **Análises de Pedidos Compartilhados**
  - **Feature**:
    - Visualização de participação percentual
    - Identificação de clientes frequentes em compras conjuntas
    - KPIs de valor compartilhado
  - **Justificativa**: Atende casos de uso complexos com múltiplos participantes
  
  ###### 4. **Visualização de Dados Interativa**
  - **Feature**:
    - Gráficos dinâmicos com Plotly
    - KPIs em tempo real
    - Tabelas detalhadas
  - **Justificativa**: Transforma dados complexos em insights acionáveis
  
  ###### 5. **Infraestrutura Técnica**
  - **Feature**:
    - Conexão direta com PostgreSQL
    - Cache inteligente de queries
    - Design responsivo
  - **Justificativa**: Garante performance e atualização em tempo real
  
  ###### 6. **Experiência do Usuário**
  - **Feature**:
    - Tema visual personalizado
    - Layout otimizado
    - Navegação simplificada
  - **Justificativa**: Aumenta a produtividade na análise diária
    
  </details>

  <details>
   <summary><strong>Print da SideBar Análises Individuais</strong></summary>
  
  ![Análises Individuais](https://github.com/user-attachments/assets/65f545f5-c635-4c2a-a72d-9809ed0acd27)

  </details>

  <details>
   <summary><strong>Print da SideBar Análises Compartilhadas</strong></summary>
  
  ![Análises Compartilhadas](https://github.com/user-attachments/assets/03a8f8ab-1530-4bf6-ae63-16505c312f63)

  </details>

  
</details>

---
<details>
  <summary><strong>5.10.Tarefa 10 - Análise Exploratória com Pandas e Matplotlib</strong></summary>
  
  Também utilizou-se o `Plotly`. Todos os prints referentes a essa tarefa estão diluídos nas tarefas 5.2-5.7
    
  </details>
</details>

---
