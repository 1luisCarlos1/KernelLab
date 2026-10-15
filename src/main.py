
import json
from pathlib import Path

from schedulers import (
    fcfs,
    sjf,
    round_robin,
    priority_scheduling,
    print_results,
)

from memory import (
    print_memory_results,
)

from devices import DeviceManager

from metrics import (
    generate_cpu_chart,
    generate_memory_chart,
)


def load_processes():
    """Carrega os processos do arquivo JSON."""
    project_folder = Path(__file__).resolve().parent.parent
    data_file = project_folder / "data" / "processes.json"

    with open(data_file, "r", encoding="utf-8") as file:
        return json.load(file)


def main():
    # ==========================================
    # 1. CARREGAMENTO DOS PROCESSOS
    # ==========================================
    processes = load_processes()

    print("=" * 60)
    print("KERNELLAB - SIMULADOR DE SISTEMAS OPERACIONAIS")
    print("=" * 60)

    # ==========================================
    # 2. ESCALONAMENTO DA CPU
    # ==========================================
    algorithms = [
        ("FCFS", lambda: fcfs(processes)),
        ("SJF", lambda: sjf(processes)),
        (
            "Round Robin (Quantum = 3)",
            lambda: round_robin(processes, quantum=3),
        ),
        (
            "Prioridade",
            lambda: priority_scheduling(processes),
        ),
    ]

    cpu_results = {}

    for name, execute in algorithms:
        timeline = execute()

        metrics, switches = print_results(
            processes,
            timeline,
            name,
        )

        count = len(metrics)

        if count > 0:
            cpu_results[name] = {
                "avg_waiting": sum(
                    item["waiting"]
                    for item in metrics.values()
                ) / count,

                "avg_turnaround": sum(
                    item["turnaround"]
                    for item in metrics.values()
                ) / count,

                "avg_response": sum(
                    item["response"]
                    for item in metrics.values()
                ) / count,

                "context_switches": switches,
            }

    print("\nSimulação de CPU concluída!")

    # ==========================================
    # 3. GERENCIAMENTO DE MEMÓRIA
    # ==========================================
    page_sequence = [
        1, 2, 3, 4, 1, 2, 5, 1, 2,
        3, 4, 5, 2, 1, 5, 3, 2,
    ]

    frame_count = 4
    memory_results = {}

    print("\n\nINICIANDO TESTES DE MEMÓRIA VIRTUAL")

    for algorithm in ("FIFO", "LRU", "Optimal"):
        result = print_memory_results(
            page_sequence,
            frame_count,
            algorithm,
        )

        memory_results[algorithm] = result

    print("\nCOMPARAÇÃO DA MEMÓRIA")

    for name, result in memory_results.items():
        print(
            f"{name}: "
            f"{result['faults']} faltas, "
            f"{result['hits']} hits, "
            f"taxa de faltas "
            f"{result['fault_rate']:.2%}"
        )

    best_algorithm = min(
        memory_results,
        key=lambda name: memory_results[name]["faults"],
    )

    print(
        f"\nMenor número de faltas: {best_algorithm}"
    )

    # ==========================================
    # 4. GERAÇÃO DOS GRÁFICOS
    # ==========================================
    print("\n\nGERANDO GRÁFICOS")

    generate_cpu_chart(cpu_results)
    generate_memory_chart(memory_results)

    # ==========================================
    # 5. CONTROLE DE DISPOSITIVOS
    # ==========================================
    print("\n\nINICIANDO CONTROLE DE DISPOSITIVOS")

    device_manager = DeviceManager()
    device_manager.show_matrix()

    print("\nTESTES DE ACESSO")

    # Solicitações autorizadas.
    device_manager.request_access(
        "P1", "rede", "read"
    )

    device_manager.request_access(
        "P3", "disco", "write"
    )

    device_manager.request_access(
        "P4", "audio", "use"
    )

    # Solicitação não autorizada.
    device_manager.request_access(
        "P1", "disco", "use"
    )

    print("\nPROCESSANDO FILA DO DISCO")
    device_manager.process_queue("disco")

    print("\nPROCESSANDO FILA DA REDE")
    device_manager.process_queue("rede")

    print("\nPROCESSANDO FILA DE AUDIO")
    device_manager.process_queue("audio")

    print("\nControle de dispositivos concluído!")

    # ==========================================
    # 6. FINALIZAÇÃO
    # ==========================================
    print("\n" + "=" * 60)
    print("SIMULAÇÃO DO KERNELLAB FINALIZADA!")
    print("=" * 60)


if __name__ == "__main__":
    main()

    