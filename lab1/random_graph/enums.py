"""Enums for the random graph module."""

from enum import StrEnum

class ErdosRenyiModel(StrEnum):
    """
    Erdős-Rényi model types.
    
    Where:
    - G(n, l) is a random graph with n vertices and l edges.
    - G(n, p) is a random graph with n vertices where each edge is included with probability p.
    """
    G_N_L = "G(n, l)"
    G_N_P = "G(n, p)"