import streamlit as st
import plotly.express as px
import pandas as pd
from src.utils.query_runner import run_query
from dateutil.relativedelta import relativedelta
from datetime import datetime

def render():
    st.header("🏆 Top 5 Produtos Mais Rentáveis (Último Ano)")
    
    st.divider()

    st.subheader("📌 KPIs Principais")
    col1, col2, col3, col4 = st.columns(4)
    col5, col6, col7, col8 = st.columns(4)
    
    st.divider()

    # Carrega todos os dados
    df = run_query("4-Query_CTE_Produtos_Rentaveis.sql")
    
    # Cálculos dos KPIs
    receita_total_geral = df['receita_total_geral'].iloc[0] if len(df) > 0 else 0
    total_receita_top5 = df['receita_total'].sum() if len(df) > 0 else 0
    percentual_top5 = (total_receita_top5 / receita_total_geral * 100) if receita_total_geral > 0 else 0
    
    with col1:
        st.metric("Total de Produtos", len(df))
    
    with col2:
        st.metric("Receita Total Geral", f"R${receita_total_geral:,.2f}")
    
    with col3:
        st.metric("Receita Top 5", f"R${total_receita_top5:,.2f}", 
                 f"{percentual_top5:.1f}% do total")
    
    with col4:
        if len(df) > 0:
            top_produto = df.iloc[0]
            st.metric("Produto #1", top_produto['nome'], 
                     f"R${top_produto['receita_total']:,.2f}")
        else:
            st.metric("Produto #1", "N/D")
    
    with col5:
        if len(df) > 0:
            st.metric("Total Itens Vendidos", f"{df['unidades_vendidas'].sum():,}")
    
    with col6:
        if len(df) > 0:
            st.metric("Preço Médio Geral", f"R${df['preco_medio'].mean():,.2f}")
    
    with col7:
        if len(df) > 0:
            st.metric("Pedidos com Top 5", f"{df['qtd_pedidos'].sum():,}")

    with col8:
        if len(df) > 0:
            produto_mais_vendido = df.loc[df['unidades_vendidas'].idxmax()]
            st.metric("Mais Vendido (Qtd.)", produto_mais_vendido['nome'], 
                     f"{produto_mais_vendido['unidades_vendidas']:,} un.")
        else:
            st.metric("Mais Vendido (Qtd.)", "N/D")
    
    # Gráfico 1 - Ranking de rentabilidade
    if len(df) > 0:
        fig1 = px.bar(
            df,
            x="receita_total",
            y="nome",
            orientation='h',
            title="Top 5 Produtos por Receita",
            labels={"receita_total": "Receita Total (R$)", "nome": "Produto"},
            color="ranking_rentabilidade",
            color_continuous_scale="tealrose",
            hover_data=["categoria", "subcategoria", "percentual_receita"]
        )
        fig1.update_layout(yaxis={'categoryorder':'total ascending'})
        st.plotly_chart(fig1, use_container_width=True)
    else:
        st.warning("Nenhum dado disponível para o período selecionado.")

    st.divider()

    # Gráfico 2 - Distribuição por categoria
    if len(df) > 0:
        st.subheader("📊 Distribuição por Categoria")
        fig2 = px.sunburst(
            df,
            path=['categoria', 'subcategoria', 'nome'],
            values='receita_total',
            title="Distribuição de Receita por Categoria e Subcategoria",
            hover_data=['percentual_receita']
        )
        st.plotly_chart(fig2, use_container_width=True)
    else:
        st.warning("Nenhum dado disponível para o período selecionado.")
  
    # Expansível com detalhes dos produtos
    if len(df) > 0:
        with st.expander("🔍 Ver Detalhes por Produto"):
            for _, row in df.iterrows():
                st.markdown(f"""
                    **{row['nome']}**  
                    - Categoria: {row['categoria']} ({row['subcategoria']})  
                    - Receita Total: R$ {row['receita_total']:,.2f}  
                    - % da Receita Geral: {row['percentual_receita']}%  
                    - Pedidos: {row['qtd_pedidos']}  
                    - Unidades Vendidas: {row['unidades_vendidas']}  
                    - Preço Médio: R$ {row['preco_medio']:,.2f}  
                    - Ranking: #{row['ranking_rentabilidade']}  
                    ---
                """)
    
    st.divider()

    # Gráfico 3 - Relação entre preço médio e unidades vendidas
    if len(df) > 0:
        st.subheader("📈 Relação Preço x Volume")
        fig3 = px.scatter(
            df,
            x="preco_medio",
            y="unidades_vendidas",
            size="receita_total",
            color="categoria",
            hover_name="nome",
            title="Relação entre Preço Médio e Unidades Vendidas",
            labels={
                "preco_medio": "Preço Médio (R$)",
                "unidades_vendidas": "Unidades Vendidas",
                "receita_total": "Receita Total"
            }
        )
        st.plotly_chart(fig3, use_container_width=True)

    st.divider()

    if st.checkbox("Mostrar dados brutos"):
        st.subheader("📋 Dados Completos")
        st.dataframe(df if len(df) > 0 else pd.DataFrame())
        
        if len(df) > 0:
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="Baixar dados como CSV",
                data=csv,
                file_name='top_produtos_rentaveis.csv',
                mime='text/csv',
                help="Clique para baixar os dados completos em formato CSV"
            )

if __name__ == "__main__":
    render()