from collections import Counter

import igraph as ig
import pytest
from lab2.components import components
from lab2.euler import fleury, generate_eulerian_graph, is_bridge, is_eulerian


def edges_of_cycle(cycle: list[int]) -> Counter:
    return Counter(tuple(sorted(pair)) for pair in zip(cycle, cycle[1:]))


def check_euler_cycle(graph: ig.Graph, cycle: list[int]) -> None:
    assert cycle[0] == cycle[-1]
    assert len(cycle) == graph.ecount() + 1
    graph_edges = Counter(tuple(sorted(e)) for e in graph.get_edgelist())
    assert edges_of_cycle(cycle) == graph_edges


# kokardka: dwa trójkąty połączone wierzchołkiem 0
BOWTIE = ig.Graph(n=5, edges=[(0, 1), (1, 2), (2, 0), (0, 3), (3, 4), (4, 0)])


@pytest.mark.parametrize(
    "edges, u, v, expected",
    [
        ([(0, 1)], 0, 1, True),
        ([(0, 1), (1, 2)], 0, 1, True),
        ([(0, 1), (1, 2), (2, 0)], 0, 1, False),
        ([(0, 1), (1, 2), (2, 0), (2, 3)], 2, 3, True),
    ],
)
def test_is_bridge(edges, u, v, expected):
    graph = ig.Graph(n=4, edges=edges)
    assert is_bridge(graph, u, v) is expected


def test_is_bridge_does_not_modify_graph():
    graph = BOWTIE.copy()
    is_bridge(graph, 0, 1)
    assert graph.ecount() == BOWTIE.ecount()


def test_fleury_bowtie():
    check_euler_cycle(BOWTIE, fleury(BOWTIE))


def test_fleury_does_not_modify_graph():
    graph = BOWTIE.copy()
    fleury(graph)
    assert graph.ecount() == BOWTIE.ecount()


@pytest.mark.parametrize("n", [3, 4, 5, 8, 10, None])
def test_generated_graph_is_eulerian(n):
    graph, sequence = generate_eulerian_graph(n)
    if n is not None:
        assert graph.vcount() == n
    assert sorted(graph.degree()) == sorted(sequence)
    assert all(d % 2 == 0 for d in graph.degree())
    assert len(set(components(graph))) == 1


@pytest.mark.parametrize("n", [3, 5, 8, 10])
def test_fleury_on_random_graphs(n):
    for _ in range(20):
        graph, _ = generate_eulerian_graph(n)
        check_euler_cycle(graph, fleury(graph))


def test_too_small_n():
    with pytest.raises(ValueError):
        generate_eulerian_graph(2)


@pytest.mark.parametrize(
    "n, edges, expected",
    [
        (3, [(0, 1), (1, 2), (2, 0)], True),  # trójkąt
        (5, [(0, 1), (1, 2), (2, 0), (0, 3), (3, 4), (4, 0)], True),  # kokardka
        (3, [(0, 1), (1, 2)], False),  # ścieżka: stopnie 1, 2, 1
        (
            6,
            [(0, 1), (1, 2), (2, 0), (3, 4), (4, 5), (5, 3)],
            False,
        ),  # dwa rozłączne trójkąty
        (4, [(0, 1), (1, 2), (2, 0)], False),  # trójkąt + izolowany wierzchołek
    ],
)
def test_is_eulerian(n, edges, expected):
    graph = ig.Graph(n=n, edges=edges)
    assert is_eulerian(graph) is expected


@pytest.mark.parametrize(
    "n, edges",
    [
        (3, [(0, 1), (1, 2)]),  # nieparzyste stopnie
        (6, [(0, 1), (1, 2), (2, 0), (3, 4), (4, 5), (5, 3)]),  # niespójny
    ],
)
def test_fleury_rejects_non_eulerian(n, edges):
    graph = ig.Graph(n=n, edges=edges)
    with pytest.raises(ValueError):
        fleury(graph)
