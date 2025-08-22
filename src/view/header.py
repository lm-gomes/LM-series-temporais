import streamlit as st

class Header:
  def __init__(
    self, model:str, dataset:str, start_date:str, end_date:str,
    periods:int, prompt_type:str, ts_format:str, ts_type:str
  ):
    """
    Classe responsável por criar o cabeçalho da aplicação.
    Esta classe é utilizada para definir os parâmetros de entrada do usuário, como o dataset, model, datas de início e fim,
    número de períodos e tipo de prompt.

    Args:
			model (str): model a ser utilizado. Ex: 'deepseek-r1-distill-qwen-32b'.
			dataset (str): Base de dados a ser utilizada. Ex: 'ETTH1', 'ETTH2'.
			start_date (str): Data de início da previsão. Ex: '2016-07-01'.
			end_date (str): Data de fim da previsão. Ex: '2016-07-02'.
			periods  (int): Número de períodos a serem previstos. Ex: 1.
      prompt_type (PromptType): Tipo do prompt (ZERO_SHOT, FEW_SHOT, etc.)
      ts_format (TSFormat): Formato dos dados temporais (ARRAY, CSV, etc.).
      ts_type (TSType): Tipo de série (NUMERIC, TEXTUAL).
    """
    self.model = model
    self.dataset = dataset
    self.start_date = start_date
    self.end_date = end_date
    self.periods  = periods
    self.prompt_type = prompt_type
    self.ts_format = ts_format
    self.ts_type = ts_type

  def header(self):
    st.write("### Análise dos dados")

    col1, col2, col3, col4 = st.columns(4)
    with col1:
      st.metric(label="Base de Dados", value=self.dataset)
    with col2:
      st.metric(label="Data de Início", value=self.start_date)
    with col3:
      st.metric(label="Data de Fim", value=self.end_date)
    with col4:
      st.metric(label="Períodos", value=self.periods)

    col4, col5, col6, col7 = st.columns(4)
    with col4:
      st.metric(label="Modelo", value=self.model)
    with col5:
      st.metric(label="Prompt", value=self.prompt_type)
    with col6:
      st.metric(label="Formato", value=self.ts_format)
    with col7:
      st.metric(label="Série Temporal", value=self.ts_type)
