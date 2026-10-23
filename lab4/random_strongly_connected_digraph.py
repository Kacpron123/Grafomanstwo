"""Generate a random strongly connected digraph."""

import igraph as ig

from lab1.random_graph.random_graph import generate_random_graph
from lab1.representation import export_igraph, GraphFormat
from lab1.random_graph.enums import ErdosRenyiModel
from lab4.kosaraju import kosaraju

def generate_random_strongly_connected_digraph(num_nodes: int, prob: float) -> ig.Graph:
    """
    Generate a random strongly connected directed graph (digraph) with the specified number of nodes.

    Args:
        num_nodes (int): The number of nodes in the digraph.

    Returns:
        ig.Graph: A random strongly connected directed graph represented as an igraph.Graph object.
    """
    graph = export_igraph(generate_random_graph(model=ErdosRenyiModel.G_N_P, num_nodes=num_nodes, edge_probability=prob, directed=True), GraphFormat.ADJACENCY_MATRIX, directed=True)
    kosaraju_result = kosaraju(graph)
    component_classes = set(kosaraju_result)
    component_classes_count = [kosaraju_result.count(component_class) for component_class in component_classes]
    for i, component_class in enumerate(component_classes):
        if component_classes_count[i] == max(component_classes_count):
            main_component_class = component_class
            break
    
    new_vertex_ids = []
    for vertex in range(graph.vcount()):
        if kosaraju_result[vertex] == main_component_class:
            new_vertex_ids.append(vertex)
            
    # Create a new graph with only the vertices from the main strongly connected component
    new_graph = graph.subgraph(new_vertex_ids)
    return new_graph