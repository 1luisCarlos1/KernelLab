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

Esta seção será preenchida com os resultados reais obtidos na execução do KernelLab, incluindo tabelas comparativas, gráficos, análise das métricas e discussão das diferenças entre os algoritmos.

# 7. Conclusão

O KernelLab busca demonstrar, por meio de simulações, como decisões de escalonamento, gerenciamento de memória e controle de dispositivos influenciam o funcionamento de um sistema operacional. A análise final será elaborada com base nos resultados observados e nas limitações identificadas durante o desenvolvimento.

# 8. Referências

As referências deverão ser completadas com os materiais da disciplina e as fontes indicadas no enunciado do trabalho.