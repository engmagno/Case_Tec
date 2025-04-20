import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from src.utils.query_runner import run_query

def render():
    st.header("🚨 Anomalias em Vendas")
    st.divider()

    # Carrega os dados
    df_anomalias = run_query("7-Query_CTE_Anomalias_Vendas.sql")

    if not df_anomalias.empty:
        # Conversão de tipos
        numeric_cols = ['valor_total_registrado', 'valor_calculado', 'diferenca_absoluta']
        for col in numeric_cols:
            df_anomalias[col] = pd.to_numeric(df_anomalias[col], errors='coerce')
        
        # Seção de métricas resumidas
        st.subheader("📌 KPIs Principais")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Anomalias", len(df_anomalias))
        with col2:
            st.metric("Maior Diferença", f"R$ {df_anomalias['diferenca_absoluta'].max():,.2f}")
        with col3:
            st.metric("Diferença Média", f"R$ {df_anomalias['diferenca_absoluta'].mean():,.2f}")
        with col4:
            total_disparidade = df_anomalias['diferenca_absoluta'].sum()
            st.metric("Total Disparidade", f"R$ {total_disparidade:,.2f}")

        # Segunda linha de KPIs
        col5, col6, col7, col8 = st.columns(4)
        with col5:
            st.metric("Pedidos Corretos", 
                     len(df_anomalias[df_anomalias['severidade'] == 'Valor correto']))
        with col6:
            st.metric("Pequenas Disparidades", 
                     len(df_anomalias[df_anomalias['severidade'] == 'Disparidade Pequena ']))
        with col7:
            st.metric("Disparidades Moderadas", 
                     len(df_anomalias[df_anomalias['severidade'] == 'Disparidade Moderada']))
        with col8:
            st.metric("Grandes Disparidades", 
                     len(df_anomalias[df_anomalias['severidade'] == 'Disparidade Grande']))

        st.divider()

        # Filtros
        st.subheader("🔍 Filtros")
        col_f1, col_f2, col_f3 = st.columns(3)
        
        with col_f1:
            severidade_opcoes = df_anomalias["severidade"].unique().tolist()
            severidade_selecionada = st.multiselect(
                "Severidade:", 
                severidade_opcoes, 
                default=severidade_opcoes
            )
        
        with col_f2:
            forma_pagamento_opcoes = ['Todas'] + df_anomalias["forma_pagamento"].unique().tolist()
            forma_pagamento_selecionada = st.selectbox("Forma de Pagamento:", forma_pagamento_opcoes)
        
        with col_f3:
            diferenca_range = st.slider(
                "Faixa de Diferença (R$):", 
                min_value=0, 
                max_value=int(df_anomalias["diferenca_absoluta"].max()) + 10, 
                value=(0, int(df_anomalias["diferenca_absoluta"].max()) + 10)
            )

        # Aplica filtros
        df_filtrado = df_anomalias[df_anomalias["severidade"].isin(severidade_selecionada)]
        
        if forma_pagamento_selecionada != 'Todas':
            df_filtrado = df_filtrado[df_filtrado["forma_pagamento"] == forma_pagamento_selecionada]
        
        df_filtrado = df_filtrado[
            (df_filtrado["diferenca_absoluta"] >= diferenca_range[0]) & 
            (df_filtrado["diferenca_absoluta"] <= diferenca_range[1])
        ]
        
        st.write(f"Pedidos filtrados: {len(df_filtrado)} ({len(df_filtrado)/len(df_anomalias)*100:.1f}%)")

        st.divider()

        # Gráfico 1: Disparidade por Pedido (Barras)
        st.subheader("📊 Diferença entre Valor Registrado e Calculado")
        fig1 = px.bar(
            df_filtrado.sort_values(by="diferenca_absoluta", ascending=False),
            x="id_pedido",
            y="diferenca_absoluta",
            color="severidade",
            text="diferenca_percentual",
            labels={
                "diferenca_absoluta": "Diferença Absoluta (R$)", 
                "id_pedido": "ID do Pedido",
                "diferenca_percentual": "Diferença %"
            },
            title="Disparidade por Pedido (Ordenado por Valor Absoluto)",
            height=500,
            color_discrete_map={
                'Valor correto': 'green',
                'Pequena Disparidade': 'lightblue',
                'Disparidade moderada': 'orange',
                'Grande Disparidade': 'red'
            }
        )
        fig1.update_layout(xaxis_tickangle=-45)
        st.plotly_chart(fig1, use_container_width=True)

        st.divider()

        # Gráfico 2: Comparativo Registrado vs Calculado (Scatter)
        st.subheader("📈 Comparativo: Registrado vs Calculado")
        fig2 = px.scatter(
            df_filtrado,
            x="valor_total_registrado",
            y="valor_calculado",
            hover_name="nome_cliente",
            color="severidade",
            size="diferenca_absoluta",
            labels={
                "valor_total_registrado": "Valor Registrado (R$)",
                "valor_calculado": "Valor Calculado (R$)",
                "nome_cliente": "Cliente"
            },
            title="Comparação entre Valor Registrado e Calculado",
            color_discrete_map={
                'Valor correto': 'green',
                'Pequena Disparidade': 'lightblue',
                'Disparidade moderada': 'orange',
                'Grande Disparidade': 'red'
            }
        )
        fig2.add_shape(
            type='line',
            x0=0,
            y0=0,
            x1=df_filtrado[["valor_total_registrado", "valor_calculado"]].max().max(),
            y1=df_filtrado[["valor_total_registrado", "valor_calculado"]].max().max(),
            line=dict(color='green', dash='dash'),
        )
        st.plotly_chart(fig2, use_container_width=True)

        st.divider()

        # Gráfico 3: Distribuição por Severidade
        st.subheader("📦 Distribuição por Severidade")
        fig3 = px.pie(
            df_filtrado,
            names="severidade",
            values="diferenca_absoluta",
            title="Proporção da Disparidade por Nível de Severidade",
            hole=0.4,
            color="severidade",
            color_discrete_map={
                'Valor correto': 'green',
                'Pequena Disparidade': 'lightblue',
                'Disparidade moderada': 'orange',
                'Grande Disparidade': 'red'
            }
        )
        st.plotly_chart(fig3, use_container_width=True)

        st.divider()

        # Gráfico 4: Histograma das Diferenças
        st.subheader("📊 Histograma das Diferenças")
        fig4 = px.histogram(
            df_filtrado,
            x="diferenca_absoluta",
            nbins=20,
            color="severidade",
            labels={"diferenca_absoluta": "Diferença Absoluta (R$)"},
            title="Distribuição das Diferenças por Severidade",
            color_discrete_map={
                'Valor correto': 'green',
                'Pequena Disparidade': 'lightblue',
                'Disparidade moderada': 'orange',
                'Grande Disparidade': 'red'
            }
        )
        st.plotly_chart(fig4, use_container_width=True)

        st.divider()

        # Gráfico 5: Top 10 Maiores Diferenças
        st.subheader("🏆 Top 10 Maiores Diferenças")
        top10 = df_filtrado.nlargest(10, 'diferenca_absoluta', keep='all')
        fig5 = go.Figure()
        fig5.add_trace(go.Bar(
            x=top10['id_pedido'],
            y=top10['valor_total_registrado'],
            name='Valor Registrado',
            marker_color='indianred'
        ))
        fig5.add_trace(go.Bar(
            x=top10['id_pedido'],
            y=top10['valor_calculado'],
            name='Valor Calculado',
            marker_color='lightseagreen'
        ))
        fig5.update_layout(
            barmode='group',
            title='Top 10 Pedidos com Maiores Diferenças (Registrado vs Calculado)',
            xaxis_title="ID do Pedido",
            yaxis_title="Valor (R$)"
        )
        st.plotly_chart(fig5, use_container_width=True)

        st.divider()

        # Checkbox para mostrar tabela completa
        if st.checkbox("Mostrar dados brutos"):
            st.subheader("📋 Dados Completos")
            st.dataframe(df_filtrado.style.format({
                'valor_total_registrado': 'R$ {:.2f}',
                'valor_calculado': 'R$ {:.2f}',
                'diferenca_absoluta': 'R$ {:.2f}',
                'diferenca_percentual': '{}'
            }))
            
            # Opção para download como CSV
            csv = df_filtrado.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Baixar dados como CSV",
                data=csv,
                file_name='anomalias_vendas.csv',
                mime='text/csv',
            )
    else:
        st.success("✅ Nenhuma anomalia encontrada nos valores dos pedidos. Tudo certo!")
        st.balloons()

if __name__ == "__main__":
    render()