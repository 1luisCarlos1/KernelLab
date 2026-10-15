def fcfs(processes):
    """Executa primeiro o processo que chegou primeiro."""
    pending = sorted(
        processes,
        key=lambda p: (p["arrival"], p["id"])
    )
    timeline = []
    time = 0

    for process in pending:
        if time < process["arrival"]:
            time = process["arrival"]

        start = time
        time += process["burst"]

        timeline.append((process["id"], start, time))

    return timeline


def _non_preemptive(processes, selection_key):
    """Executa um processo até terminar antes de escolher outro."""
    pending = [p.copy() for p in processes]
    timeline = []
    time = 0

    while pending:
        available = [
            p for p in pending
            if p["arrival"] <= time
        ]

        if not available:
            time = min(p["arrival"] for p in pending)
            available = [
                p for p in pending
                if p["arrival"] <= time
            ]

        process = min(available, key=selection_key)

        start = time
        time += process["burst"]

        timeline.append((process["id"], start, time))
        pending.remove(process)

    return timeline


def sjf(processes):
    """Escolhe o menor tempo de CPU entre os processos disponíveis."""
    return _non_preemptive(
        processes,
        lambda p: (p["burst"], p["arrival"], p["id"])
    )


def priority_scheduling(processes):
    """Escolhe o processo de maior prioridade (menor número)."""
    return _non_preemptive(
        processes,
        lambda p: (p["priority"], p["arrival"], p["id"])
    )


def round_robin(processes, quantum=3):
    """Distribui a CPU em fatias de tempo configuráveis."""
    if quantum <= 0:
        raise ValueError("O quantum deve ser maior que zero.")

    ordered = sorted(
        [p.copy() for p in processes],
        key=lambda p: (p["arrival"], p["id"])
    )

    remaining = {p["id"]: p["burst"] for p in ordered}
    timeline = []
    ready_queue = []
    time = 0
    next_process = 0

    while next_process < len(ordered) or ready_queue:
        # Adiciona à fila os processos que já chegaram.
        while (
            next_process < len(ordered)
            and ordered[next_process]["arrival"] <= time
        ):
            ready_queue.append(ordered[next_process]["id"])
            next_process += 1

        # Se a fila estiver vazia, avança até a próxima chegada.
        if not ready_queue:
            time = ordered[next_process]["arrival"]
            continue

        process_id = ready_queue.pop(0)
        duration = min(quantum, remaining[process_id])

        start = time
        time += duration
        remaining[process_id] -= duration

        timeline.append((process_id, start, time))

        # Processos que chegaram durante esta fatia entram primeiro.
        while (
            next_process < len(ordered)
            and ordered[next_process]["arrival"] <= time
        ):
            ready_queue.append(ordered[next_process]["id"])
            next_process += 1

        # Se ainda não terminou, o processo volta ao fim da fila.
        if remaining[process_id] > 0:
            ready_queue.append(process_id)

    return timeline


def calculate_metrics(processes, timeline):
    """Calcula espera, retorno, resposta e trocas de contexto."""
    metrics = {}

    for process in processes:
        process_id = process["id"]

        own_segments = [
            segment for segment in timeline
            if segment[0] == process_id
        ]

        first_start = min(segment[1] for segment in own_segments)
        completion = max(segment[2] for segment in own_segments)

        turnaround = completion - process["arrival"]
        waiting = turnaround - process["burst"]
        response = first_start - process["arrival"]

        metrics[process_id] = {
            "waiting": waiting,
            "turnaround": turnaround,
            "response": response,
            "completion": completion
        }

    if timeline:
        context_switches = sum(
            1
            for previous, current in zip(timeline, timeline[1:])
            if previous[0] != current[0]
        )
    else:
        context_switches = 0

    return metrics, context_switches


def print_results(processes, timeline, algorithm_name):
    """Exibe o diagrama de Gantt e as métricas do algoritmo."""
    metrics, switches = calculate_metrics(processes, timeline)

    print(f"\n{'=' * 55}")
    print(algorithm_name)
    print("=" * 55)

    print("\nDiagrama de Gantt:")
    print(" | ".join(
        f"{process_id} [{start}-{end}]"
        for process_id, start, end in timeline
    ))

    print("\nProcesso | Espera | Retorno | Resposta")

    for process in processes:
        process_id = process["id"]
        values = metrics[process_id]

        print(
            f"{process_id:8} | "
            f"{values['waiting']:6} | "
            f"{values['turnaround']:7} | "
            f"{values['response']:8}"
        )

    count = len(processes)

    print(f"\nTempo médio de espera: "
          f"{sum(m['waiting'] for m in metrics.values()) / count:.2f}")

    print(f"Tempo médio de retorno: "
          f"{sum(m['turnaround'] for m in metrics.values()) / count:.2f}")

    print(f"Tempo médio de resposta: "
          f"{sum(m['response'] for m in metrics.values()) / count:.2f}")

    print(f"Trocas de contexto: {switches}")

    return metrics, switches