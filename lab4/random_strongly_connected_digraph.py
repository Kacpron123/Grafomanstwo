"""Generate a random strongly connected digraph."""

import igraph as ig

from lab1.random_graph.random_graph import generate_random_graph
from lab1.representation import export_igraph, GraphFormat
from lab1.random_graph.enums import ErdosRenyiModel
from lab4.kosaraju import kosaraju


def generate_random_strongly_connected_digraph(num_nodes: int, prob: float) -> ig.Graph:
    """
    Generate a random directed graph and extract its largest strongly connected component.

    Args:
        num_nodes (int): The number of nodes in the original digraph.
        prob (float): Probability of creating an edge between two vertices.

    Returns:
        tuple[ig.Graph, ig.Graph]: The original graph and its largest strongly connected component.
    """
    graph = export_igraph(
        generate_random_graph(
            model=ErdosRenyiModel.G_N_P,
            num_nodes=num_nodes,
            edge_probability=prob,
            directed=True
        ),
        GraphFormat.ADJACENCY_MATRIX,
        directed=True
    )

    kosaraju_result = kosaraju(graph)

    main_component_class = max(
        set(kosaraju_result),
        key=kosaraju_result.count
    )

    new_vertex_ids = []
    for vertex in range(graph.vcount()):
        if kosaraju_result[vertex] == main_component_class:
            new_vertex_ids.append(vertex)

    # Create a new graph with only the vertices from the main strongly connected component
    new_graph = graph.subgraph(new_vertex_ids)

    return new_graph
