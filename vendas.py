import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

st.set_page_config(layout='wide')

dados = pd.read_csv('vendas.csv', delimiter=';', parse_dates=['Date'])
dados['Total'] = dados['Total'].str.replace(',', '.').astype(float)
dados['Rating'] = pd.to_numeric(dados['Rating'].str.replace(',', '.'))

dados['AnoMes'] = dados['Date'].dt.to_period('M')
opcoes_ano_mes = sorted(dados['AnoMes'].unique().astype(str))
opcao_selecionada = st.sidebar.selectbox('Escolha o mês e ano', opcoes_ano_mes)

dados_filtrados = dados[dados['AnoMes'].astype(str) == opcao_selecionada]

primeira_coluna, segunda_coluna = st.columns(2)

fig_faturamento_dia, ax_faturamento_dia = plt.subplots()
dados_filtrados.groupby(dados_filtrados['Date'].dt.date)['Total'].sum().plot(kind='bar', ax=ax_faturamento_dia)
ax_faturamento_dia.set_title('Faturamento Diário')
ax_faturamento_dia.set_xlabel('Data')
ax_faturamento_dia.set_ylabel('Total')
primeira_coluna.pyplot(fig_faturamento_dia)

dados_agrupados = dados_filtrados.groupby(['Product line', 'City'])['Total'].sum().unstack()

fig_faturamento_produto, ax_faturamento_produto = plt.subplots()
dados_agrupados.plot(kind='bar', stacked=True, ax=ax_faturamento_produto)
ax_faturamento_produto.set_title('Faturamento por Produto')
ax_faturamento_produto.set_xlabel('Linha de Produto')
ax_faturamento_produto.set_ylabel('Total')
segunda_coluna.pyplot(fig_faturamento_produto)

coluna_cidade, coluna_pagamento, coluna_avaliacao = st.columns(3)

faturamento_por_cidade = dados_filtrados.groupby('City')['Total'].sum()

fig_faturamento_cidade, ax_faturamento_cidade = plt.subplots()
faturamento_por_cidade.plot(kind='bar', ax=ax_faturamento_cidade)
ax_faturamento_cidade.set_title('Faturamento por Cidade')
ax_faturamento_cidade.set_xlabel('Cidade')
ax_faturamento_cidade.set_ylabel('Total')
coluna_cidade.pyplot(fig_faturamento_cidade)

pagamentos = dados_filtrados.groupby('Payment')['Total'].sum()
total_faturamento = pagamentos.sum()
percentuais_pagamentos = (pagamentos / total_faturamento) * 100

fig_pagamento, ax_pagamento = plt.subplots()
ax_pagamento.pie(percentuais_pagamentos, labels=pagamentos.index, autopct='%1.1f%%', startangle=90)
ax_pagamento.set_title('Faturamento por Tipo de Pagamento')
coluna_pagamento.pyplot(fig_pagamento)

avaliacao_media_por_cidade = dados_filtrados.groupby('City')['Rating'].mean()

fig_avaliacao, ax_avaliacao = plt.subplots()
avaliacao_media_por_cidade.plot(kind='bar', ax=ax_avaliacao)
ax_avaliacao.set_title('Avaliação Média por Cidade')
ax_avaliacao.set_xlabel('Cidade')
ax_avaliacao.set_ylabel('Avaliação Média')
coluna_avaliacao.pyplot(fig_avaliacao)
