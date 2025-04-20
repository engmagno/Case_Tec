import streamlit as st
from src.analytics import (
    rfm_analysis, 
    top_produtos, 
    tendencia_vendas, 
    clientes_inativos, 
    anomalias_vendas,
    pedidos_compartilhados
)

tema = {
    "primaryColor": "#FF4B4B",
    "backgroundColor": "#FFFFFF",
    "secondaryBackgroundColor": "#F0F2F6",
    "textColor": "#31333F",
    "font": "sans serif"
}

st.set_page_config(
    page_title="Dashboard de Clientes", 
    layout="wide", 
    initial_sidebar_state="expanded",
)

st._config.set_option("theme", tema)

st.title("Dashboard - Análises de Dados do Banco")

# Sidebar
with st.sidebar:
    st.markdown("### 🔍 Tipo de Análise")
    tipo_analise = st.selectbox(
        "Selecione o tipo de análise:",
        ["Análises Individuais", "Análises Compartilhadas"]
    )
    
    st.markdown("---")
    
    if tipo_analise == "Análises Individuais":
        st.markdown("### 🧍‍♂️ Análises de Compras Individuais")
        aba = st.selectbox("Escolha uma análise individual:", [
            "Análise de Recência, Frequência e Valor (RFM)", 
            "Top 5 Produtos Mais Rentáveis (Último Ano)",
            "Análise de Tendência de Vendas Mensal",
            "Análise de Clientes Inativos",
            "Análise de Anomalias em Vendas"
        ])
    else:
        st.markdown("### 👥 Análises de Compras Compartilhadas")
        aba_compartilhada = st.selectbox(
            "Escolha uma análise compartilhada:",
            ["Visão Geral de Pedidos Compartilhados", "(em breve)"]
        )

# Chamada das funções de análise
if tipo_analise == "Análises Individuais":
    if aba == "Análise de Recência, Frequência e Valor (RFM)":
        rfm_analysis.render()
    elif aba == "Top 5 Produtos Mais Rentáveis (Último Ano)":
        top_produtos.render()
    elif aba == "Análise de Tendência de Vendas Mensal":
        tendencia_vendas.render()
    elif aba == "Análise de Clientes Inativos":
        clientes_inativos.render()
    elif aba == "Análise de Anomalias em Vendas":
        anomalias_vendas.render()
else:
    if aba_compartilhada == "Visão Geral de Pedidos Compartilhados":
        pedidos_compartilhados.render()