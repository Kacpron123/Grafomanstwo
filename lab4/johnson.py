"""Implementation of Johnson's algorithm for finding the shortest paths in a weighted graph."""

import igraph as ig
from lab4.bellman_ford import bellman_ford
from lab3.dijkstra import dijkstra

def johnson(G: ig.Graph) -> list[list[float]]:
    """
    Johnson's algorithm to find the shortest paths between all pairs of nodes in a weighted graph.
    
    Args:
        G (ig.Graph): The input graph represented as an igraph.Graph object.
        
    Returns:
        list[list[float]]: A 2D list representing the shortest path distances between all pairs of nodes.
    """
    # add_s
    G = G.copy()  # Create a copy of the graph to avoid modifying the original graph
    s = G.vcount()
    G.add_vertex()
    for v in range(G.vcount() - 1):
        G.add_edge(s, v, weight=0)
    
    h, _ = bellman_ford(G, s)
    
    for edge in G.es:
        u, v = edge.tuple
        if u != s and v != s:
            edge["weight"] += h[u] - h[v]
    
    G.delete_vertices(s)
    
    distance_matrix = [[0 for _ in range(G.vcount())] for _ in range(G.vcount())]
    for u in range(G.vcount()):
        d, _ = dijkstra(G, u)
        for v in range(G.vcount()):
            distance_matrix[u][v] = d[v] + h[v] - h[u]
    
    return distance_matrix

if __name__ == "__main__":
    from lab4.random_strongly_connected_digraph import generate_random_strongly_connected_digraph
    from lab1.random_graph.random_graph import add_weights_to_edges
    from lab1.visualization import generate_visualization
    from PIL import Image, ImageDraw
    from datetime import datetime
    from pathlib import Path
    
    graph = generate_random_strongly_connected_digraph(num_nodes=10, prob=0.5)
    add_weights_to_edges(graph, range_weights=(-5, 10))
    image = generate_visualization(graph)
    draw = ImageDraw.Draw(image)
    draw.text((10, 10), "Random Strongly Connected Digraph", fill="black")
    now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    path = Path("lab4") / "results" / f"random_strongly_connected_digraph_{now}.png"
    path.parent.mkdir(parents=True, exist_ok=True)
    distance_matrix = johnson(graph)
    with open(Path("lab4") / "results" / f"shortest_distance_matrix_{now}.txt", "w") as f:
        print("Shortest distance matrix (Johnson):", file=f)
        for row in distance_matrix:
            print(row, file=f)
        
    image.save(path.absolute().as_posix())