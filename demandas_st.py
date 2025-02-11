import streamlit as st
import pandas as pd
import os
import numpy as np
import pydeck as pdk
import plotly.express as px

#BOTANDO A PAGINA WIDE
st.set_page_config(layout= 'wide')

path = os.getcwd() + '/df_demandas_tratado_teste.csv'

dados = pd.read_csv(path, sep= ';', decimal = ',')
dados = dados.rename(columns= {'LONG': 'longitude', 'LAT': 'latitude'})
dados['longitude'] = pd.to_numeric(dados['longitude'], errors='coerce', downcast='float')
dados['latitude'] = pd.to_numeric(dados['latitude'], errors='coerce',downcast='float')


dados = dados.dropna(subset=['longitude', 'latitude'])
dados['Data Recebimento'] = pd.to_datetime(dados['Data Recebimento'], dayfirst = True)
dados.sort_values("Data Recebimento")
dados.columns = dados.columns.str.strip()

#aplicar uma função na coluna de data para pegar os valores de unicos de meses
dados['mes'] = dados['Data Recebimento'].apply(lambda x: str(x.year) + '-' + str(x.month))

#criar a aba dos meses unicos
mes = st.sidebar.selectbox("Selecione o Mês", dados['mes'].unique())

#linkar a sidebar para ele puxar o df referente ao valor da select box
df_filter = dados[dados["mes"] == mes]



with st.container(border= True):
    st.write("""
    # DEMANDAS DO SETOR DE GEOPROCESSAMENTO
""",)

    #CRIANCO FILTRO PARA MENSAGEM INTERATIVA
df_execucao = dados[dados['SITUAÇÃO DE ANDAMENTO'] == 'Em execução.']

#MENSAGEM INTERATIVA
mensagem = " | ".join([f"""{row['Responsável']} - Requerimento {row['Nº do Requerimento']} - Trabalhando em: {row['Tipo de demanda']} !""" \
                    for _, row in df_execucao.iterrows()])

marquee_html = """
<div style="
    white-space: nowrap;
    overflow: hidden;
    box-sizing: border-box;">
    <marquee behavior="scroll" direction="left" scrollamount="5" style="color: red; font-size: 25px;">
        🚀🗺️ Demandas em execução: {} 🌍 SETOR QUE MAIS PRODUZ 📊 !!
    </marquee>
</div>
""".format(mensagem)
st.markdown(marquee_html, unsafe_allow_html=True)


#CRIANDO AS COLUNAS
col1, col2, col3 = st.columns([2,1,2], vertical_alignment= 'top', border=True)


#COLUNA 1
with col1:
    
    col1.write(df_filter)
    fig1 = px.bar(df_filter, y = 'Órgão - quem solicitou ao Geo', title= 'Setores Solicitantes', orientation= 'h', color = 'Cargo/Função')
    col1.plotly_chart(fig1)


#coluna 2
with col2:
    df_pie2 = df_filter['Responsável'].value_counts().reset_index()
    df_pie2.columns = ['membros', 'quantidade']
    fig2_ = px.pie(df_pie2, values= 'quantidade', names = 'membros', title= 'Demandas Realizados Por Membro')
    col2.plotly_chart(fig2_)
    df_pie = df_filter['SITUAÇÃO DE ANDAMENTO'].value_counts().reset_index()
    df_pie.columns = ['status','quantidade']
    fig2 = px.pie(df_pie, 
                names='status', 
                values='quantidade', 
                title=f'Situação das Demandas do Período: {mes}',
                color_discrete_sequence=px.colors.qualitative.Set3,
                hole=0.4)  # Define um "donut" no centro)

    col2.plotly_chart(fig2)




with col3:
   
    col3.write('Localização das Demandas')
    col3.map(df_filter, longitude= 'longitude', latitude= 'latitude', use_container_width= False, height= 400)

    
    fig3 = px.bar(df_filter, x ='Tipo de demanda', title= 'Tipos de demandas Entregues:')
    col3.plotly_chart(fig3)






