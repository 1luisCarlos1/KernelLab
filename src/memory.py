def simulate_pages(sequence, frame_count, algorithm):
    """Simula a substituição de páginas usando FIFO, LRU ou Optimal."""
    if frame_count <= 0:
        raise ValueError("A quantidade de frames deve ser maior que zero.")

    if algorithm not in ("FIFO", "LRU", "Optimal"):
        raise ValueError("Algoritmo de memória desconhecido.")

    frames = [None] * frame_count
    history = []
    hits = 0
    faults = 0
    fifo_pointer = 0
    last_used = {}

    for position, page in enumerate(sequence):
        if page in frames:
            hits += 1
            status = "HIT"
        else:
            faults += 1
            status = "FAULT"

            if None in frames:
                # Usa primeiro um frame vazio.
                victim_index = frames.index(None)

            elif algorithm == "FIFO":
                # Substitui seguindo a ordem de entrada.
                victim_index = fifo_pointer

            elif algorithm == "LRU":
                # Substitui a página usada há mais tempo.
                victim_index = min(
                    range(frame_count),
                    key=lambda i: last_used[frames[i]]
                )

            else:
                # Optimal: escolhe a página cujo próximo uso
                # está mais distante no futuro.
                future = sequence[position + 1:]
                next_uses = []

                for frame_page in frames:
                    if frame_page in future:
                        next_uses.append(future.index(frame_page))
                    else:
                        next_uses.append(float("inf"))

                victim_index = next_uses.index(max(next_uses))

            frames[victim_index] = page

            if algorithm == "FIFO":
                fifo_pointer = (victim_index + 1) % frame_count

        last_used[page] = position

        history.append({
            "reference": page,
            "frames": frames.copy(),
            "status": status
        })

    total = len(sequence)
    fault_rate = faults / total if total else 0

    return {
        "history": history,
        "hits": hits,
        "faults": faults,
        "fault_rate": fault_rate
    }


def print_memory_results(sequence, frame_count, algorithm):
    """Mostra o estado da memória após cada referência."""
    result = simulate_pages(sequence, frame_count, algorithm)

    print(f"\n{'=' * 60}")
    print(f"MEMÓRIA VIRTUAL - {algorithm}")
    print("=" * 60)

    print("Ref. | " + " | ".join(
        f"Frame {i + 1}" for i in range(frame_count)
    ) + " | Resultado")

    for step in result["history"]:
        frame_text = " | ".join(
            "-" if page is None else str(page)
            for page in step["frames"]
        )

        print(
            f"{step['reference']:4} | "
            f"{frame_text} | {step['status']}"
        )

    print(f"\nPage hits: {result['hits']}")
    print(f"Page faults: {result['faults']}")
    print(f"Taxa de faltas: {result['fault_rate']:.2%}")

    return result