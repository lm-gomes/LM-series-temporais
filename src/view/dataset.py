import streamlit as st

from src.model.data import Data

class Dataset:
  def __init__(self, dataset:str, start_date:str, end_date:str, periods:int):
    """
    Classe responsável por manipular o dataset.

    Args:
      dataset (str): Dataset a ser manipulado.
      start_date (str): Data de início do dataset.
      end_date (str): Data de fim do dataset.
      periods (int): Quantidade de períodos a serem previstos.
    """
    self.dataset = dataset
    self.start_date = start_date
    self.end_date = end_date
    self.periods = periods*24

  def show(self):
    df_selected, y_true = Data(dataset=self.dataset, start_date=self.start_date, end_date=self.end_date, periods=self.periods).period_selection()
    st.write("### Dados Selecionados")
    st.dataframe(df_selected, use_container_width=True)
    st.write("### Dados Exatos")
    st.dataframe(y_true, use_container_width=True)
