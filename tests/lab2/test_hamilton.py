import igraph as ig
import pytest
from lab2.hamilton import can_be_hamiltonian, hamilton_cycle


def check_hamilton_cycle(graph: ig.Graph, cycle: list[int]) -> None:
    n = graph.vcount()
    assert cycle[0] == cycle[-1]
    assert len(cycle) == n + 1
    assert sorted(cycle[:-1]) == list(range(n))
    for u, v in zip(cycle, cycle[1:]):
        assert graph.are_adjacent(u, v)


EXAMPLE = ig.Graph(n=8, edges=[
    (0, 1), (1, 2), (2, 6), (6, 3), (3, 5), (5, 7), (7, 4), (4, 0),
    (0, 6), (1, 4), (2, 3),
])

# kokardka: dwa trójkąty połączone wierzchołkiem 0
BOWTIE = ig.Graph(n=5, edges=[(0, 1), (1, 2), (2, 0), (0, 3), (3, 4), (4, 0)])

TWO_TRIANGLES = ig.Graph(n=6, edges=[(0, 1), (1, 2), (2, 0), (3, 4), (4, 5), (5, 3)])


@pytest.mark.parametrize(
    "graph",
    [
        ig.Graph(n=3, edges=[(0, 1), (1, 2), (2, 0)]),
        ig.Graph.Ring(6),
        ig.Graph.Full(5),
        EXAMPLE,
    ],
)
def test_hamiltonian(graph):
    cycle = hamilton_cycle(graph)
    assert cycle is not None
    check_hamilton_cycle(graph, cycle)


@pytest.mark.parametrize("start", range(8))
def test_any_start(start):
    cycle = hamilton_cycle(EXAMPLE, start)
    assert cycle[0] == start
    check_hamilton_cycle(EXAMPLE, cycle)


@pytest.mark.parametrize(
    "graph",
    [
        ig.Graph(n=2, edges=[(0, 1)]),
        ig.Graph(n=4, edges=[(0, 1), (1, 2), (2, 3)]),
        ig.Graph.Star(5),
        BOWTIE,
        TWO_TRIANGLES,
        ig.Graph.Famous("Petersen"),
    ],
)
def test_not_hamiltonian(graph):
    assert hamilton_cycle(graph) is None


@pytest.mark.parametrize(
    "graph, expected",
    [
        (ig.Graph(n=2, edges=[(0, 1)]), False),
        (ig.Graph(n=4, edges=[(0, 1), (1, 2), (2, 3)]), False),
        (TWO_TRIANGLES, False),
        (BOWTIE, True),                       # warunki konieczne spełnione, a cyklu i tak nie ma
        (ig.Graph.Famous("Petersen"), True),  # j.w.
        (ig.Graph.Ring(6), True),
    ],
)
def test_can_be_hamiltonian(graph, expected):
    assert can_be_hamiltonian(graph) is expected
