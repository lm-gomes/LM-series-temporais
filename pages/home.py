import streamlit as st
import pandas as pd
import os

# Componentes
from src.view.header import Header
from src.view.dataset import Dataset
from src.view.prompt import Prompt
from src.view.results import Results

# Banco de dados e API
from database.crud_models import CrudModels
from database.crud_history import CrudHistory
from api.api import API, Provider

# Tipos e Formatos
from src.model.prompt import PromptType
from src.model.format import TSFormat, TSType, parse_timeseries


with st.sidebar:
  st.write(f"#### ⚙️ Configurações do Modelo")

  provider = st.selectbox("API", options=list(Provider)).value
  models = CrudModels().select(provider=provider)
  models = [model[1] for model in models]

  model = st.selectbox('Modelo', models, index=0, help='Escolha o modelo a ser utilizado. O modelo deepseek-r1-distill-qwen-32b é o mais avançado e pode fornecer melhores resultados, mas também é mais pesado e pode levar mais response_time para gerar respostas.')
  temperature = st.slider(label='Temperatura', min_value=0.0, max_value=1.0, value=0.7, step=0.1, help='A temperatura controla a aleatoriedade da resposta do modelo. Valores mais altos resultam em respostas mais criativas e variados.')

  st.write('---')
  datasets = os.listdir('data')
  dataset = st.selectbox('Base de Dados', datasets)

  if dataset:
    st.write(f"#### ⚙️ Configurações do Prompt")
    df = pd.read_csv(f'data/{dataset}')
    min_date = pd.to_datetime(df['date']).min().date()
    max_date = pd.to_datetime(df['date']).max().date()

    default_start_date = min_date
    default_end_date = min(min_date + pd.Timedelta(days=1), max_date)

    start_date = st.date_input(label='Data de início', max_value=max_date, min_value=min_date, value=default_start_date)
    end_date = st.date_input(label='Data de término', max_value=max_date, min_value=min_date, value=default_end_date)

    periods = st.slider(label='Períodos', min_value=1, max_value=96, value=24, step=1, help='Número de períodos a serem previstos. Cada período representa 1 hora de previsão.')
    prompt_type = st.selectbox(label='Prompt', options=list(PromptType), index=0, format_func=lambda f: f.name, help='Escolha o tipo de prompt a ser utilizado.')

    ts_format = st.selectbox(label='Formato dos Dados', options=list(TSFormat), index=0, format_func=lambda f: f.name, help='Formato de apresentação dos dados para o modelo. Diferentes formatos podem influenciar a performance do modelo.')
    ts_type = st.radio(label='Série', options=list(TSType), index=0, format_func=lambda f: f.name, help='Na série numérica os valores são passados como [3.662, 3.124, 3.465, 3.609], enquanto na série textual os valores são passados como [3 . 6 6 2, 3 . 1 2 4, 3 . 4 6 5, 3 . 6 0 9].')

  confirm = st.button(label='Gerar Análise', help='Clique para gerar a análise de dados',type='primary', use_container_width=True)

if not confirm:
  st.write('## LLM4Time Pipeline')
  st.write('Siga as etapas de pré-processamento dos dados e configuração do modelo no pipeline abaixo para gerar previsões.\n\n')
  st.image("icons/llm4time.svg", width=750)

# ---------------- Validações ----------------

elif not model:
  st.toast("Modelo não selecionado. Selecione um antes de continuar.", icon="⚠️")

elif not dataset:
  st.toast("Base de dados não selecionada. Selecione uma antes de continuar.", icon="⚠️")

# ---------------- Resultado ----------------

else:
  Header(model=model, dataset=dataset, start_date=str(start_date), end_date=str(end_date), periods=periods, prompt_type=prompt_type.name, ts_format=ts_format.name, ts_type=ts_type.name).header()
  Dataset(dataset=dataset, start_date=str(start_date), end_date=str(end_date), periods=periods).show()
  prompt, y_true = Prompt(dataset=dataset, start_date=str(start_date), end_date=str(end_date), periods=periods, prompt_type=prompt_type, ts_format=ts_format, ts_type=ts_type).view()
  y_pred, total_tokens_prompt, total_tokens_response, response_time = API.mock(periods=periods, ts_format=ts_format, ts_type=ts_type)
  #y_pred, total_tokens_prompt, total_tokens_response, response_time = API(model=model, provider=provider, prompt=prompt, temperature=temperature).response()

  y_pred = parse_timeseries(y_pred, ts_format, ts_type) # Converte a resposta para uma lista
  smape, mae, rmse = Results(y_true=y_true, y_pred=y_pred, total_tokens_prompt=total_tokens_prompt, total_tokens_response=total_tokens_response, response_time=response_time).show()

  inserted = CrudHistory().insert(
    model=model,
    temperature=temperature,
    dataset=dataset,
    start_date=start_date,
    end_date=end_date,
    periods=periods,
    prompt=prompt,
    prompt_type=prompt_type,
    ts_format=ts_format,
    ts_type=ts_type,
    y_true=str(y_true),
    y_pred=str(y_pred),
    smape=smape,
    mae=mae,
    rmse=rmse,
    total_tokens_prompt=total_tokens_prompt,
    total_tokens_response=total_tokens_response,
    total_tokens=total_tokens_prompt+total_tokens_response,
    response_time=response_time
  )
  if inserted:
    st.toast("Análise gerada com sucesso!", icon="✅")
  else:
    st.error("Erro ao gerar a análise.", icon="🚨")
