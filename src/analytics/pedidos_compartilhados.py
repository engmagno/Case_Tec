import streamlit as st
import pandas as pd
import plotly.express as px
from src.utils.query_runner_compartilhado import run_query

def render():
    st.header("Análise de Pedidos Compartilhados")
    
    st.divider()
    st.subheader("📌 KPIs Principais")

    # Carrega os dados da view
    df = run_query("3.2-Query_visualizacao_completa.sql")

    # KPIs principais
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Pedidos Compartilhados", df['id_pedido'].nunique())
    with col2:
        st.metric("Média de Participantes", round(df['total_participantes'].mean(), 1))
    with col3:
        st.metric("Valor Médio", f"R$ {round(df['valor_total'].mean(), 2)}")
    
    st.markdown("---")
    
    # Gráfico 1: Evolução temporal
    st.subheader("Evolução de Pedidos Compartilhados")
    df['data_pedido'] = pd.to_datetime(df['data_pedido'])
    df_mensal = df.groupby(pd.Grouper(key='data_pedido', freq='M')).agg(
        total_pedidos=('id_pedido', 'nunique'),
        valor_total=('valor_total', 'sum')
    ).reset_index()
    
    fig1 = px.line(df_mensal, x='data_pedido', y='total_pedidos',
                  title='Pedidos Compartilhados por Mês',
                  labels={'data_pedido': 'Mês', 'total_pedidos': 'Total de Pedidos'})
    st.plotly_chart(fig1, use_container_width=True)
    
    # Gráfico 2: Distribuição de participantes
    st.subheader("Distribuição de Participantes por Pedido")
    dist_participantes = df.groupby('total_participantes')['id_pedido'].nunique().reset_index()
    fig2 = px.pie(dist_participantes, values='id_pedido', names='total_participantes',
                 title='Proporção de Pedidos por Número de Participantes')
    st.plotly_chart(fig2, use_container_width=True)
    
    # Gráfico 3: Top clientes principais
    st.subheader("Top 10 Clientes Principais em Pedidos Compartilhados")
    top_clientes = df['cliente_principal'].value_counts().head(10).reset_index()
    fig3 = px.bar(top_clientes, x='cliente_principal', y='count',
                 labels={'cliente_principal': 'Cliente', 'count': 'Número de Pedidos'})
    st.plotly_chart(fig3, use_container_width=True)
    
    # Tabela detalhada
    st.subheader("Detalhes dos Pedidos Compartilhados")
    st.dataframe(df.sort_values('data_pedido', ascending=False), height=400)