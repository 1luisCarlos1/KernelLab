from collections import deque
from threading import Lock


# Matriz de permissões por processo e dispositivo.
# As permissões são exemplos para o simulador acadêmico.
ACCESS_MATRIX = {
    "P1": {
        "rede":  {"read": True,  "write": True,  "execute": False, "use": True,  "exclusive": False},
        "disco": {"read": False, "write": False, "execute": False, "use": False, "exclusive": False},
        "audio": {"read": False, "write": False, "execute": False, "use": False, "exclusive": False},
        "log":   {"read": True,  "write": True,  "execute": False, "use": True,  "exclusive": False},
    },
    "P2": {
        "rede":  {"read": True,  "write": True,  "execute": False, "use": True,  "exclusive": False},
        "disco": {"read": False, "write": False, "execute": False, "use": False, "exclusive": False},
        "audio": {"read": False, "write": False, "execute": False, "use": False, "exclusive": False},
        "log":   {"read": True,  "write": True,  "execute": False, "use": True,  "exclusive": False},
    },
    "P3": {
        "rede":  {"read": False, "write": False, "execute": False, "use": False, "exclusive": False},
        "disco": {"read": True,  "write": True,  "execute": False, "use": True,  "exclusive": False},
        "audio": {"read": False, "write": False, "execute": False, "use": False, "exclusive": False},
        "log":   {"read": True,  "write": True,  "execute": False, "use": True,  "exclusive": False},
    },
    "P4": {
        "rede":  {"read": True,  "write": True,  "execute": False, "use": True,  "exclusive": False},
        "disco": {"read": False, "write": False, "execute": False, "use": False, "exclusive": False},
        "audio": {"read": False, "write": True,  "execute": False, "use": True,  "exclusive": True},
        "log":   {"read": True,  "write": True,  "execute": False, "use": True,  "exclusive": False},
    },
    "P5": {
        "rede":  {"read": False, "write": False, "execute": False, "use": False, "exclusive": False},
        "disco": {"read": True,  "write": True,  "execute": False, "use": True,  "exclusive": True},
        "audio": {"read": False, "write": False, "execute": False, "use": False, "exclusive": False},
        "log":   {"read": True,  "write": True,  "execute": False, "use": True,  "exclusive": False},
    },
    "P6": {
        "rede":  {"read": True,  "write": True,  "execute": False, "use": True,  "exclusive": False},
        "disco": {"read": True,  "write": True,  "execute": False, "use": True,  "exclusive": False},
        "audio": {"read": False, "write": False, "execute": False, "use": False, "exclusive": False},
        "log":   {"read": True,  "write": True,  "execute": False, "use": True,  "exclusive": False},
    },
}


class DeviceManager:
    def __init__(self):
        self.queues = {
            "disco": deque(),
            "rede": deque(),
            "audio": deque(),
            "log": deque(),
        }

        # Um lock para proteger cada dispositivo compartilhado.
        self.locks = {
            device: Lock() for device in self.queues
        }

    def check_permission(self, process_id, device, action):
        """Verifica se o processo possui a permissão solicitada."""
        if process_id not in ACCESS_MATRIX:
            return False

        if device not in ACCESS_MATRIX[process_id]:
            return False

        if action not in ACCESS_MATRIX[process_id][device]:
            return False

        return ACCESS_MATRIX[process_id][device][action]

    def request_access(self, process_id, device, action="use"):
        """Valida a permissão e registra a solicitação na fila."""
        if device not in self.queues:
            print(f"Dispositivo desconhecido: {device}")
            return False

        if not self.check_permission(process_id, device, action):
            print(
                f"ACESSO NEGADO: {process_id} não tem permissão "
                f"para {action} em {device}."
            )
            return False

        self.queues[device].append({
            "process": process_id,
            "action": action
        })

        print(
            f"Solicitação aceita: {process_id} -> {device} "
            f"({action})."
        )
        return True

    def process_queue(self, device):
        """Processa as solicitações em ordem, protegendo o recurso."""
        if device not in self.queues:
            print(f"Dispositivo desconhecido: {device}")
            return

        queue = self.queues[device]

        while queue:
            request = queue.popleft()
            process_id = request["process"]
            action = request["action"]

            # O lock garante acesso exclusivo à seção protegida.
            with self.locks[device]:
                print(
                    f"Dispositivo {device}: "
                    f"{process_id} executando {action}."
                )
                print(f"Solicitação de {process_id} concluída.")

    def show_matrix(self):
        """Exibe as permissões resumidas de cada processo."""
        print("\nMATRIZ DE CONTROLE DE ACESSO")
        print("-" * 70)

        for process_id, devices in ACCESS_MATRIX.items():
            print(f"\n{process_id}:")

            for device, permissions in devices.items():
                allowed = [
                    action
                    for action, permitted in permissions.items()
                    if permitted
                ]

                print(
                    f"  {device}: "
                    f"{', '.join(allowed) if allowed else 'sem permissões'}"
                )
