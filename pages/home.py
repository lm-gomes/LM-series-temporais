import streamlit as st
from datetime import date
from streamlit_option_menu import option_menu
import os
import ast
import re

#componentes
from src.view.header import Header
from src.view.dataset import Dataset
from src.view.prompt import Prompt
from src.view.resultados import Resultados

from api.api import API


with st.sidebar:
	st.write(" ### 🔍 Parâmetros da Busca")

	lista_datasets = os.listdir('data')

	dataset = st.selectbox('Base de Dados', lista_datasets)
	modelo = st.selectbox('Modelo', [
		'deepseek-r1-distill-qwen-32b',
		'deepseek-r1-distill-qwen-14b',
		'deepseek-r1-distill-llama-8b',
		'deepseek-r1-distill-qwen-7b',
		'unsloth/deepseek-r1-distill-qwen-1.5b'
	], index=0, help='Escolha o modelo a ser utilizado. O modelo deepseek-r1-distill-qwen-32b é o mais avançado e pode fornecer melhores resultados, mas também é mais pesado e pode levar mais tempo para gerar respostas.')
	temperatura = st.slider(label='Temperatura', min_value=0.0, max_value=1.0, value=0.7, step=0.1, help='A temperatura controla a aleatoriedade da resposta do modelo. Valores mais altos resultam em respostas mais criativas e variados.')
	st.write('---')
	st.write(f"#### ⚙️ Configurações do Prompt - {dataset}")
		
	data_min = date(2016, 7, 1)
	data_max = date(2018, 6, 26)
	data_inicio = st.date_input(label='Data de início', max_value=data_max, min_value=data_min, value=date(2016, 7, 1))
	data_fim = st.date_input(label='Data de término', max_value=data_max, min_value=data_min, value=date(2016, 7, 2))
		
	periodos = st.slider(label='Períodos', min_value=24, max_value=96, value=24, step=1, help='Número de períodos a serem previstos. Cada período representa 1 hora de previsão.')
	tipo_prompt = st.radio(label='Prompt', options=['ZERO_SHOT', 'FEW_SHOT', 'COT', 'COT_FEW'], index=0, help='Escolha o tipo de prompt a ser utilizado')

	confirma = st.button(label='Gerar Análise', key='gerar_analise', help='Clique para gerar a análise de dados',type='primary', use_container_width=True)

if confirma:
	Header(dataset=dataset, data_fim=str(data_fim), data_inicio=str(data_inicio), modelo=modelo, periodos=periodos, tipo_prompt=tipo_prompt).header()
	Dataset(dataset=dataset, data_inicio=str(data_inicio), data_fim=str(data_fim), qtd_periodos=periodos).exibir_dados()
	prompt, lista_exato = Prompt(dataset=dataset, data_inicio=str(data_inicio), data_fim=str(data_fim), qtd_periodos=periodos, tipo_prompt=tipo_prompt).prompt()
	resposta, qtd_tokens_prompt, qtd_tokens_predito, tempo = API(model=modelo, prompt=prompt, temperature=temperatura).resposta()
	Resultados(val_exatos=lista_exato, val_previstos=resposta, qtd_tokens_prompt=qtd_tokens_prompt, qtd_tokens_resposta=qtd_tokens_predito, tempo=tempo).exibir_resultados()
	


else:
	st.write('## Confirme a escolha dos parâmetros para gerar a análise.')
	st.image("icons/undraw_search_re_x5gq.svg", width=500)