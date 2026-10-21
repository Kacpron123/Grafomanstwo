"""Represents the center of a graph and minimax center."""


from lab3.distance_matrix import distance_matrix
from lab3.random_connected_graph import generate_random_connected_graph

import igraph as ig

def center(graph: ig.Graph) -> int:
    """
    Computes the center of a graph.

    Parameters:
        - graph: igraph.Graph object representing the graph

    Returns:
        - center_node: The node that is the center of the graph - sum of distances to all other nodes is minimized
    """
    dist_matrix = distance_matrix(graph)  # Get the distance matrix of the graph
    center_node, distances_sum  = min([(i, sum(row)) for i, row in enumerate(dist_matrix)], key=lambda x: x[1])  # Calculate the sum of distances for each node
    
    return center_node, distances_sum


def minimax_center(graph: ig.Graph) -> int:
    """
    Computes the minimax center of a graph.

    Parameters:
        - graph: igraph.Graph object representing the graph

    Returns:
        - minimax_center_node: The node that is the minimax center of the graph - maximum distance to any other node is minimized
    """
    dist_matrix = distance_matrix(graph)  # Get the distance matrix of the graph
    minimax_center_node, max_distance = min([(i, max(row)) for i, row in enumerate(dist_matrix)], key=lambda x: x[1])  # Calculate the maximum distance for each node
    
    return minimax_center_node, max_distance

if __name__ == "__main__":
    # Example usage
    graph = generate_random_connected_graph(num_nodes=5, min_num_edges=4)
    center_node, distances_sum = center(graph)
    print(f"Center node: {center_node}, Sum of distances: {distances_sum}")
    minimax_center_node, max_distance = minimax_center(graph)
    print(f"Minimax center node: {minimax_center_node}, Maximum distance: {max_distance}")