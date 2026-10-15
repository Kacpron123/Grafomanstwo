def read_lines(path: str) -> list[str]:
    """Reads file, returns without new line character"""
    with open(path, "r") as file:
        return [stripped for line in file if (stripped := line.strip())]


def parse_to_int(text: str) -> list[int]:
    """
    '1 0 1' -> [1, 0, 1]
    Accepts spaces as separators
    """
    return list(map(int, text.split()))


def read_matrix(path: str) -> list[list[int]]:
    """Reads an adjacency or incidence matrix from a file"""
    return [parse_to_int(line) for line in read_lines(path)]


def print_matrix(matrix: list[list[int]], file=None) -> None:
    """Prints matrix to the screen or to an open file if given"""
    for row in matrix:
        print(*row, file=file)

def print_adjacency_list(adjacency: list[list[int]], file=None) -> None:
    """Prints adjacency list to the screen or to an open file if given"""
    for vertex, neighbours in enumerate(adjacency, 1):
        print(f"{vertex}.", *neighbours, file=file)