ZERO_SHOT = """Você é um assistente de previsão de séries temporais encarregado de analisar dados de uma série temporal específica.

A série temporal tem dados de {periodos} peiodo(s) consecutivos. Cada anotação da série temporal representa a incidência de um evento que ocorre a cada dia.

Início da Previsão:
Sua previsão deve começar a partir do próximo período (meia-noite do próximo dia), seguindo o padrão observado nos dados anteriores.
Para este exemplo, um início de previsão esperado pode ser {dados_prompt[:4]}.
Garanta que o primeiro valor da previsão corresponda ao início do período, respeitando os padrões observados.

Objetivo:
Seu objetivo é prever a incidência de um evento para os próximos {dias} períodos, considerando os dados históricos e o contexto geral da série temporal.

Regras da Saída:
Após analisar os dados fornecidos e compreender os padrões de tráfego, gere uma previsão para os próximos {dias} dias, com as seguintes regras:
A saída deve ser uma lista contendo apenas os valores previstos, sem explicação adicional ou texto introdutório.
Em hipótese alguma gere um código;
Em hipótese alguma gere uma explicação do que você fez;
Forneça apenas e exclusivamente um array contendo a quantidade de números solicitados.
A previsão deve começar com o valor correspondente ao início do próximo período, respeitando os padrões observados nos dados históricos.

Exemplo de Saída para N=168:
{dados_prompt[:168]}

Instruções Adicionais:
Padrões Semanais: Utilize os dados fornecidos para entender padrões sazonais, como picos de incidência em determinados períodos.
Eventos Especiais: A ocorrência de eventos é significativamente afetada por feriados e outros eventos importantes.
Dia da Semana: O dia da semana também influencia a ocorrência de eventos.
Duração de um evento: A série temporal fornecida representa a ocorrência de um evento a cada hora.

Organização dos Dados:
Os dados da série temporal são apresentados como uma sequencia de valores, onde cada valor representa um período consecutivo.

Série temporal a ser analisada:
{dados_prompt}

Gere um array com {dias} posições (N={dias}) prevendo os números da sequência:
"""