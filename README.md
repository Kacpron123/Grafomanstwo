# Grafomanstwo
Project repository for the Graphs course, containing implementations and solutions to assigned tasks.

[igraph documentation](https://python.igraph.org/en/stable/)

# Wymagania wstępne
- Python >= 3.14
- uv (fast Python package and environment manager)

## Installation uv:
Linux / macOS:
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```
Windows (PowerShell):
```ps1
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

# Setup
Synchronize dependencies and prepare the virtual environment:
```bash
uv sync
```
# Running scripts
Scripts can be run directly by path:
```sh
uv run python lab5/ford_fulkerson.py
```
or as modules:
```sh
uv run python -m lab5.ford_fulkerson
```
Example:

# Tests
Tests live in `tests/`, mirroring the `labN` directories.
```sh
uv run pytest                                          # all tests
uv run pytest tests/lab5                               # one lab
uv run pytest tests/lab5/test_ford_fulkerson.py        # one file
uv run pytest tests/lab5 -k bfs                        # tests matching a name
```
