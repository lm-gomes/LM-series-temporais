import streamlit as st
import plotly.graph_objects as go

class Graph:
  @staticmethod
  def sample(title:str, values:list):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=list(range(len(values))), y=values, mode='lines', name='Série Temporal'))
    fig.update_layout(
      title=title,
      xaxis_title='Períodos',
      yaxis_title='Valores',
      colorway=['#1f77b4'],
      showlegend=True,
    )
    st.plotly_chart(fig, use_container_width=True)
    st.write('---')

  @staticmethod
  def forecast(title:str, y_true:list, y_pred:list, key:int=1):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=list(range(len(y_true))), y=y_true, mode='lines', name='Valores Reais'))
    fig.add_trace(go.Scatter(x=list(range(len(y_pred))), y=y_pred, mode='lines', name='Valores Previsto'))
    fig.update_layout(
      title=title,
      xaxis_title='Períodos',
      yaxis_title='Valores',
      colorway=['#1f77b4', '#ff7f0e'],
      showlegend=True,
      height=600
    )
    st.plotly_chart(fig, use_container_width=True, key=key)
