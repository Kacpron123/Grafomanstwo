###### Composing functions ######


def _check_square(matrix: list[list[int]]) -> None:
    """Raise ValueError if matrix is not a square (n x n)"""
    if not all(len(row) == len(matrix) for row in matrix):
        raise ValueError("Matrix is not a square!")


def _check_rows_equal_length(matrix: list[list[int]]) -> None:
    """Raise ValueError if rows in matrix are not equal (n x k)"""
    if not all(len(row) == len(matrix[0]) for row in matrix):
        raise ValueError("Rows have different lengths!")


def _check_symmetric(matrix: list[list[int]]) -> None:
    """Raise ValueError if matrix is not symmetrical"""
    n = len(matrix)
    if not all(matrix[i][j] == matrix[j][i] for i in range(n) for j in range(n)):
        raise ValueError("Matrix is not symmetrical!")


def _check_zero_diagonal(matrix: list[list[int]]) -> None:
    """Raise ValueError if matrix has other number than 0 on diagonal"""
    if not all(matrix[i][i] == 0 for i in range(len(matrix))):
        raise ValueError("Diagonal does not have only 0!")



def _check_two_vertices_per_edge(matrix: list[list[int]], directed: bool = False) -> None:
    """Raise ValueError if edge does not have EXACTLY two vertices"""
    if directed:
        if not all(sum(column) == 0 for column in zip(*matrix)):
            raise ValueError("All of the columns MUST have EXACTLY two vertices!")
    else:
        if not all(sum(column) == 2 for column in zip(*matrix)):
            raise ValueError("All of the columns MUST have EXACTLY two vertices!")


def _check_unique_edges(matrix: list[list[int]]) -> None:
    """Raise ValueError if there are multiple edges"""
    columns = list(zip(*matrix))
    if len(set(columns)) != len(columns):
        raise ValueError("Edges cannot be multiple!")


def _check_not_empty(matrix: list[list[int]]) -> None:
    """Raise ValueError if matrix is empty"""
    if not matrix:
        raise ValueError("Matrix is empty")
    
def _check_contains_only(matrix: list[list[int]], allowed_values: set[int]) -> None:
    """Raise ValueError if matrix contains values not in allowed_values"""
    if not all(value in allowed_values for row in matrix for value in row):
        raise ValueError(f"Matrix contains values not in {allowed_values}!")

###### Main functions ######


def validate_adjacency_matrix(matrix: list[list[int]], directed: bool = False) -> None:
    """Checks whether adjacency matrix describes a simple graph"""
    _check_not_empty(matrix)
    _check_square(matrix)
    _check_contains_only(matrix, {0, 1})
    _check_zero_diagonal(matrix)
    if not directed:
        _check_symmetric(matrix)




def validate_incidence_matrix(matrix: list[list[int]], directed: bool = False) -> None:
    """Raise ValueError if incidence matrix is invalid"""
    _check_not_empty(matrix)
    _check_rows_equal_length(matrix)
    if not directed:
        _check_contains_only(matrix, {0, 1})
    else:
        _check_contains_only(matrix, {0, 1, -1})
    _check_two_vertices_per_edge(matrix, directed)
    _check_unique_edges(matrix)

def _check_adjacency_list_valid_vertices(adjacency: list[list[int]]) -> None:
    """Raise ValueError if adjacency list contains invalid vertex indices"""
    n = len(adjacency)
    for vertex, neighbours in enumerate(adjacency, 1):
        for neighbour in neighbours:
            if not (1 <= neighbour <= n):
                raise ValueError(f"Vertex {neighbour} out of range (1..{n})!")
            if neighbour == vertex:
                raise ValueError("Loops are not allowed in simple graphs!")


def _check_adjacency_list_unique_neighbours(adjacency: list[list[int]]) -> None:
    """Raise ValueError if a vertex has duplicate neighbours (multiple edges)"""
    for vertex, neighbours in enumerate(adjacency, 1):
        if len(neighbours) != len(set(neighbours)):
            raise ValueError(f"Vertex {vertex} has duplicate neighbours (multiple edges are not allowed)!")


def _check_adjacency_list_symmetry(adjacency: list[list[int]]) -> None:
    """Raise ValueError if adjacency list is not symmetrical (if u has v, v must have u)"""
    # n = len(adjacency)
    for u, neighbours in enumerate(adjacency, 1):
        for v in neighbours:
            if u not in adjacency[v - 1]:
                raise ValueError(f"Asymmetry detected: vertex {v} does not list {u} as neighbour!")

def validate_adjacency_list(adjacency: list[list[int]], directed: bool = False) -> None:
    """Checks whether adjacency list describes a simple graph"""
    _check_not_empty(adjacency)
    _check_adjacency_list_valid_vertices(adjacency)
    _check_adjacency_list_unique_neighbours(adjacency)
    if not directed:
        _check_adjacency_list_symmetry(adjacency)
