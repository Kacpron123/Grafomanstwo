"""
Represents a minimal spanning tree of a graph.
Implementation of Prim's algorithm to find the minimal spanning tree of a graph:
https://upel.agh.edu.pl/pluginfile.php/39504/mod_resource/content/8/alg_3.pdf
"""

import igraph as ig
from pathlib import Path
from datetime import datetime
from PIL import Image, ImageDraw

from lab1.visualization import generate_visualization
from lab3.random_connected_graph import generate_random_connected_graph

def minimal_spanning_tree(graph: ig.Graph) -> ig.Graph:
    """
    Computes the minimal spanning tree of a graph using Prim's algorithm.

    Parameters:
        - graph: igraph.Graph object representing the graph

    Returns:
        - mst: igraph.Graph object representing the minimal spanning tree
    """
    T = [0] # Start with the first vertex in the tree
    graph = graph.copy()  # Create a copy of the graph to avoid modifying the original
    graph.es["color"] = ["gray"] * graph.ecount()
    graph.es["width"] = [2] * graph.ecount()
    while len(T) < graph.vcount(): # While the number of vertices in T is less than the number of vertices in the graph
        # Find the minimum weight edge connecting T to a vertex not in T
        min_edge = min(
            (e for e in graph.es if (e.source in T) != (e.target in T)),
            key=lambda e: e["weight"]
        )
        # Add the vertex connected by the minimum edge to T
        graph.es[min_edge.index]["color"] = "red"  # Highlight the edge in red for visualization
        graph.es[min_edge.index]["width"] = 5
        if min_edge.source in T:
            T.append(min_edge.target)  # Add the target vertex of the minimum edge to T
        else:
            T.append(min_edge.source)  # Add the source vertex of the minimum edge to T

    return graph


if __name__ == "__main__":
    # Example usage
    graph = generate_random_connected_graph(num_nodes=10, min_num_edges=20)  # Generate a random connected graph
    graph = minimal_spanning_tree(graph)  # Compute the minimal spanning tree
    print(graph.es["color"])
    print(graph.es["width"])
    now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    path = Path("lab3") / "results" / f"mst_{now}.png"
    path.parent.mkdir(parents=True, exist_ok=True)
    image: Image.Image = generate_visualization(graph)
    draw = ImageDraw.Draw(image)
    draw.text((10, 10), "Minimal Spanning Tree", fill="black")
    image.save(path.absolute().as_posix())
