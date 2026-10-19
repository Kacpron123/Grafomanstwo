import pytest
from lab1.validation import validate_adjacency_list, validate_adjacency_matrix, validate_incidence_matrix

def test_validate_adjacency_matrix_valid():
    valid_matrix = [
        [0, 1, 1],
        [1, 0, 0],
        [1, 0, 0],
    ]
    validate_adjacency_matrix(valid_matrix)


@pytest.mark.parametrize(
    "invalid_matrix, match_message",
    [
        ([], "Matrix is empty"),
        ([[0, 1], [1]], "Matrix is not a square!"),
        (
            [[0, 2], [2, 0]],
            "Matrix has different numbers than 1 and 0!",
        ),
        (
            [[1, 0], [0, 0]],
            "Diagonal does not have only 0!",
        ),
        (
            [[0, 1, 0], [0, 0, 0], [0, 0, 0]],
            "Matrix is not symmetrical!",
        ),
    ],
)
def test_validate_adjacency_matrix_invalid(invalid_matrix, match_message):
    with pytest.raises(ValueError, match=match_message):
        validate_adjacency_matrix(invalid_matrix)


def test_validate_incidence_matrix_valid():
    valid_matrix = [
        [1, 1],
        [1, 0],
        [0, 1],
    ]
    validate_incidence_matrix(valid_matrix)


@pytest.mark.parametrize(
    "invalid_matrix, match_message",
    [
        ([], "Matrix is empty"),
        ([[1, 0], [1]], "Rows have different lengths!"),
        (
            [[1, 2], [1, 0]],
            "Matrix has different numbers than 1 and 0!",
        ),
        (
            [[1, 0], [1, 0]],
            "All of the columns MUST have EXACTLY two vertices!",
        ),
        (
            [[1, 1], [1, 1]],
            "Edges cannot be multiple!",
        ),
    ],
)
def test_validate_incidence_matrix_invalid(invalid_matrix, match_message):
    with pytest.raises(ValueError, match=match_message):
        validate_incidence_matrix(invalid_matrix)


def test_validate_adjacency_list_valid():
    valid_adjacency = [
        [2, 3],
        [1],
        [1],
    ]
    validate_adjacency_list(valid_adjacency)


@pytest.mark.parametrize(
    "invalid_adjacency, match_message",
    [
        ([], "Matrix is empty"),
        (
            [[2], [1, 4]],
            r"Vertex 4 out of range \(1\.\.2\)",
        ),
        (
            [[1]],
            "Loops are not allowed in simple graphs!",
        ),
        (
            [[2, 2], [1]],
            "Vertex 1 has duplicate neighbours",
        ),
        (
            [[2], []],
            "Asymmetry detected: vertex 2 does not list 1 as neighbour!",
        ),
    ],
)
def test_validate_adjacency_list_invalid(invalid_adjacency, match_message):
    with pytest.raises(ValueError, match=match_message):
        validate_adjacency_list(invalid_adjacency)