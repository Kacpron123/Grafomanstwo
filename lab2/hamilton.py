from pathlib import Path

import igraph as ig
from lab1.visualization import save_cycle_gif

from lab2.components import components


def can_be_hamiltonian(graph: ig.Graph) -> bool:
    if graph.vcount() < 3:
        return False
    if min(graph.degree()) < 2:
        return False
    return len(set(components(graph))) == 1


def hamilton_dfs(graph: ig.Graph, u: int, start: int, stack: list[int], visited: set[int]) -> bool:
    if len(stack) == graph.vcount():
        return graph.are_adjacent(u, start)

    for v in graph.neighbors(u):
        if v not in visited:
            stack.append(v)
            visited.add(v)
            if hamilton_dfs(graph, v, start, stack, visited):
                return True
            stack.pop()
            visited.remove(v)

    return False


def hamilton_cycle(graph: ig.Graph, start: int = 0) -> list[int] | None:
    if not can_be_hamiltonian(graph):
        return None

    stack = [start]
    visited = {start}

    if hamilton_dfs(graph, start, start, stack, visited):
        return stack + [start]
    return None


if __name__ == "__main__":
    graph = ig.Graph(n=8, edges=[
        (0, 1), (1, 2), (2, 6), (6, 3), (3, 5), (5, 7), (7, 4), (4, 0),
        (0, 6), (1, 4), (2, 3),
    ])

    cycle = hamilton_cycle(graph)

    if cycle is None:
        print("Graf nie jest hamiltonowski")
    else:
        print("Graf jest hamiltonowski")
        print("[" + " - ".join(str(v + 1) for v in cycle) + "]")
        save_cycle_gif(graph, cycle, Path("lab2") / "results" / "hamilton.gif")
