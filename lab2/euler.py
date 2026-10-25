import random
from pathlib import Path

import igraph as ig
from lab1.visualization import save_cycle_gif

from lab2.components import components
from lab2.graphic_sequence import (
    build_graph_from_graphic_sequence,
    validate_graphic_sequence,
)
from lab2.k_regular import randomize_graph_locally


def is_eulerian(graph: ig.Graph) -> bool:
    if any(deg % 2 for deg in graph.degree()):
        return False
    return len(set(components(graph))) == 1


def generate_eulerian_graph(n: int | None = None) -> tuple[ig.Graph, list[int]]:

    if n is None:
        n = random.randint(3, 10)

    if n < 3:
        raise ValueError("Cannot be graph. Number of vertices is less than 3")

    while True:
        sequence: list[int] = [random.choice(range(2, n, 2)) for _ in range(n)]

        if not validate_graphic_sequence(sequence):
            continue

        graph = build_graph_from_graphic_sequence(sequence)
        graph = randomize_graph_locally(graph, n_steps=100)

        if not is_eulerian(graph):
            continue

        return graph, sequence


def is_bridge(graph: ig.Graph, u: int, v: int) -> bool:
    g = graph.copy()
    g.delete_edges(g.get_eid(u, v))
    return v not in g.subcomponent(u)


def choose_next(graph: ig.Graph, u: int) -> int:
    neighbors = graph.neighbors(u)
    v = neighbors[0]
    for neighbor in neighbors:
        if not is_bridge(graph, u, neighbor):
            v = neighbor
            break
    return v


def fleury(graph: ig.Graph, start: int = 0) -> list[int]:
    if not is_eulerian(graph):
        raise ValueError("Graph is not eulerian")

    g = graph.copy()

    cycle = [start]
    u = start

    while g.ecount():
        v = choose_next(g, u)
        g.delete_edges(g.get_eid(u, v))
        cycle.append(v)
        u = v

    return cycle


if __name__ == "__main__":
    n = 8

    graph, sequence = generate_eulerian_graph(n)
    cycle = fleury(graph)

    print("Wylosowano stopnie:", *sequence)
    print("[" + " - ".join(str(v + 1) for v in cycle) + "]")

    save_cycle_gif(graph, cycle, Path("lab2") / "results" / "euler.gif")
