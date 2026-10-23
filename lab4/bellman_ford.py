"""Implementation of the Bellman-Ford algorithm for finding the shortest paths in a weighted graph."""

import igraph as ig

def bellman_ford(G: ig.Graph, s: int) -> tuple[list[float], list[int | None]]:
    """
    Bellman-Ford algorithm to find the shortest paths from a source node to all other nodes in a weighted graph.
    
    Args:
        G (ig.Graph): The input graph represented as an igraph.Graph object.
        s (int): The index of the source node.
        
    Returns:
        tuple[list[float], list[int | None]]: A tuple containing two lists:
            - distances: A list of shortest distances from the source to each node.
            - predecessors: A list of predecessor nodes for each node in the shortest path tree.
    """
    # init
    d = [float("inf")] * G.vcount()  # Initialize distances to infinity
    d[s] = 0  # Distance to the source is 0
    p = [None] * G.vcount()  # Initialize previous nodes to None
    
    n = G.vcount()  
    for _ in range(n - 1):
        for edge in G.es:
            u, v = edge.tuple
            if d[v] > d[u] + edge["weight"]:
                d[v] = d[u] + edge["weight"]
                p[v] = u
    # Check for negative-weight cycles
    for edge in G.es:
        u, v = edge.tuple
        if d[v] > d[u] + edge["weight"]:
            raise ValueError("Graph contains a negative-weight cycle")
    return d, p



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
    distance_matrix = []
    for i in range(graph.vcount()):
        distances, predecessors = bellman_ford(graph, i)
        distance_matrix.append(distances)
    with open(Path("lab4") / "results" / f"shortest_distance_matrix_{now}.txt", "w") as f:
        print("Shortest distance matrix:", file=f)
        for row in distance_matrix:
            print(row, file=f)
        
    image.save(path.absolute().as_posix())
    