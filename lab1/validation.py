###### Composing functions ######


def _check_square(matrix: list[list[int]]) -> None:
    """Raise ValueError if matrix is not a square (n x n)"""
    if not all(len(row) == len(matrix) for row in matrix):
        raise ValueError("Matrix is not a square!")


def _check_rows_equal_length(matrix: list[list[int]]) -> None:
    """Raise ValueError if rows in matrix are not equal (n x k)"""
    if not all(len(row) == len(matrix[0]) for row in matrix):
        raise ValueError("Rows have different lengths!")


def _check_zeroes_and_ones(matrix: list[list[int]]) -> None:
    """Raise ValueError if matrix has different numbers than 1 and 0!"""
    if not all(value in (0, 1) for row in matrix for value in row):
        raise ValueError("Matrix has different numbers than 1 and 0!")


def _check_symmetric(matrix: list[list[int]]) -> None:
    """Raise ValueError if matrix is not symmetrical"""
    n = len(matrix)
    if not all(matrix[i][j] == matrix[j][i] for i in range(n) for j in range(n)):
        raise ValueError("Matrix is not symmetrical!")


def _check_zero_diagonal(matrix: list[list[int]]) -> None:
    """Raise ValueError if matrix has other number than 0 on diagonal"""
    if not all(matrix[i][i] == 0 for i in range(len(matrix))):
        raise ValueError("Diagonal does not have only 0!")


def _check_two_vertices_per_edge(matrix: list[list[int]]) -> None:
    """Raise ValueError if edge does not have EXACTLY two vertices"""
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


###### Main functions ######


def validate_adjacency_matrix(matrix: list[list[int]]) -> None:
    """Checks whether adjacency matrix describes a simple graph"""
    _check_not_empty(matrix)
    _check_square(matrix)
    _check_zeroes_and_ones(matrix)
    _check_zero_diagonal(matrix)
    _check_symmetric(matrix)


def validate_incidence_matrix(matrix: list[list[int]]) -> None:
    """Checks whether incidence matrix describes a simple graph"""
    _check_not_empty(matrix)
    _check_rows_equal_length(matrix)
    _check_zeroes_and_ones(matrix)
    _check_two_vertices_per_edge(matrix)
    _check_unique_edges(matrix)
