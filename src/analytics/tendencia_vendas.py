import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from src.utils.query_runner import run_query
import pandas as pd

def render():
    st.header("📈 Análise de Tendência de Vendas Mensal")
    
    st.divider()

    try:
        df = run_query("5-Query_CTE_Tendencias_Vendas.sql")

        # Verificação básica
        if df.empty or df['status_dados'].iloc[0] == 'Sem pedidos no período':
            st.warning("Nenhum dado encontrado para análise.")
            return
            
        # Garante que as colunas existem
        required_columns = {
            'mes_ano', 'total_vendas', 'crescimento_percentual', 
            'quantidade_pedidos', 'ticket_medio', 'clientes_ativos',
            'forma_pagamento_mais_comum'
        }
        if not required_columns.issubset(df.columns):
            missing = required_columns - set(df.columns)
            st.error(f"Colunas faltando: {missing}")
            return
            
        # Conversão segura e tratamento de dados
        numeric_cols = ['total_vendas', 'crescimento_percentual', 'quantidade_pedidos', 
                       'ticket_medio', 'clientes_ativos']
        for col in numeric_cols:
            df[col] = pd.to_numeric(df[col], errors='coerce')
        
        df = df.dropna(subset=['total_vendas'])
        
        # Cálculo da média móvel de 3 meses
        df['media_movel_3meses'] = df['total_vendas'].rolling(3).mean()
        
        # Seção de métricas
        st.subheader("📌 KPIs Principais")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Último Mês", df['mes_ano'].iloc[-1])
        with col2:
            st.metric("Vendas Último Mês", f"R$ {df['total_vendas'].iloc[-1]:,.2f}",
                     help=f"Ticket médio: R$ {df['ticket_medio'].iloc[-1]:,.2f}")
        with col3:
            crescimento = df['crescimento_percentual'].iloc[-1]
            st.metric("Crescimento", f"{crescimento:.2f}%" if pd.notna(crescimento) else "N/D",
                     delta_color="inverse" if pd.notna(crescimento) and crescimento < 0 else "normal")
        with col4:
            st.metric("Clientes Ativos", f"{int(df['clientes_ativos'].iloc[-1])}",
                     help=f"Forma de pagamento mais usada: {df['forma_pagamento_mais_comum'].iloc[-1]}")

        # Segunda linha de KPIs
        col5, col6, col7, col8 = st.columns(4)
        with col5:
            media_movel = df['media_movel_3meses'].iloc[-1]
            st.metric("Média Móvel (3 meses)", f"R$ {media_movel:,.2f}" if pd.notna(media_movel) else "N/D")
        with col6:
            st.metric("Pedidos Último Mês", f"{int(df['quantidade_pedidos'].iloc[-1])}")
        with col7:
            st.metric("Vendas Totais", f"R$ {df['total_vendas'].sum():,.2f}")
        with col8:
            st.metric("Ticket Médio Geral", f"R$ {df['ticket_medio'].mean():,.2f}")

        st.divider()

        # Gráfico 1: Evolução de Vendas (Linha) com múltiplas métricas
        st.subheader("📈 Tendência de Vendas")
        fig1 = go.Figure()
        
        # Linha principal de vendas
        fig1.add_trace(go.Scatter(
            x=df['mes_ano'],
            y=df['total_vendas'],
            name='Vendas Totais',
            mode='lines+markers',
            line=dict(width=3, color='#4E79A7'),
            hovertext=df.apply(lambda x: f"""
                Mês: {x['mes_ano']}<br>
                Vendas: R$ {x['total_vendas']:,.2f}<br>
                Crescimento: {x['crescimento_percentual']:.2f}%<br>
                Pedidos: {int(x['quantidade_pedidos'])}<br>
                Clientes ativos: {int(x['clientes_ativos'])}<br>
                Forma de pagamento: {x['forma_pagamento_mais_comum']}
            """, axis=1),
            hoverinfo='text'
        ))
        
        # Linha de média móvel
        fig1.add_trace(go.Scatter(
            x=df['mes_ano'],
            y=df['media_movel_3meses'],
            name='Média Móvel (3 meses)',
            line=dict(width=2, color='#F28E2B', dash='dot'),
            hoverinfo='skip'
        ))
        
        fig1.update_layout(
            title="Evolução Mensal de Vendas com Média Móvel",
            xaxis_title="Mês/Ano",
            yaxis_title="Vendas (R$)",
            hovermode="x unified",
            xaxis=dict(tickangle=45)
        )
        st.plotly_chart(fig1, use_container_width=True)
        
        st.divider()

        # Gráfico 2: Crescimento Percentual (Barras) com referência
        st.subheader("📉 Variação Percentual Mensal")
        fig2 = go.Figure()
        
        fig2.add_trace(go.Bar(
            x=df['mes_ano'],
            y=df['crescimento_percentual'],
            marker=dict(
                color=df['crescimento_percentual'],
                colorscale='RdYlGn',
                cmin=-50,
                cmax=50
            ),
            text=df['crescimento_percentual'].apply(lambda x: f"{x:.2f}%" if pd.notna(x) else "N/D"),
            textposition='outside',
            hovertext=df.apply(lambda x: f"""
                Mês: {x['mes_ano']}<br>
                Variação: {x['crescimento_percentual']:.2f}%<br>
                Vendas: R$ {x['total_vendas']:,.2f}<br>
                Pedidos: {int(x['quantidade_pedidos'])}<br>
                Clientes: {int(x['clientes_ativos'])}
            """, axis=1),
            hoverinfo='text'
        ))
        
        # Linha de referência zero
        fig2.add_shape(
            type="line",
            x0=df['mes_ano'].iloc[0],
            x1=df['mes_ano'].iloc[-1],
            y0=0,
            y1=0,
            line=dict(color="Black", width=2)
        )
        
        fig2.update_layout(
            title="Taxa de Crescimento Mensal",
            xaxis_title="Mês/Ano",
            yaxis_title="Variação (%)",
            xaxis=dict(tickangle=45),
            coloraxis_showscale=False
        )
        st.plotly_chart(fig2, use_container_width=True)

        st.divider()

        # Gráfico 3: Comparativo com múltiplas dimensões
        st.subheader("🔄 Comparativo de Desempenho Mensal")
        fig3 = px.scatter(
            df,
            x="mes_ano",
            y="total_vendas",
            size="quantidade_pedidos",
            color="crescimento_percentual",
            color_continuous_scale='RdYlGn',
            hover_name="mes_ano",
            hover_data={
                'clientes_ativos': True,
                'crescimento_percentual': ':.2f%',
                'total_vendas': 'R$ ,.2f',
                'quantidade_pedidos': True,
                'ticket_medio': 'R$ ,.2f',
                'forma_pagamento_mais_comum': True
            },
            labels={
                'total_vendas': 'Vendas (R$)',
                'mes_ano': 'Mês/Ano',
                'quantidade_pedidos': 'Nº Pedidos',
                'crescimento_percentual': 'Crescimento (%)',
                'clientes_ativos': 'Clientes Ativos',
                'ticket_medio': 'Ticket Médio'
            },
            title="Comparativo Multidimensional de Vendas"
        )
        fig3.update_xaxes(tickangle=45)
        fig3.update_traces(
            marker=dict(sizemode='diameter', sizeref=0.1),
            hovertemplate="<b>%{hovertext}</b><br><br>" +
                         "Vendas: %{y:$,.2f}<br>" +
                         "Crescimento: %{marker.color:.2f}%<br>" +
                         "Pedidos: %{marker.size:,}<br>" +
                         "Clientes: %{customdata[0]:,}<br>" +
                         "Ticket médio: %{customdata[4]:$,.2f}<br>" +
                         "Pagamento: %{customdata[5]}"
        )
        st.plotly_chart(fig3, use_container_width=True)

        st.divider()

        # Gráfico 4: Boxplot com distribuição de múltiplas métricas
        st.subheader("📦 Distribuição de Métricas Mensais")
        tab1, tab2, tab3, tab4 = st.tabs(["Vendas", "Pedidos", "Ticket Médio", "Clientes"])
        
        with tab1:
            fig4a = px.box(
                df,
                y="total_vendas",
                points="all",
                labels={'total_vendas': 'Vendas (R$)'},
                title="Distribuição de Vendas Mensais"
            )
            st.plotly_chart(fig4a, use_container_width=True)
            
        with tab2:
            fig4b = px.box(
                df,
                y="quantidade_pedidos",
                points="all",
                labels={'quantidade_pedidos': 'Quantidade de Pedidos'},
                title="Distribuição de Pedidos Mensais"
            )
            st.plotly_chart(fig4b, use_container_width=True)
            
        with tab3:
            fig4c = px.box(
                df,
                y="ticket_medio",
                points="all",
                labels={'ticket_medio': 'Ticket Médio (R$)'},
                title="Distribuição do Ticket Médio"
            )
            st.plotly_chart(fig4c, use_container_width=True)
            
        with tab4:
            fig4d = px.box(
                df,
                y="clientes_ativos",
                points="all",
                labels={'clientes_ativos': 'Clientes Ativos'},
                title="Distribuição de Clientes Ativos"
            )
            st.plotly_chart(fig4d, use_container_width=True)

        st.divider()

        # Gráfico 5: Formas de pagamento ao longo do tempo
        st.subheader("💳 Formas de Pagamento Mais Utilizadas")
        fig5 = px.bar(
            df,
            x='mes_ano',
            y='quantidade_pedidos',
            color='forma_pagamento_mais_comum',
            title='Forma de Pagamento Dominante por Mês',
            labels={
                'mes_ano': 'Mês/Ano',
                'quantidade_pedidos': 'Total Pedidos',
                'forma_pagamento_mais_comum': 'Forma de Pagamento'
            }
        )
        fig5.update_xaxes(tickangle=45)
        st.plotly_chart(fig5, use_container_width=True)

        st.divider()

        if st.checkbox("Mostrar dados brutos"):
            st.subheader("📋 Dados Completos")
            st.dataframe(df.style.format({
                'total_vendas': 'R$ {:.2f}',
                'crescimento_percentual': '{:.2f}%',
                'ticket_medio': 'R$ {:.2f}',
                'media_movel_3meses': 'R$ {:.2f}'
            }))
            
            # Opção para download dos dados
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="Baixar dados como CSV",
                data=csv,
                file_name='tendencias_vendas_mensais.csv',
                mime='text/csv',
                help="Clique para baixar os dados completos em formato CSV"
            )

    except Exception as e:
        st.error(f"Erro na análise: {str(e)}")
        st.stop()

if __name__ == "__main__":
    render()