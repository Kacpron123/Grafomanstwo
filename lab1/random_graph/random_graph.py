"""Generates random graphs based on the Erdős-Rényi model."""

from pathlib import Path
import igraph as ig
from datetime import datetime

from lab1.random_graph.enums import ErdosRenyiModel
from lab1.representation import GraphFormat
from lab1.visualization import generate_visualization
from lab1.validation import validate_adjacency_matrix, validate_incidence_matrix, validate_adjacency_list



def generate_random_graph(
        model: ErdosRenyiModel,
        num_nodes: int,
        num_edges: int | None = None,
        edge_probability: float | None = None,
        return_graph_format: GraphFormat = GraphFormat.ADJACENCY_LIST
    ) -> list[list[int]]:
    """
    Generates a random graph represented as the specified format.

    Parameters:
        - model (ErdosRenyiModel): The model to use for generating the graph.
        - num_nodes (int): The number of nodes in the graph.
        - num_edges (int | None): The number of edges in the graph.
            Must be in range [0, n*(n-1)/2] for G(n, l) model.
        - edge_probability (float | None): The probability of an edge existing between any two nodes.
            Must be in range [0, 1] for G(n, p) model.
        - return_graph_format (GraphFormat): The format in which to return the graph.

    Returns:
        - list: A list of lists representing the random graph.
    """
    if num_nodes <= 0:
        raise ValueError("num_nodes must be a positive integer.")
    if model not in ErdosRenyiModel:
        raise ValueError(f"Invalid model. Choose from: {list(ErdosRenyiModel)}")
    if model == ErdosRenyiModel.G_N_L and num_edges is None:
        raise ValueError("num_edges must be provided for G(n, l) model.")
    if model == ErdosRenyiModel.G_N_L and not (0 <= num_edges <= num_nodes * (num_nodes - 1) // 2):
        raise ValueError(f"num_edges must be in range [0, {num_nodes * (num_nodes - 1) // 2}] for G(n, l) model.")
    if model == ErdosRenyiModel.G_N_P and edge_probability is None:
        raise ValueError("edge_probability must be provided for G(n, p) model.")
    if model == ErdosRenyiModel.G_N_P and not (0 <= edge_probability <= 1):
        raise ValueError("edge_probability must be between 0 and 1.")
    import random
    
    # random.random() chooses a random float in the range [0.0, 1.0) with uniform distribution.
    # by testing if the random number is smaller than edge_probability, random.ranom() has edge_probability chance to pass the test
    
    if model == ErdosRenyiModel.G_N_L:
        # Create a list of all possible edges
        possible_edges = [
            (i, j)
            for i in range(num_nodes)
            for j in range(i + 1, num_nodes)
        ]
        # Randomly select num_edges edges from the possible edges
        selected_edges = random.sample(possible_edges, num_edges)
        if return_graph_format == GraphFormat.ADJACENCY_MATRIX:
            # Fill the adjacency matrix based on the selected edges
            matrix = [
                [0 for _ in range(num_nodes)]
                for _ in range(num_nodes)
            ]
            for u, v in selected_edges:
                matrix[u][v] = 1
                matrix[v][u] = 1
            validate_adjacency_matrix(matrix)
            return matrix
        elif return_graph_format == GraphFormat.ADJACENCY_LIST:
            # Create an adjacency list based on the selected edges
            adjacency_list: list[list[int]] = [[] for _ in range(num_nodes)]
            for u, v in selected_edges:
                adjacency_list[u].append(v)
                adjacency_list[v].append(u)
            validate_adjacency_list(adjacency_list)
            return adjacency_list
        elif return_graph_format == GraphFormat.INCIDENCE_MATRIX:
            # Create an incidence matrix based on the selected edges
            incidence_matrix = [
                [0 for _ in range(num_edges)]
                for _ in range(num_nodes)
            ]
            for edge_index, (u, v) in enumerate(selected_edges):
                incidence_matrix[u][edge_index] = 1
                incidence_matrix[v][edge_index] = 1
            validate_incidence_matrix(incidence_matrix)
            return incidence_matrix
        
    elif model == ErdosRenyiModel.G_N_P:
        if return_graph_format == GraphFormat.ADJACENCY_MATRIX:
            # Fill the adjacency matrix based on the edge probability
            matrix = [
                [0 for _ in range(num_nodes)]
                for _ in range(num_nodes)
            ]
            for i in range(num_nodes):
                for j in range(i + 1, num_nodes):
                    if random.random() < edge_probability:
                        matrix[i][j] = 1
                        matrix[j][i] = 1
            validate_adjacency_matrix(matrix)
            return matrix
        elif return_graph_format == GraphFormat.ADJACENCY_LIST:
            # Fill the adjacency list based on the edge probability
            adjacency_list: list[list[int]] = [[] for _ in range(num_nodes)]
            for i in range(num_nodes):
                for j in range(num_nodes):
                    if i != j and random.random() < edge_probability:
                        adjacency_list[i].append(j)
            validate_adjacency_list(adjacency_list)
            return adjacency_list
        elif return_graph_format == GraphFormat.INCIDENCE_MATRIX:
            # Fill the incidence matrix based on the edge probability
            incidence_matrix = [[0 for _ in range(num_edges)] for _ in range(num_nodes)]
            edges = [
                (i, j) for i in range(num_nodes)
                for j in range(i + 1, num_nodes)
                if random.random() < edge_probability
            ]
            for edge_index, (u, v) in enumerate(edges):
                incidence_matrix[u][edge_index] = 1
                incidence_matrix[v][edge_index] = 1
            validate_incidence_matrix(incidence_matrix)
            return incidence_matrix
        
if __name__ == "__main__":
    # Example usage
    # adjacency_matrix = generate_random_graph(ErdosRenyiModel.G_N_L, num_nodes=10, num_edges=8, return_graph_format=GraphFormat.ADJACENCY_MATRIX)
    adjacency_matrix = generate_random_graph(ErdosRenyiModel.G_N_P, num_nodes=10, edge_probability=0.3, return_graph_format=GraphFormat.ADJACENCY_MATRIX)
    n= len(adjacency_matrix)
    edges = [(i, j) for i in range(n) for j in range(i + 1, n) if adjacency_matrix[i][j] == 1]
    graph = ig.Graph(n=n, edges=edges)
    now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    path = Path("lab1") / "random_graph" / "results" / f"random_graph_{now}.png"
    path.parent.mkdir(parents=True, exist_ok=True)
    generate_visualization(graph).save(path.absolute().as_posix())