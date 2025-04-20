import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from src.utils.query_runner import run_query
import pandas as pd

def render():
    st.header("📈 Análise de Recência, Frequência e Valor (RFM)")
    st.divider()
    
    # Carrega os dados
    df_rfm = run_query("2-Query_CTE_Rec_Feq_Valor.sql")
    
    # Seção de KPIs (agora no topo)
    st.subheader("📌 KPIs Principais")
    kpi1, kpi2, kpi3, kpi4, kpi5 = st.columns(5)
    
    with kpi1:
        total_clientes = len(df_rfm)
        st.metric("Total Clientes", f"{total_clientes:,}")
    
    with kpi2:
        ticket_medio = df_rfm['ticket_medio'].mean()
        st.metric("Ticket Médio", f"R${ticket_medio:,.2f}")
    
    with kpi3:
        freq_media = df_rfm['total_pedidos'].mean()
        st.metric("Frequência Média", f"{freq_media:.1f} pedidos")
    
    with kpi4:
        recencia_media = df_rfm['dias_desde_ultimo_pedido'].mean()
        st.metric("Recência Média", f"{recencia_media:.1f} dias")
        
    with kpi5:
        valor_total = (df_rfm['ticket_medio'] * df_rfm['total_pedidos']).sum()
        st.metric("Valor Total Clientes", f"R${valor_total:,.2f}")
    
    # Linha adicional de KPIs
    kpi6, kpi7, kpi8, kpi9, kpi10 = st.columns(5)
    
    with kpi6:
        clientes_ouro = len(df_rfm[df_rfm['ticket_medio'] > ticket_medio * 2])
        st.metric("Clientes Ouro", clientes_ouro, 
                 f"{clientes_ouro/total_clientes*100:.1f}%")
    
    with kpi7:
        clientes_inativos = len(df_rfm[df_rfm['dias_desde_ultimo_pedido'] > 90])
        st.metric("Clientes Inativos (>90d)", clientes_inativos,
                 f"{clientes_inativos/total_clientes*100:.1f}%")
    
    with kpi8:
        pedidos_totais = df_rfm['total_pedidos'].sum()
        st.metric("Total Pedidos", f"{pedidos_totais:,}")
        
    with kpi9:
        # Segmento mais comum
        segmento_mais_comum = df_rfm['segmento'].mode()[0]
        st.metric("Segmento Mais Comum", segmento_mais_comum)
        
    with kpi10:
        # Forma de pagamento mais recente mais comum
        forma_pagamento_comum = df_rfm['ultima_forma_pagamento'].mode()[0]
        st.metric("Forma Pagamento Mais Recente", forma_pagamento_comum)
    
    st.divider()

    # Seção de filtros
    st.subheader("🔍 Filtros")
    col1, col2, col3 = st.columns(3)
    with col1:
        dias_filtro = st.slider("Clientes inativos há mais de (dias):", 
                              min_value=0, max_value=365, value=30)
    with col2:
        min_pedidos = st.slider("Mínimo de pedidos:", 
                               min_value=1, max_value=int(df_rfm["total_pedidos"].max()), 
                               value=1)
    with col3:
        segmento_filtro = st.multiselect(
            "Segmento do Cliente:",
            options=df_rfm['segmento'].unique(),
            default=df_rfm['segmento'].unique()
        )
    
    df_filtrado = df_rfm[
        (df_rfm["dias_desde_ultimo_pedido"] > dias_filtro) & 
        (df_rfm["total_pedidos"] >= min_pedidos) &
        (df_rfm["segmento"].isin(segmento_filtro))
    ]
    
    st.divider()

    # Visualização 1: KPI Cards
    st.subheader("📊 Métricas Gerais")
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.metric("Total Clientes", len(df_rfm))
    with col2:
        st.metric("Clientes Inativos", len(df_filtrado), 
                 f"{len(df_filtrado)/len(df_rfm)*100:.1f}%")
    with col3:
        st.metric("Ticket Médio Geral", f"R${df_rfm['ticket_medio'].mean():.2f}")
    with col4:
        st.metric("Pedidos Médios", f"{df_rfm['total_pedidos'].mean():.1f}")
    with col5:
        st.metric("Tamanho Médio Empresa", df_rfm['tamanho_empresa'].mode()[0])
    
    st.divider()

    # Visualização 2: Gráfico de Recência
    st.subheader("📅 Distribuição de Recência (Dias desde último pedido)")
    fig_recencia = px.histogram(df_rfm, x="dias_desde_ultimo_pedido", 
                               nbins=30, 
                               title="Distribuição de Dias desde o Último Pedido",
                               labels={"dias_desde_ultimo_pedido": "Dias desde último pedido"},
                               color="segmento")
    fig_recencia.add_vline(x=dias_filtro, line_dash="dash", line_color="red",
                         annotation_text=f"Filtro: {dias_filtro} dias")
    st.plotly_chart(fig_recencia)
    
    st.divider()

    # Visualização 3: Gráfico de Frequência
    st.subheader("🔄 Distribuição de Frequência (Total de Pedidos)")
    fig_freq = px.histogram(df_rfm, x="total_pedidos", 
                           nbins=20,
                           title="Distribuição de Total de Pedidos por Cliente",
                           labels={"total_pedidos": "Total de Pedidos"},
                           color="tamanho_empresa")
    fig_freq.add_vline(x=min_pedidos, line_dash="dash", line_color="red",
                      annotation_text=f"Filtro: {min_pedidos} pedidos")
    st.plotly_chart(fig_freq)
    
    st.divider()

    # Visualização 4: Gráfico de Valor (Ticket Médio)
    st.subheader("💰 Distribuição de Valor (Ticket Médio)")
    fig_valor = px.box(df_rfm, y="ticket_medio", 
                      title="Distribuição do Ticket Médio",
                      labels={"ticket_medio": "Ticket Médio (R$)"},
                      color="segmento")
    st.plotly_chart(fig_valor)

    st.divider()
    
    # Visualização 5: Dispersão RFM (existente, mas aprimorada)
    st.subheader("🎯 Análise RFM - Dispersão 3D")
    fig_3d = px.scatter_3d(
        df_rfm,
        x="dias_desde_ultimo_pedido",
        y="total_pedidos",
        z="ticket_medio",
        color="segmento",
        hover_data=["nome", "tamanho_empresa", "ultima_forma_pagamento"],
        title="Relação entre Recência, Frequência e Valor",
        labels={
            "dias_desde_ultimo_pedido": "Recência (dias)",
            "total_pedidos": "Frequência",
            "ticket_medio": "Valor (R$)"
        },
        height=500
    )
    fig_3d.update_layout(
        scene=dict(
            xaxis_title='Recência (dias)',
            yaxis_title='Frequência (pedidos)',
            zaxis_title='Valor (R$)',
            camera=dict(eye=dict(x=1.5, y=1.5, z=0.8))
        ),
        margin=dict(l=0, r=0, b=0, t=30)
    )
    st.plotly_chart(fig_3d, use_container_width=True)

    st.divider()
    
    # Visualização 6: Top clientes inativos por valor
    if not df_filtrado.empty:
        st.subheader("🏆 Top Clientes Inativos por Valor")
        df_top = df_filtrado.sort_values("ticket_medio", ascending=False).head(10)
        fig_top = px.bar(df_top, 
                         x="nome", y="ticket_medio",
                         title="Top 10 Clientes Inativos por Ticket Médio",
                         labels={"nome": "Cliente", "ticket_medio": "Ticket Médio (R$)"},
                         text_auto=".2f",
                         color="segmento",
                         hover_data=["tamanho_empresa", "ultima_forma_pagamento"])
        st.plotly_chart(fig_top)
    
    st.divider()

    # Visualização 7: Treemap de segmentação RFM
    st.subheader("🌳 Segmentação RFM")
    df_rfm['segmento_recencia'] = pd.cut(df_rfm['dias_desde_ultimo_pedido'], bins=[0, 30, 90, 365, float('inf')], 
                               labels=['Ativo(0-30 dias)', 'Inativo Recente(31-90 dias)', 'Inativo(91-365 dias)', 'Churn(>365 dias)'])
    
    fig_treemap = px.treemap(df_rfm, path=['segmento', 'segmento_recencia', 'tamanho_empresa'], values='ticket_medio',
                            color='total_pedidos', hover_data=['nome', 'ultima_forma_pagamento'],
                            title='Segmentação de Clientes por RFM')
    st.plotly_chart(fig_treemap)

    st.divider()

    # Visualização 8: Formas de pagamento por segmento
    st.subheader("💳 Formas de Pagamento por Segmento")
    fig_pagamento = px.sunburst(df_rfm, path=['segmento', 'ultima_forma_pagamento'], 
                               title='Distribuição de Formas de Pagamento por Segmento')
    st.plotly_chart(fig_pagamento)

    st.divider()

    # Opcional: Mostrar dados brutos
    if st.checkbox("Mostrar dados brutos"):
        st.subheader("📋 Dados Completos")
        st.dataframe(df_rfm)

        csv = df_rfm.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Baixar dados como CSV",
            data=csv,
            file_name='rfm.csv',
            mime='text/csv'
        )