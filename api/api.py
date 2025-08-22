# Provedores
import lmstudio as lms
from openai import OpenAI, AzureOpenAI

# Utilitárias
import re
import os
import time
from enum import Enum
from dotenv import load_dotenv

# Mock
import random
import pandas as pd
from src.model.format import TSFormat, TSType, format_timeseries

load_dotenv()

class Provider(str, Enum):
  LM_STUDIO = 'lmstudio'
  OPENAI = 'openai'
  AZURE = 'azure'

  def __str__(self):
    return {
      Provider.LM_STUDIO: "LM Studio",
      Provider.OPENAI: "OpenAI / Ollama",
      Provider.AZURE: "OpenAI Azure",
    }[self]

class API:
  def __init__(self, model: str, provider: Provider, prompt: str, temperature: float):
    """
    Classe responsável por manipular a API do modelo.

    Args:
      model (str): Modelo a ser utilizado.
      provider (Provider): Provedor da API (lmstudio, openai, azure).
      prompt (str): Prompt a ser utilizado.
      temperature (float): Temperatura do modelo.
    """
    self.model = model
    self.provider = provider
    self.prompt = prompt
    self.temperature = temperature

  def response(self):
    """
    Gera a resposta do modelo com base no prompt e temperatura definidos.

    Returns:
        tuple: (response, total_tokens_prompt, total_tokens_response, elapsed_time)
    """
    if self.provider == Provider.LM_STUDIO:
      return self.response_lmstudio()
    elif self.provider == Provider.OPENAI:
      return self.response_openai()
    elif self.provider == Provider.AZURE:
      return self.response_azure_openai()
    else:
      print(f"[ERROR] Provedor desconhecido: {self.provider}")
      return None, None, None, None

  def response_lmstudio(self):
    try:
      model_instance = lms.llm(self.model)
      print(f"[INFO] Modelo: {model_instance}")

      start_time = time.time()
      response_obj = model_instance.respond(self.prompt, config={
        "temperature": self.temperature,
      })
      end_time = time.time()

      # Verifica se o objeto tem o atributo `.text`
      response = response_obj.text if hasattr(response_obj, 'text') else str(response_obj)

      if 'deepseek-r1' in self.model:
        result_match = re.search(r'</think>\s*(.*)', response, re.DOTALL)
        if result_match:
          response = result_match.group(1).strip()

      print(f"[INFO] Resposta: {response}")
      total_tokens_prompt = response_obj.stats.prompt_tokens_count if hasattr(response_obj, "stats") else 0
      total_tokens_response = response_obj.stats.predicted_tokens_count if hasattr(response_obj, "stats") else 0
      print(f"[INFO] Tokens Prompt: {total_tokens_prompt} - Tokens Resposta: {total_tokens_response} - Tempo: {end_time - start_time:.2f} segundos")
      return response, total_tokens_prompt, total_tokens_response, end_time - start_time

    except Exception as e:
      print(f"[ERROR] Erro ao gerar resposta: {e}")
      return None, None, None, None

  def response_openai(self) -> tuple[str, int, int, float]:
    print(f"[INFO] Modelo: {self.model}")
    key_name = f'openai_{self.model}_key'.replace("-", "_").replace(".", "_")
    base_url_name = f'openai_{self.model}_base_url'.replace("-", "_").replace(".", "_")

    api_key = os.getenv(key_name)
    base_url = os.getenv(base_url_name)
    print(f"[INFO] Base URL: {base_url}")

    client = OpenAI(
      api_key=api_key,
      base_url=base_url
    )

    try:
      start_time = time.time()
      response = client.chat.completions.create(
        model=self.model,
        messages=[{"role": "user", "content": self.prompt}],
        temperature=self.temperature,
      )
      end_time = time.time()

      response = response.choices[0].message.content

      if self.model == "deepseek-r1-distill-llama-70b":
        match = re.search(r'</think>\s*(.*)', response, re.DOTALL)
        if match:
          response = match.group(1).strip()
        else:
          response = response.strip()
      else:
        response = response.strip()

      if self.model == "deepseek-r1-distill-llama-70b":
        total_tokens_prompt = response.usage.total_tokens
        total_tokens_response = response.usage.prompt_tokens
      else:
        total_tokens_prompt = response.usage.prompt_tokens
        total_tokens_response = response.usage.completion_tokens

      print(f"[INFO] Resposta: {response}")
      print(f"[INFO] Tokens Prompt: {total_tokens_prompt} - Tokens Resposta: {total_tokens_response} - Tempo: {end_time - start_time:.2f} segundos")
      return response, total_tokens_prompt, total_tokens_response, end_time - start_time
    except Exception as e:
      print(f"[ERROR] Erro ao gerar resposta: {e}")
      return None, None, None, None

  def response_azure_openai(self) -> tuple[str, int, int, float]:
    print(f"[INFO] Modelo: {self.model}")
    key_name = f'azure_{self.model}_key'.replace("-", "_").replace(".", "_")
    version_name = f'azure_{self.model}_api_version'.replace("-", "_").replace(".", "_")
    endpoint_name = f'azure_{self.model}_endpoint'.replace("-", "_").replace(".", "_")

    api_key = os.getenv(key_name)
    api_version = os.getenv(version_name)
    endpoint = os.getenv(endpoint_name)
    print(f"[INFO] API Version: {api_version}")
    print(f"[INFO] Endpoint: {endpoint}")

    client = AzureOpenAI(
      api_key=api_key,
      azure_endpoint=endpoint,
      api_version=api_version
    )

    try:
      start_time = time.time()
      response = client.chat.completions.create(
        model=self.model,
        messages=[{"role": "user", "content": self.prompt}],
        temperature=self.temperature,
      )
      end_time = time.time()
      response_text = response.choices[0].message.content
      print(f"[INFO] Resposta: {response_text}")
      total_tokens_prompt = response.usage.prompt_tokens
      total_tokens_response = response.usage.completion_tokens
      print(f"[INFO] Tokens Prompt: {total_tokens_prompt} - Tokens Resposta: {total_tokens_response} - Tempo: {end_time - start_time:.2f} segundos")
      return response_text, total_tokens_prompt, total_tokens_response, end_time - start_time
    except Exception as e:
      print(f"[ERROR] Erro ao gerar resposta: {e}")
      return None, None, None, None

  @staticmethod
  def mock(periods: int, ts_format: TSFormat, ts_type: TSType) -> tuple[str, int, int, float]:
    response_time = round(random.uniform(0.5, 2.5), 2)
    total_tokens_prompt = random.randint(10, 500)
    total_tokens_response = random.randint(10, 500)

    # Gera uma resposta aleatória
    dates = pd.date_range(start='2018-01-01', periods=periods, freq='D')
    values = [round(random.uniform(0, 500), 4) for _ in range(periods)]
    response = [(d.strftime('%Y-%m-%d'), v) for d, v in zip(dates, values)]

    # Formata a resposta
    response = format_timeseries(response, ts_format, ts_type)

    time.sleep(response_time * 0.1) # Tempo de espera
    print(f"[MOCK] Resposta:\n{response}")
    print(f"[MOCK] Tokens Prompt: {total_tokens_prompt} - Tokens Resposta: {total_tokens_response} - Tempo: {response_time} segundos")
    return response, total_tokens_prompt, total_tokens_response, response_time
