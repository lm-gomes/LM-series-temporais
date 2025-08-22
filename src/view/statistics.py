import streamlit as st
from pathlib import Path
import pandas as pd
import plotly.graph_objects as go

class Statistics:
  def __init__(self, dataset:str):
    self.dataset = dataset
    diretorio_do_script = Path(__file__).resolve().parent
    self.caminho =  diretorio_do_script.parent.parent / 'data' / self.dataset
    self.df = pd.read_csv(self.caminho)

  def describe(self):
    describe = self.df['value'].describe()

    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
      st.metric(label="Base de Dados", value=self.dataset)
    with col2:
      st.metric("Total de Dados", len(self.df))
    with col3:
      st.metric("Mínimo", f"{describe['min']:.2f}")
    with col4:
      st.metric("Máximo", f"{describe['max']:.2f}")
    with col5:
      st.metric("Média", f"{describe['mean']:.2f}")

    col6, col7, col8, col9 = st.columns(4)
    with col6:
      st.metric("1º Quartil (Q1)", f"{describe['25%']:.2f}")
    with col7:
      st.metric("Mediana", f"{describe['50%']:.2f}")
    with col8:
      st.metric("3º Quartil (Q3)", f"{describe['75%']:.2f}")
    with col9:
      st.metric("Desvio Padrão", f"{describe['std']:.2f}")

  def dataframe(self):
    st.dataframe(self.df, use_container_width=True)

  def show(self):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=self.df["date"], y=self.df["value"], mode="lines", name="Série Temporal"))
    fig.update_layout(
      title="Valores ao Longo do Tempo",
      xaxis_title="Tempo",
      yaxis_title="Valores",
      colorway=["#1f77b4"],
      showlegend=True
    )
    st.plotly_chart(fig, use_container_width=True)
