# KernelLab — Relatório Técnico

# 1. Introdução

O KernelLab é um simulador didático de sistemas operacionais desenvolvido para demonstrar conceitos relacionados ao gerenciamento de processos, escalonamento da CPU, gerenciamento de memória virtual e controle de dispositivos de entrada e saída.

O projeto utiliza cenários de processos com diferentes tempos de chegada, durações, prioridades, necessidades de memória e dispositivos associados. A partir desses dados, o simulador permite observar o comportamento de diferentes algoritmos e comparar seus resultados.

# 2. Objetivos

O objetivo geral é desenvolver um simulador capaz de representar aspectos fundamentais do funcionamento de um sistema operacional multitarefa.

Os objetivos específicos são:

- Implementar algoritmos de escalonamento de CPU.
- Calcular métricas de desempenho dos processos.
- Simular algoritmos de substituição de páginas.
- Representar o controle de acesso a dispositivos.
- Gerar gráficos para facilitar a análise dos resultados.
- Comparar os resultados e discutir vantagens e limitações das abordagens utilizadas.

# 3. Tecnologias utilizadas

O projeto foi desenvolvido em Python. A biblioteca Matplotlib é utilizada para gerar gráficos dos resultados das simulações. Os dados dos processos são armazenados em um arquivo JSON, e os testes automatizados utilizam o módulo `unittest`.

# 4. Organização do projeto

O projeto está organizado em módulos com responsabilidades específicas:

- `src/main.py`: ponto de entrada e execução das simulações.
- `src/schedulers.py`: algoritmos de escalonamento e cálculo de métricas da CPU.
- `src/memory.py`: simulação de memória virtual e substituição de páginas.
- `src/devices.py`: controle de acesso e filas de dispositivos.
- `src/metrics.py`: geração de gráficos.
- `data/processes.json`: dados dos processos utilizados na simulação.
- `tests/`: testes automatizados.
- `resultados/`: arquivos gráficos gerados pelo simulador.
- `docs/`: documentação técnica do projeto.

# 5. Metodologia

As simulações utilizam os processos definidos no arquivo JSON e uma sequência de referências a páginas para testar os algoritmos de memória. Os resultados são apresentados no terminal e em gráficos, permitindo comparar o comportamento das técnicas implementadas.

Os resultados quantitativos, a análise dos algoritmos e as limitações da implementação serão apresentados nas próximas seções após a consolidação das execuções e dos testes.

# 6. Resultados e discussão

# 6.1 Escalonamento da CPU

Foram executados quatro algoritmos de escalonamento: FCFS, SJF, Round Robin com quantum de 3 unidades de tempo e escalonamento por prioridade, considerando os seis processos definidos no cenário da MedControl Systems.

O FCFS apresentou tempo médio de espera de 13,67 e tempo médio de retorno de 20,50, com cinco trocas de contexto. O SJF apresentou resultados menores para essas métricas, com espera média de 10,67 e retorno médio de 17,50, também com cinco trocas de contexto.

O escalonamento por prioridade obteve os mesmos resultados do SJF nesta execução: espera média de 10,67, retorno médio de 17,50 e cinco trocas de contexto. Essa igualdade ocorreu devido à ordem de seleção dos processos disponíveis neste conjunto de dados, não sendo uma equivalência geral entre os algoritmos.

O Round Robin apresentou tempo médio de resposta de 5,33, inferior ao dos demais algoritmos. Por outro lado, sua espera média foi de 18,00 e seu retorno médio foi de 24,83, com 13 trocas de contexto registradas. Esses resultados evidenciam o compromisso entre oferecer oportunidades de execução aos processos e aumentar a frequência de alternância da CPU.

Considerando o cenário da MedControl, o tempo de resposta merece atenção especial devido à existência de um processo de emissão de alarme crítico. O algoritmo de prioridade pode ser adequado quando tarefas críticas precisam receber preferência, mas a implementação atual é não preemptiva. Portanto, um processo prioritário que chega enquanto outro está executando precisa aguardar o término deste último.

# 6.2 Gerenciamento de memória virtual

A simulação de memória foi realizada com quatro frames e uma sequência de 17 referências a páginas. O FIFO registrou 12 faltas e cinco acertos, correspondendo a uma taxa de faltas de 70,59%. O LRU registrou dez faltas e sete acertos, com taxa de 58,82%. O Optimal apresentou sete faltas e dez acertos, resultando em taxa de 41,18%.

Para a sequência utilizada, o Optimal apresentou o menor número de faltas. Esse resultado é esperado porque o algoritmo escolhe a página cuja próxima utilização está mais distante no futuro, utilizando o conhecimento prévio da sequência. Na prática, esse conhecimento não está disponível de forma perfeita, de modo que o Optimal serve como referência para avaliar outros métodos.

O LRU obteve resultado intermediário e superou o FIFO nesta sequência. O FIFO, por sua vez, substitui a página que está há mais tempo na memória, sem considerar diretamente a frequência ou a proximidade de uma nova utilização.

Os resultados mostram que a escolha do algoritmo de substituição influencia a quantidade de faltas de página. Entretanto, a conclusão está limitada à sequência e à quantidade de frames utilizadas nesta simulação.

# 6.3 Controle de acesso aos dispositivos

O módulo de dispositivos apresentou uma matriz de permissões por processo e recurso. Durante os testes, as solicitações de P1 para leitura da rede, P3 para escrita no disco e P4 para uso do áudio foram aceitas. Uma solicitação de P1 para utilizar o disco foi negada, pois esse processo não possui a permissão correspondente.

O programa também processou as filas dos dispositivos de forma sequencial e apresentou mensagens de conclusão das solicitações. Essa etapa demonstra o controle básico de permissões e o gerenciamento de filas.

Entretanto, a execução registrada não comprova, por si só, a disputa simultânea entre processos. A validação da concorrência e da sincronização com mutexes exige um teste adicional que provoque acessos concorrentes ao mesmo recurso e demonstre que o mecanismo de exclusão mútua impede acessos simultâneos incompatíveis.

# 6.4 Síntese dos resultados

Nas simulações realizadas, SJF e Prioridade apresentaram a menor espera média de CPU, enquanto Round Robin obteve a menor resposta média. Na memória, Optimal apresentou a menor taxa de faltas, seguido por LRU e FIFO.

Esses resultados não indicam que exista um único algoritmo superior em todas as situações. A escolha depende dos objetivos do sistema: reduzir a espera média, melhorar a resposta inicial, favorecer processos críticos ou diminuir faltas de página.

Para o cenário da MedControl, recomenda-se avaliar uma política de prioridade preemptiva para tarefas críticas, acompanhada de mecanismos contra starvation, além de testar a sincronização real dos dispositivos. As recomendações devem ser consideradas propostas de melhoria, e não funcionalidades já comprovadas pela implementação atual.

# 7. Conclusão

O KernelLab busca demonstrar, por meio de simulações, como decisões de escalonamento, gerenciamento de memória e controle de dispositivos influenciam o funcionamento de um sistema operacional. A análise final será elaborada com base nos resultados observados e nas limitações identificadas durante o desenvolvimento.

# 8. Referências

As referências deverão ser completadas com os materiais da disciplina e as fontes indicadas no enunciado do trabalho.