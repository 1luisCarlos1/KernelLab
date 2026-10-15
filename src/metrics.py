import matplotlib.pyplot as plt
from pathlib import Path


def generate_cpu_chart(cpu_results):
    """Gera um gráfico comparando as médias dos escalonadores."""
    if not cpu_results:
        print("Nenhum resultado de CPU disponível para o gráfico.")
        return

    names = list(cpu_results.keys())
    waiting = [cpu_results[n]["avg_waiting"] for n in names]
    turnaround = [cpu_results[n]["avg_turnaround"] for n in names]
    response = [cpu_results[n]["avg_response"] for n in names]

    x = list(range(len(names)))
    width = 0.25

    fig, ax = plt.subplots(figsize=(10, 6))

    ax.bar(
        [i - width for i in x],
        waiting,
        width,
        label="Espera média"
    )
    ax.bar(
        x,
        turnaround,
        width,
        label="Retorno médio"
    )
    ax.bar(
        [i + width for i in x],
        response,
        width,
        label="Resposta média"
    )

    ax.set_title("Comparação dos escalonadores de CPU")
    ax.set_ylabel("Unidades de tempo")
    ax.set_xticks(x)
    ax.set_xticklabels(names, rotation=15)
    ax.legend()
    ax.grid(axis="y", alpha=0.3)

    fig.tight_layout()
    output_path = get_output_folder() / "comparacao_cpu.png"
    fig.savefig(output_path, dpi=150)
    plt.close(fig)

    print(f"Gráfico de CPU salvo em: {output_path}")


def generate_memory_chart(memory_results):
    """Compara page hits e page faults dos algoritmos de memória."""
    if not memory_results:
        print("Nenhum resultado de memória disponível para o gráfico.")
        return

    names = list(memory_results.keys())
    hits = [memory_results[n]["hits"] for n in names]
    faults = [memory_results[n]["faults"] for n in names]

    x = list(range(len(names)))
    width = 0.35

    fig, ax = plt.subplots(figsize=(8, 5))

    ax.bar(
        [i - width / 2 for i in x],
        hits,
        width,
        label="Page hits"
    )
    ax.bar(
        [i + width / 2 for i in x],
        faults,
        width,
        label="Page faults"
    )

    ax.set_title("Comparação dos algoritmos de memória")
    ax.set_ylabel("Quantidade")
    ax.set_xticks(x)
    ax.set_xticklabels(names)
    ax.legend()
    ax.grid(axis="y", alpha=0.3)

    fig.tight_layout()
    output_path = get_output_folder() / "comparacao_memoria.png"
    fig.savefig(output_path, dpi=150)
    plt.close(fig)

    print(f"Gráfico de memória salvo em: {output_path}")


def get_output_folder():
    """Cria a pasta de resultados na raiz do projeto."""
    project_folder = Path(__file__).resolve().parent.parent
    output_folder = project_folder / "resultados"
    output_folder.mkdir(parents=True, exist_ok=True)
    return output_folder
