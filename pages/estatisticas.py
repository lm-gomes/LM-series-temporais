import streamlit as st
import os

from src.view.statistics import Statistics

with st.sidebar:
  datasets = os.listdir('data')
  dataset = st.selectbox('Database', datasets)
  confirm = st.button(label='Gerar Estatísticas', key='generate_statistics', type='primary', use_container_width=True)

if confirm:
  statistics = Statistics(dataset=dataset)
  st.write("### Descrição")
  statistics.describe()
  st.write("### Base de Dados")
  statistics.dataframe()
  statistics.show()
