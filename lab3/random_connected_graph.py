"""Generate a random connected graph."""

import random
from PIL import ImageDraw
import igraph as ig
from pathlib import Path
from datetime import datetime

from lab1.random_graph.random_graph import generate_random_graph
from lab2.components import components
from lab1.representation import export_igraph, GraphFormat
from lab1.visualization import generate_visualization

def generate_random_connected_graph(num_nodes: int, min_num_edges: int) -> ig.Graph:
    """
    Generate a random connected graph with the specified number of nodes.
    
    Implementation was chosen bearing in mind the need to use as much of the previously developed code as possible:
        - Generate a random graph with the specified number of nodes and minimum number of edges.
        - Check if the graph is connected using the components function.
        - If the graph is not connected, add edges until it becomes connected.

    Args:
        num_nodes (int): The number of nodes in the graph.
        min_num_edges (int): The minimum number of edges in the graph.

    Returns:
        ig.Graph: A random connected graph with edges weighted.
    """
    if num_nodes <= 0:
        raise ValueError("num_nodes must be a positive integer.")
    if min_num_edges < 0:
        raise ValueError("min_num_edges must be a non-negative integer.")
    if min_num_edges > num_nodes * (num_nodes - 1) // 2:
        raise ValueError(f"min_num_edges must be in range [0, {num_nodes * (num_nodes - 1) // 2}] for a simple graph.")

    graph = export_igraph(generate_random_graph(num_nodes=num_nodes, num_edges=min_num_edges), GraphFormat.ADJACENCY_MATRIX)
    
    while len(set(components(graph))) > 1:  # While the graph is not connected
        # Get the list of connected components
        comp = components(graph)
        unique_components = list(set(comp))
        
        # Randomly select two different components to connect
        comp1, comp2 = random.sample(unique_components, 2)
        
        # Get the nodes in each component
        nodes_comp1 = [i for i, c in enumerate(comp) if c == comp1]
        nodes_comp2 = [i for i, c in enumerate(comp) if c == comp2]
        
        # Randomly select one node from each component
        node1 = random.choice(nodes_comp1)
        node2 = random.choice(nodes_comp2)
        
        # Add an edge between the two selected nodes
        graph.add_edge(node1, node2)


    # Add random weights to the edges
    for edge in graph.es:
        edge["weight"] = random.randint(1, 10)  # Assign a random weight between 1 and 10
    
    return graph

if __name__ == "__main__":
    num_nodes = 10
    min_num_edges = 5
    graph = generate_random_connected_graph(num_nodes, min_num_edges)
    image = generate_visualization(graph)
    
    now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    path = Path("lab3") / "results" / f"random_connected_graph_{now}.png"
    path.parent.mkdir(parents=True, exist_ok=True)
    draw = ImageDraw.Draw(image)
    draw.text((10, 10), f"Random Connected Graph: nodes: {num_nodes}, min_edges: {min_num_edges}", fill="black")
    image.save(path)
    