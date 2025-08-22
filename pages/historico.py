import streamlit as st
from database.crud_history import CrudHistory
from src.view.graph import Graph
import os

# ---------------- Dialog confirmação de exclusão ----------------

@st.dialog("Confirmar exclusão")
def confirmation_dialog(dataset: str, prompts: list):
  st.write(f"Tem certeza que deseja limpar o histórico do dataset **{dataset}** para os prompts abaixo?")
  st.markdown("\n".join(f"- **{prompt}**" for prompt in prompts))
  st.caption("**⚠️ Esta ação não poderá ser desfeita.**")

  col1, col2 = st.columns(2)
  with col1:
    if st.button("Cancelar", use_container_width=True):
      st.rerun()
  with col2:
    if st.button("Limpar", use_container_width=True, type="primary"):
      try:
        CrudHistory().remove_many(dataset=dataset, prompt_types=prompts)
        st.rerun()
      except Exception as e:
        st.toast(f"Erro ao limpar o histórico: {str(e)}", icon="⚠️")

# ---------------- Sidebar ----------------

with st.sidebar:
  st.write(" ### 🔍 Parâmetros da Busca")

  datasets = os.listdir('data')
  dataset = st.selectbox('Base de Dados', datasets)

  prompts = st.multiselect(label='Tipo de Prompt',
    options=['ZERO_SHOT', 'FEW_SHOT', 'COT', 'COT_FEW'],
    default=['ZERO_SHOT'],
    help='Selecione os tipos de prompts que deseja visualizar. Você pode selecionar mais de um tipo de prompt para comparar os resultados.'
  )
  confirm_view_history = st.button(
    label='Visualizar Previsões',
    help='Clique para visualizar o histórico de previsões dos prompts selecionados.',
    type='primary',
    use_container_width=True
  )
  confirm_clear_history = st.button(
    label='Limpar Histórico',
    help='Clique para limpar o histórico de previsões dos prompts selecionados.',
    use_container_width=True
  )

# ---------------- Validações ----------------

if confirm_view_history and prompts == []:
  st.warning("Por favor, selecione pelo menos um tipo de prompt para visualizar as previsões.")

elif confirm_clear_history and prompts == []:
  st.warning("Por favor, selecione pelo menos um tipo de prompt para limpar o histórico.")

# ---------------- Ações ----------------

elif confirm_clear_history:
  confirmation_dialog(dataset, prompts)

elif confirm_view_history:
  results = CrudHistory().select(dataset=dataset, prompt_types=prompts)
  for i, result in enumerate(results[::-1]):
    y_true = list(map(float, result[11].strip('[]').split(',')))
    y_pred = eval(result[12])

    st.write('### Gráfico Série Temporal - Prompt')
    Graph.forecast(
      title=f'{result[1]} / SMAPE = {result[13]}',
      y_true=y_true,
      y_pred=y_pred,
      key=i
    )

    st.markdown(
      """
      <style>
        .full-width-table {
          width: 100%;
          border-collapse: collapse;
        }
        .full-width-table th, .full-width-table td {
          padding: 8px;
          text-align: left;
          font-size: 18px;
        }
        .full-width-table th {
          text-align: center;
          background-color: #333;
          color: #fff;
        }
        .centered {
          text-align: center;
          background-color: #333;
          color: #fff;
          font-weight: bold;
        }
        .full-width-table tr:nth-child(even) {
          background-color: #444;
        }
        .full-width-table tr:nth-child(odd) {
          background-color: #666;
        }
        .full-width-table td {
          color: #fff;
          font-weight: bold;
        }
      </style>
      """,
      unsafe_allow_html=True
      )

    st.markdown(
      f"""
      <table class="full-width-table">
        <tbody>
          <tr>
            <th colspan="2" class="centered">Parâmetros do Modelo</th>
          </tr>
          <tr>
            <td>Modelo</td>
            <td>{str(result[1])}</td>
          </tr>
          <tr>
            <td>Temperatura</td>
            <td>{str(result[2])}</td>
          </tr>
          <tr>
            <th colspan="2" class="centered">Parâmetros do Prompt</th>
          </tr>
          <tr>
            <td>Base de dados</td>
            <td>{str(result[3])}</td>
          </tr>
          <tr>
            <td>Data de início</td>
            <td>{str(result[4])}</td>
          </tr>
          <tr>
            <td>Data de término</td>
            <td>{str(result[5])}</td>
          </tr>
          <tr>
            <td>Períodos</td>
            <td>{int(result[6])}</td>
          </tr>
          <tr>
            <td>Tipo do prompt</td>
            <td>{str(result[8])}</td>
          </tr>
          <tr>
            <td>Formato</td>
            <td>{str(result[9])}</td>
          </tr>
          <tr>
            <td>Tipo de série</td>
            <td>{str(result[10])}</td>
          </tr>
          <tr>
            <th colspan="2" class="centered">Resposta do Modelo</th>
          </tr>
          <tr>
            <td>Quantidade de tokens do prompt</td>
            <td>{str(result[16])}</td>
          </tr>
          <tr>
            <td>Quantidade de tokens da resposta</td>
            <td>{str(result[17])}</td>
          </tr>
          <tr>
            <td>Total de tokens</td>
            <td>{str(result[18])}</td>
          </tr>
          <tr>
            <td>Tempo de resposta (segundos)</td>
            <td>{str(result[19])}</td>
          </tr>
          <tr>
            <td>Valores exatos</td>
            <td>{result[11]}</td>
          </tr>
          <tr>
            <td>Valores previstos</td>
            <td>{result[12]}</td>
          </tr>
          <tr>
            <th colspan="2" class="centered">Métricas</th>
          </tr>
          <tr>
            <td>sMAPE</td>
            <td>{result[13]}</td>
          </tr>
          <tr>
            <td>MAE</td>
            <td>{result[14]}</td>
          </tr>
          <tr>
            <td>RMSE</td>
            <td>{result[15]}</td>
          </tr>
        </tbody>
      </table>
    """,
    unsafe_allow_html=True)
    st.write("### Prompt")
    st.code(result[7], language='python', line_numbers=True)
    st.write('---')
