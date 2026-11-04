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
        (0,1), (0,2), (0,3), (0,4), (0,5), (0,6), (0,7),
        (1,2), (1,3), (1,4), (1,5), (1,6),
        (2,3), (2,4), (2,5), (2,6),
        (3,7)
    ])
    # graph = ig.Graph(n=11, edges=[
    #     (0,1), (0,4), (0,6), (0,9),
    #     (1,2), (1,5), (1,7),
    #     (2,3), (2,6), (2,8),
    #     (3,4), (3,7), (3,9),
    #     (4,5), (4,8),
    #     (5,10),
    #     (6,10),
    #     (7,10),
    #     (8,10),
    #     (9,10)
    # ])
    from lab1.visualization import generate_visualization
    generate_visualization(graph).save("graphSZCZEGOL.png")

    cycle = hamilton_cycle(graph)

    if cycle is None:
        print("Graf nie jest hamiltonowski")
    else:
        print("Graf jest hamiltonowski")
        print("[" + " - ".join(str(v + 1) for v in cycle) + "]")
        save_cycle_gif(graph, cycle, Path("lab2") / "results" / "hamilton.gif")
