
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

from schedulers import fcfs, round_robin
from memory import simulate_pages


class TestKernelLab(unittest.TestCase):

    def test_fcfs(self):
        processes = [
            {"id": "P1", "arrival": 0, "burst": 5, "priority": 2},
            {"id": "P2", "arrival": 1, "burst": 2, "priority": 1},
        ]

        result = fcfs(processes)

        self.assertEqual(result[0], ("P1", 0, 5))
        self.assertEqual(result[1], ("P2", 5, 7))

    def test_round_robin(self):
        processes = [
            {"id": "P1", "arrival": 0, "burst": 5, "priority": 1},
            {"id": "P2", "arrival": 1, "burst": 2, "priority": 2},
        ]

        result = round_robin(processes, quantum=2)

        self.assertEqual(result[0], ("P1", 0, 2))
        self.assertEqual(result[-1][2], 7)

    def test_memory_reference_count(self):
        sequence = [1, 2, 1, 3, 2]

        for algorithm in ("FIFO", "LRU", "Optimal"):
            result = simulate_pages(sequence, 2, algorithm)

            self.assertEqual(
                result["hits"] + result["faults"],
                len(sequence)
            )

    def test_optimal(self):
        sequence = [1, 2, 3, 1, 2, 4, 1, 2, 3, 4]

        fifo = simulate_pages(sequence, 3, "FIFO")
        optimal = simulate_pages(sequence, 3, "Optimal")

        self.assertLessEqual(
            optimal["faults"],
            fifo["faults"]
        )


if __name__ == "__main__":
    unittest.main()
