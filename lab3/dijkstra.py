"""
Dijkstra's algorithm for finding shortest paths in a graph.
Implementation source: https://upel.agh.edu.pl/pluginfile.php/39504/mod_resource/content/8/alg_3.pdf,
https://upel.agh.edu.pl/pluginfile.php/204642/mod_resource/content/4/Grafy_3.pdf
"""

import igraph as ig
from pathlib import Path
from datetime import datetime
from lab1.save import save_igraph_png
from lab3.random_connected_graph import generate_random_connected_graph

def init(graph: ig.Graph, s: int) -> tuple[list[float], list[int | None]]:
    """
    Initializes the data structures for Dijkstra's algorithm.
    
    Parameters:
        - graph: igraph.Graph object representing the graph
        - s: The index of the source node from which to calculate shortest paths
        
    Returns:
        - d: List of distances from the source to each node, initialized to infinity except for the source node which is set to 0
        - p: List of previous nodes in the shortest path tree, initialized to None
    """
    # graph.vcount() returns the number of vertices in the graph
    d = [float("inf")] * graph.vcount()  # Initialize distances to infinity
    d[s] = 0  # Distance to the source is 0
    p = [None] * graph.vcount()  # Initialize previous nodes to None
    return d, p

def relax(u: int, v: int, graph: ig.Graph, d: list[float], p: list[int | None]) -> None:
    """
    Relaxes the edge between nodes u and v.
    
    Parameters:
        - u: The index of the starting node of the edge
        - v: The index of the ending node of the edge
        - graph: igraph.Graph object representing the graph
        - d: List of current shortest distances from the source to each node
        - p: List of previous nodes in the shortest path tree
    Returns:
        None
    """
    # get_eid(u, v) returns the edge ID for the edge between u and v
    # graph.es retrieves a sequence of all edges
    if d[v] > d[u] + graph.es[graph.get_eid(u, v)]["weight"]:
        d[v] = d[u] + graph.es[graph.get_eid(u, v)]["weight"]
        p[v] = u
        
def dijkstra(graph: ig.Graph, s: int) -> tuple[list[float], list[int | None]]:
    """
    Implements Dijkstra's algorithm to find the shortest paths from a source node to all other nodes in the graph.
    
    Parameters:
        - graph: igraph.Graph object representing the graph
        - s: The index of the source node from which to calculate shortest paths
        it is zero-based index!!!
        
    Returns:
        - d: List of shortest distances from the source to each node
        - p: List of previous nodes in the shortest path tree
    """
    
    d, p = init(graph, s)
    S = set()  # Set of nodes for which the shortest path is known
    while len(S) < graph.vcount():
        # Select the node u not in S with the smallest distance d[u]
        u = min((v for v in range(graph.vcount()) if v not in S), key=lambda v: d[v])
        S.add(u)  # Add u to the set of known shortest paths
        for v in graph.neighbors(u, mode="out"):  # For each neighbor v of u
            relax(u, v, graph, d, p)  # Relax the edge (u, v)
    return d, p


def print_dijkstra(d: list[float], p: list[int | None]) -> None:
    """
    Prints Dijkstra's shortest paths using 1-based vertex numbering.

    Args:
        d (list[float]): List of shortest distances from the source to each node.
        p (list[int | None]): List of previous nodes in the shortest path tree.
    """
    s = next(i for i, distance in enumerate(d) if distance == 0)
    print(f"START: s = {s + 1}")

    for i in range(len(d)):
        print(f"d[{i + 1}] = {d[i]} ==> [", end="")

        shortest_path = []
        j = i

        while j is not None:
            shortest_path.append(j + 1)
            j = p[j]

        print(" - ".join(map(str, reversed(shortest_path))), end="")
        print("]")



if __name__ == "__main__":
    # Example usage

    #zad1
    source_node = 1
    num_nodes = 10
    min_num_edges = 5
    graph = generate_random_connected_graph(num_nodes=num_nodes, min_num_edges=min_num_edges)
    now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    path = Path("lab3") / "results" / f"random_connected_graph_{now}.png"
    text = f"Random Connected Graph: nodes: {graph.vcount()}, edges: {graph.ecount()}"
    save_igraph_png(graph, path, text)

    #zad2
    distances, previous_nodes = dijkstra(graph, source_node)
    print_dijkstra(distances, previous_nodes)