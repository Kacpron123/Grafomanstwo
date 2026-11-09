"""
Zadanie 1: Algorytm PageRank dla digrafu (Błądzenie przypadkowe oraz Metoda potęgowa).
"""

import sys
import os
import random
import numpy as np

current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.abspath(os.path.join(current_dir, '..'))
sys.path.append(root_dir)

import igraph as ig
from lab1.representation import GraphFormat, convert
from lab1.random_graph.random_graph import generate_random_graph
from lab1.random_graph.enums import ErdosRenyiModel


def pagerank_random_walk(graph: ig.Graph, d: float = 0.15, steps: int = 100_000) -> dict[int, float]:
    """
    Metoda (a): Błądzenie przypadkowe z prawdopodobieństwem teleportacji d.
    """
    n = graph.vcount()
    visits = {i: 0 for i in range(n)}
    
    current_node = random.randint(0, n - 1)
    
    for _ in range(steps):
        visits[current_node] += 1
        
        neighbors = graph.neighbors(current_node, mode="out")
        
        if random.random() < d or not neighbors:
            current_node = random.randint(0, n - 1)
        else:
            current_node = random.choice(neighbors)

    pagerank_scores = {node: count / steps for node, count in visits.items()}
    return pagerank_scores


def pagerank_power_iteration(graph: ig.Graph, d: float = 0.15, max_iter: int = 1000, tol: float = 1e-7) -> dict[int, float]:
    """
    Metoda (b): Iteracja wektora obsadzeń (metoda potęgowa z macierzą stochastyczną P).
    """
    adj_matrix = convert(graph, GraphFormat.ADJACENCY_MATRIX)
    n = graph.vcount()
    A = np.array(adj_matrix, dtype=float)

    out_degrees = np.sum(A, axis=1)
    
    Q = np.zeros((n, n))
    for i in range(n):
        deg = out_degrees[i]
        if deg > 0:
            Q[i, :] = A[i, :] / deg
        else:
            Q[i, :] = 1.0 / n
            
    # Macierz stochastyczna P = (1 - d) * Q + (d / n) * J
    J = np.ones((n, n)) / n
    P = (1 - d) * Q + d * J
    
    p = np.ones(n) / n
    
    for _ in range(max_iter):
        p_next = np.dot(p, P)
        if np.linalg.norm(p_next - p, ord=1) < tol:
            p = p_next
            break
        p = p_next
        
    pagerank_scores = {i: float(p[i]) for i in range(n)}
    return pagerank_scores


if __name__ == "__main__":
    num_nodes = 6
    probability = 0.4
    
    print(f"Generowanie losowego digrafu dla n = {num_nodes}, p = {probability}")
    from lab1.representation import export_igraph
    
    adj_matrix = generate_random_graph(model=ErdosRenyiModel.G_N_P, num_nodes=num_nodes, edge_probability=probability, return_graph_format=GraphFormat.ADJACENCY_MATRIX)
    
    g_ig = export_igraph(adj_matrix, GraphFormat.ADJACENCY_MATRIX, directed=True)

    d_param = 0.15
    
    result_walk = pagerank_random_walk(g_ig, d=d_param, steps=200_000)
    result_power = pagerank_power_iteration(g_ig, d=d_param)
    
    sorted_walk = sorted(result_walk.items(), key=lambda x: x[1], reverse=True)
    sorted_power = sorted(result_power.items(), key=lambda x: x[1], reverse=True)
    
    print(f"\n{'Wierzchołek':<15} | {'Błądzenie Przypadkowe':<22} | {'Metoda Potęgowa':<20}")
    print("-" * 63)
    
    for (node_w, score_w), (node_p, score_p) in zip(sorted_walk, sorted_power):
        print(f"Strona {node_w:<8} | {score_w:<22.6f} | {score_p:<20.6f}")