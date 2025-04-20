import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from src.utils.query_runner import run_query
from datetime import datetime, timedelta
import matplotlib

def render():
    st.header("📉 Análise de Clientes Inativos")
    
    st.divider()

    # Carrega os dados
    df_inativos = run_query("6-Query_CTE_Clientes_Inativos.sql")
    
    # Verificação básica
    if df_inativos.empty:
        st.warning("Nenhum dado encontrado para análise.")
        return
        
    # Conversão de tipos e tratamento
    df_inativos['data_ultimo_pedido'] = pd.to_datetime(df_inativos['data_ultimo_pedido'])
    
    # Calcula dias de inatividade para os que tem data
    df_inativos['dias_inatividade'] = (datetime.now() - df_inativos['data_ultimo_pedido']).dt.days
    
    # Seção de KPIs
    st.subheader("📌 KPIs Principais")
    
    # Calcula métricas
    total_clientes = len(df_inativos)
    nunca_compraram = len(df_inativos[df_inativos['status_cliente'] == 'Nunca comprou'])
    potencial_recuperacao = len(df_inativos[df_inativos['dias_inatividade'].between(180, 365)])
    
    # Layout de KPIs
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Clientes", total_clientes)
    with col2:
        st.metric("Nunca Compraram", nunca_compraram, f"{nunca_compraram/total_clientes*100:.1f}%")
    with col3:
        ultima_compra = df_inativos['data_ultimo_pedido'].max()
        st.metric("Última Compra", ultima_compra.strftime("%d/%m/%Y") if not pd.isnull(ultima_compra) else "N/A")

    # Segunda linha de KPIs
    col5, col6, col7, col8 = st.columns(4)
    with col5:
        media_inatividade = df_inativos[df_inativos['status_cliente'] != 'Nunca comprou']['dias_inatividade'].mean()
        st.metric("Inatividade Média", f"{media_inatividade:.0f} dias" if not pd.isna(media_inatividade) else "N/A")
    with col6:
        max_inatividade = df_inativos['dias_inatividade'].max()
        st.metric("Máx. Inatividade", f"{max_inatividade} dias" if not pd.isna(max_inatividade) else "N/A")
    with col7:
        min_inatividade = df_inativos[df_inativos['status_cliente'] != 'Nunca comprou']['dias_inatividade'].min()
        st.metric("Mín. Inatividade", f"{min_inatividade} dias" if not pd.isna(min_inatividade) else "N/A")
    with col8:
        st.metric("Potencial Recuperação", potencial_recuperacao, f"{potencial_recuperacao/total_clientes*100:.1f}%")

    st.divider()

    # Filtros
    st.subheader("🔍 Filtros Avançados")
    col_f1, col_f2, col_f3 = st.columns(3)
    
    with col_f1:
        status_opcoes = df_inativos["status_cliente"].unique().tolist()
        status_selecionado = st.multiselect(
            "Status do Cliente:", 
            status_opcoes, 
            default=status_opcoes
        )
    
    with col_f2:
        segmentos = df_inativos["segmento"].unique().tolist()
        segmento_selecionado = st.multiselect(
            "Segmento:",
            segmentos,
            default=segmentos
        )
    
    with col_f3:
        dias_range = st.slider(
            "Faixa de Inatividade (dias):", 
            min_value=0, 
            max_value=365*3,  # 3 anos
            value=(180, 365),  # 6 meses a 1 ano
            help="Filtra clientes pelo tempo de inatividade (exceto 'Nunca comprou')"
        )

        # Aplica filtros
    df_filtrado = df_inativos[
        (df_inativos["status_cliente"].isin(status_selecionado)) &
        (df_inativos["segmento"].isin(segmento_selecionado))
    ]
    
    # Filtra por dias de inatividade (exceto para "Nunca comprou")
    mask = (
        (df_filtrado['status_cliente'] == 'Nunca comprou') |
        (
            (df_filtrado['dias_inatividade'] >= dias_range[0]) & 
            (df_filtrado['dias_inatividade'] <= dias_range[1])
        )
    )
    df_filtrado = df_filtrado[mask]
    
    st.write(f"🔹 **Clientes filtrados:** {len(df_filtrado)} ({len(df_filtrado)/total_clientes*100:.1f}% do total)")
    st.write(f"🔹 **Valor potencial:** R$ {calcular_valor_potencial(df_filtrado):,.2f} (estimado)")

    st.divider()

    # Visualizações
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Distribuição", "📈 Temporal", "📍 Geográfica", "🗂 Detalhes"])
    
    with tab1:
        st.subheader("Distribuição de Clientes")
        
        col_t1_1, col_t1_2 = st.columns(2)
        
        with col_t1_1:
            fig_status = px.pie(
                df_filtrado,
                names='status_cliente',
                title='Proporção por Status',
                hole=0.4,
                color_discrete_sequence=px.colors.qualitative.Pastel
            )
            st.plotly_chart(fig_status, use_container_width=True)
            
        with col_t1_2:
            fig_segmento = px.bar(
                df_filtrado.groupby('segmento').size().reset_index(name='count'),
                x='segmento',
                y='count',
                title='Clientes por Segmento',
                color='segmento'
            )
            st.plotly_chart(fig_segmento, use_container_width=True)
        
        fig_box = px.box(
            df_filtrado[df_filtrado['status_cliente'] != 'Nunca comprou'],
            y='dias_inatividade',
            x='segmento',
            color='segmento',
            title='Distribuição de Dias de Inatividade por Segmento',
            points="all"
        )
        st.plotly_chart(fig_box, use_container_width=True)
    
    with tab2:
        st.subheader("Análise Temporal")
        
        if not df_filtrado['data_ultimo_pedido'].isnull().all():
            df_temporal = df_filtrado.copy()
            df_temporal['ano_mes'] = df_temporal['data_ultimo_pedido'].dt.to_period('M').astype(str)
            
            col_t2_1, col_t2_2 = st.columns(2)
            
            with col_t2_1:
                fig_evolucao = px.line(
                    df_temporal.groupby(['ano_mes', 'status_cliente']).size().reset_index(name='clientes'),
                    x='ano_mes',
                    y='clientes',
                    color='status_cliente',
                    title='Evolução de Clientes Inativos por Mês',
                    markers=True
                )
                fig_evolucao.update_xaxes(tickangle=45)
                st.plotly_chart(fig_evolucao, use_container_width=True)
            
            with col_t2_2:
                df_temporal['trimestre'] = df_temporal['data_ultimo_pedido'].dt.to_period('Q').astype(str)
                fig_trimestre = px.bar(
                    df_temporal.groupby(['trimestre', 'status_cliente']).size().reset_index(name='clientes'),
                    x='trimestre',
                    y='clientes',
                    color='status_cliente',
                    title='Distribuição por Trimestre',
                    barmode='group'
                )
                st.plotly_chart(fig_trimestre, use_container_width=True)
        else:
            st.warning("Sem dados temporais para análise")
            
    with tab3:
        st.subheader("Análise Geográfica")
        
        if 'uf' in df_filtrado.columns:
            df_geo = df_filtrado.groupby(['uf', 'status_cliente']).size().reset_index(name='count')
            
            fig_uf = px.bar(
                df_geo,
                x='uf',
                y='count',
                color='status_cliente',
                title='Distribuição por Estado',
                barmode='stack'
            )
            st.plotly_chart(fig_uf, use_container_width=True)
            
            # Solução alternativa para o mapa do Brasil
            try:
                # Criamos um dataframe com as siglas dos estados brasileiros
                estados_br = {
                    'AC': 'Acre', 'AL': 'Alagoas', 'AP': 'Amapá', 'AM': 'Amazonas',
                    'BA': 'Bahia', 'CE': 'Ceará', 'DF': 'Distrito Federal', 'ES': 'Espírito Santo',
                    'GO': 'Goiás', 'MA': 'Maranhão', 'MT': 'Mato Grosso', 'MS': 'Mato Grosso do Sul',
                    'MG': 'Minas Gerais', 'PA': 'Pará', 'PB': 'Paraíba', 'PR': 'Paraná',
                    'PE': 'Pernambuco', 'PI': 'Piauí', 'RJ': 'Rio de Janeiro', 'RN': 'Rio Grande do Norte',
                    'RS': 'Rio Grande do Sul', 'RO': 'Rondônia', 'RR': 'Roraima', 'SC': 'Santa Catarina',
                    'SP': 'São Paulo', 'SE': 'Sergipe', 'TO': 'Tocantins'
                }
                
                # Prepara os dados para o mapa
                df_mapa = df_filtrado.groupby('uf').size().reset_index(name='count')
                df_mapa['estado'] = df_mapa['uf'].map(estados_br)
                
                fig_map = px.choropleth(
                    df_mapa,
                    locations='uf',
                    locationmode='country names',
                    scope='south america',
                    color='count',
                    hover_name='estado',
                    hover_data=['count'],
                    color_continuous_scale='Blues',
                    title='Distribuição de Clientes por Estado',
                    labels={'count': 'Nº de Clientes'}
                )
                
                # Centraliza o mapa no Brasil
                fig_map.update_geos(
                    center=dict(lat=-14, lon=-55),
                    projection_scale=4,
                    visible=False
                )
                
                st.plotly_chart(fig_map, use_container_width=True)
                
            except Exception as e:
                st.warning(f"Não foi possível gerar o mapa: {str(e)}")
                st.info("Como alternativa, você pode usar a visualização de barras por estado acima.")
        else:
            st.warning("Dados geográficos não disponíveis")
            
    with tab4:
        st.subheader("Detalhes dos Clientes")
        
        col_d1, col_d2 = st.columns(2)
        
        with col_d1:
            st.markdown("**🔝 Top 10 - Maior Inatividade**")
            top_inativos = df_filtrado[df_filtrado['status_cliente'] != 'Nunca comprou']\
                .sort_values('dias_inatividade', ascending=False)
    
            if len(top_inativos) > 0:
                st.dataframe(
                    top_inativos.head(10)[['nome', 'segmento', 'dias_inatividade', 'data_ultimo_pedido']]
                    .style.format({'dias_inatividade': '{:.0f} dias'})
                    .background_gradient(subset=['dias_inatividade'], cmap='Reds')
                )
            else:
                st.info("Nenhum cliente inativo encontrado")
        
        with col_d2:
            st.markdown("**📌 Clientes que Nunca Compraram**")
            nunca_compraram_df = df_filtrado[df_filtrado['status_cliente'] == 'Nunca comprou']
    
            # Verifica se há clientes antes de tentar mostrar
            if len(nunca_compraram_df) > 0:
                # Mostra até 10 clientes ou todos se houver menos que 10
                st.dataframe(
                    nunca_compraram_df.head(10)[['nome', 'segmento', 'cidade', 'uf']]
                    .style.set_properties(**{'background-color': '#f0f2f6'})
                )
            else:
                st.info("Nenhum cliente encontrado que nunca comprou")
                    
                st.markdown("**📅 Linha do Tempo de Inatividade**")
                plot_timeline(df_filtrado)

    st.divider()

    # Dados completos e exportação
    if st.checkbox("📋 Mostrar dados completos"):
        st.subheader("Dados Completos")
        st.dataframe(
            df_filtrado[['id_cliente', 'nome', 'segmento', 'status_cliente', 'dias_inatividade', 'data_ultimo_pedido', 'cidade', 'uf']]
            .style.format({'dias_inatividade': '{:.0f} dias'})
            .background_gradient(subset=['dias_inatividade'], cmap='YlOrRd')
        )
        
        csv = df_filtrado.to_csv(index=False).encode('utf-8')
        st.download_button(
            "💾 Exportar para CSV",
            data=csv,
            file_name="clientes_inativos.csv",
            mime="text/csv",
            help="Exporta todos os dados filtrados para um arquivo CSV"
        )

def calcular_valor_potencial(df):
    """Calcula um valor potencial estimado para recuperação dos clientes"""
    # Valor médio estimado por cliente (pode ser ajustado)
    VALOR_MEDIO = 1500  
    return len(df) * VALOR_MEDIO

def plot_timeline(df):
    """Cria uma visualização de timeline para os clientes"""
    df_timeline = df.copy()
    df_timeline['dias_formatado'] = df_timeline['dias_inatividade'].apply(
        lambda x: f"{x} dias" if not pd.isna(x) else "Nunca comprou"
    )
    
    fig = go.Figure()
    
    for status in df_timeline['status_cliente'].unique():
        df_status = df_timeline[df_timeline['status_cliente'] == status]
        fig.add_trace(go.Scatter(
            x=df_status['dias_inatividade'],
            y=df_status['nome'],
            mode='markers',
            name=status,
            hovertext=df_status['dias_formatado'],
            marker=dict(size=10, line=dict(width=2))
            )
        )
    fig.update_layout(
        title='Linha do Tempo de Inatividade',
        xaxis_title='Dias de Inatividade',
        yaxis_title='Cliente',
        showlegend=True,
        height=600
    )
    
    st.plotly_chart(fig, use_container_width=True)

if __name__ == "__main__":
    render()