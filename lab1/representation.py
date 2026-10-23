"""Functions for importing and exporting graphs in different representations"""

from enum import Enum

import igraph as ig
from lab1.common import print_matrix, print_adjacency_list, read_matrix, read_lines, parse_to_int
from lab1.validation import validate_adjacency_matrix, validate_incidence_matrix, validate_adjacency_list

###### Adjacency Matrix

def import_adjacency_matrix(path: str, directed: bool = False) -> ig.Graph:
    """Reads adjacency matrix from file and returns graph"""
    matrix = read_matrix(path)
    validate_adjacency_matrix(matrix, directed)

    n = len(matrix)

    if directed:
        # Reads only one side of matrix (it is symmetrical)
        edges = [(i, j) for i in range(n) for j in range(i + 1, n) if matrix[i][j] == 1]
    else:
        edges = [(i, j) for i in range(n) for j in range(n) if matrix[i][j] == 1]

    return ig.Graph(n=n, edges=edges, directed=directed)



def export_adjacency_matrix(graph: ig.Graph) -> list[list[int]]:
    """Converts graph into adjacency matrix"""
    n = graph.vcount()

    # Creates square matrix filled with zeroes
    matrix = [[0] * n for _ in range(n)]

    # Put 1 on both sides of the diagonal for each edge
    for u, v in graph.get_edgelist():
        matrix[u][v] = 1
        if not graph.is_directed():
            matrix[v][u] = 1

    return matrix


###### Incidence Matrix

def import_incidence_matrix(path: str, directed: bool = False) -> ig.Graph:
    """Reads incidence matrix from file and returns graph"""
    matrix = read_matrix(path)
    validate_incidence_matrix(matrix, directed)

    edges = []

    # Columns in matrix are edges with EXACTLY two vertices
    # for directed graphs -1 is the source and 1 is the target, for undirected graphs both are 1
    for column in zip(*matrix):
        if directed:
            targets = [vertex for vertex, value in enumerate(column) if value == 1]
            source = [vertex for vertex, value in enumerate(column) if value == -1]
            edges.append((source[0], targets[0]))
        else:
            ends = [vertex for vertex, value in enumerate(column) if value == 1]
            edges.append((ends[0], ends[1]))

    return ig.Graph(n=len(matrix), edges=edges, directed=directed)

def export_incidence_matrix(graph: ig.Graph) -> list[list[int]]:
    """Converts graph into incidence matrix"""
    n = graph.vcount()
    edges = graph.get_edgelist()
    k = len(edges)

    matrix = [[0] * k for _ in range(n)]

    for edge_idx, (u, v) in enumerate(edges):
        matrix[v][edge_idx] = 1
        if graph.is_directed():
            matrix[u][edge_idx] = -1
        else:
            matrix[v][edge_idx] = 1

    return matrix

###### Adjacency List
def import_adjacency_list(path: str, directed: bool = False) -> ig.Graph:
    """Reads adjacency list from file and returns graph"""
    lines = read_lines(path)
    adjacency = []

    for line in lines:
        if "." not in line:
            raise ValueError(f"Invalid format (missing dot '.'): '{line}'")
        
        neighbours_str = line.split(".", 1)[1]
        neighbours = parse_to_int(neighbours_str)
        adjacency.append(neighbours)

    validate_adjacency_list(adjacency, directed)
    n = len(adjacency)

    # -1 because adjacency list is 1-indexed, while igraph is 0-indexed
    edges = [
        (i, neighbour - 1)
        for i, neighbours in enumerate(adjacency)
        for neighbour in neighbours
        if i < neighbour - 1
    ]

    return ig.Graph(n=n, edges=edges, directed=directed)

def export_adjacency_list(graph: ig.Graph) -> list[list[int]]:
    """Converts graph into adjacency list"""
    n = graph.vcount()
    adjacency = [[] for _ in range(n)]

    for u, v in graph.get_edgelist():
        adjacency[u].append(v + 1)
        if not graph.is_directed():
            adjacency[v].append(u + 1)

    for neighbours in adjacency:
        neighbours.sort()

    return adjacency


###### Conversion


class GraphFormat(Enum):
    ADJACENCY_MATRIX = "Adjacency matrix"
    INCIDENCE_MATRIX = "Incidence matrix"
    ADJACENCY_LIST = "Adjacency list"


EXPORTS = {
    GraphFormat.ADJACENCY_MATRIX: export_adjacency_matrix,
    GraphFormat.INCIDENCE_MATRIX: export_incidence_matrix,
    GraphFormat.ADJACENCY_LIST: export_adjacency_list
}

PRINTS = {
    GraphFormat.ADJACENCY_MATRIX: print_matrix,
    GraphFormat.INCIDENCE_MATRIX: print_matrix,
    GraphFormat.ADJACENCY_LIST: print_adjacency_list
}


def save(data: list[list[int]], graph_format: GraphFormat, path: str) -> None:
    """Saves representation to a file (overwrites!)"""
    with open(path, "w") as file:
        PRINTS[graph_format](data, file)


def convert(graph: ig.Graph, graph_format: GraphFormat) -> list[list[int]]:
    """Converts graph into given representation"""
    return EXPORTS[graph_format](graph)

def export_igraph(graph: list[list[int]], format: GraphFormat, directed: bool = False) -> ig.Graph:
    """
    Converts graph from:
        - Adjacency matrix
        - Incidence matrix
        - Adjacency list
    into igraph.Graph
    """
    if format == GraphFormat.ADJACENCY_MATRIX:
        validate_adjacency_matrix(graph, directed)
        n= len(graph)
        if not directed:
            edges = [(i, j) for i in range(n) for j in range(i + 1, n) if graph[i][j] == 1]
        else:
            edges = [(i, j) for i in range(n) for j in range(n) if graph[i][j] == 1]
        igraph = ig.Graph(n=n, edges=edges, directed=directed)
        return igraph
    elif format == GraphFormat.INCIDENCE_MATRIX:
        validate_incidence_matrix(graph, directed)
        n = len(graph)
        edges = []
        for column in zip(*graph):
            if graph.is_directed():
                targets = [vertex for vertex, value in enumerate(column) if value == 1]
                source = [vertex for vertex, value in enumerate(column) if value == -1]
                edges.append((source[0], targets[0]))
            else:
                ends = [vertex for vertex, value in enumerate(column) if value == 1]
                edges.append((ends[0], ends[1]))
        igraph = ig.Graph(n=n, edges=edges, directed=directed)
        return igraph
    elif format == GraphFormat.ADJACENCY_LIST:
        validate_adjacency_list(graph, directed)
        n = len(graph)
        edges = [
            (i, neighbour - 1)
            for i, neighbours in enumerate(graph)
            for neighbour in neighbours
            if i < neighbour - 1
        ]
        igraph = ig.Graph(n=n, edges=edges, directed=directed)
        return igraph
    else:
        raise ValueError(f"Unsupported graph format: {format}")


if __name__ == "__main__":
    graph = import_adjacency_matrix("data/adjacency_matrix.txt")
    # graph = import_incidence_matrix("data/incidence_matrix.txt")

    for graph_format in EXPORTS:
        data = convert(graph, graph_format)
        print(graph_format.value)
        PRINTS[graph_format](data)
        print()

    # Saving to file example:
    # graph = import_adjacency_matrix("data/adjacency_matrix.txt")
    # adjacency_matrix = convert(graph, GraphFormat.ADJACENCY_MATRIX)
    # save(adjacency_matrix, GraphFormat.ADJACENCY_MATRIX, "adjacency_matrix.txt")
