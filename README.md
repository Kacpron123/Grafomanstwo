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

# setup
Synchronize dependencies and prepare the virtual environment:
```bash
uv sync
```
# Execute scripts as modules:
```sh
uv run python -m path.to.module
```
Example:
```sh
uv run python -m lab1.visualization
```
