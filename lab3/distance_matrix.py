"""Represents the distance matrix of a graph."""


import igraph as ig
from lab3.dijkstra import dijkstra
from lab3.random_connected_graph import generate_random_connected_graph


def distance_matrix(graph: ig.Graph) -> list[list[float]]:
    """
    Computes the distance matrix of a graph.

    Parameters:
        - graph: igraph.Graph object representing the graph

    Returns:
        - dist: A 2D list where dist[i][j] is the shortest distance from node i to node j
    """
    matrix = []
    for i in range(graph.vcount()):
        d, _ = dijkstra(graph, i)  # Get shortest distances from node i to all other nodes
        dist = []
        for j in range(graph.vcount()):
            dist.append(d[j])  # Append the distance from node i to node j
        matrix.append(dist)  # Append the row for node i to the distance matrix
    return matrix  # Return the complete distance matrix

def print_distance_matrix(matrix: list[list[float]]) -> None:
    """
    Prints the distance matrix in a formatted manner.

    Parameters:
        - matrix: A 2D list representing the distance matrix
    """
    max_v = max(max(row) for row in matrix)  # Find the maximum distance value in the matrix
    count_digits = len(str(int(max_v)))  # Determine the number of digits in the maximum value for formatting
    for row in matrix:
        print(" ".join(f"{dist:>{count_digits}}" for dist in row))  # Print each distance formatted to the width of the maximum value
        
if __name__ == "__main__":
    # Example usage
    graph = generate_random_connected_graph(num_nodes=5, min_num_edges=4)
    dist_matrix = distance_matrix(graph)
    print_distance_matrix(dist_matrix)