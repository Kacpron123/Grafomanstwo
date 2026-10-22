import sys
import os
import random

current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.abspath(os.path.join(current_dir, '..'))
sys.path.append(root_dir)
sys.path.append(os.path.join(root_dir, 'lab1'))

import igraph as ig
from lab2.graphic_sequence import build_graph_from_graphic_sequence
from lab1.visualization import generate_visualization

def randomize_graph_locally(graph: ig.Graph, n_steps: int = 100) -> ig.Graph:
    """Lokalna funkcja randomizacji krawędzi dla grafu k-regularnego"""
    n_vertices = graph.vcount()
    edges = [tuple(sorted(e.tuple)) for e in graph.es]
    m = len(edges)

    if m < 2:
        return graph.copy()

    for _ in range(n_steps):
        if m < 2:
            break
        idx1, idx2 = random.sample(range(m), 2)
        u1, v1 = edges[idx1]
        u2, v2 = edges[idx2]
        
        if len({u1, u2, v1, v2}) != 4:
            continue
            
        new_edge1, new_edge2 = tuple(sorted((u1, v2))), tuple(sorted((u2, v1)))
        
        if new_edge1 in edges or new_edge2 in edges:
            continue
            
        edges[idx1] = new_edge1
        edges[idx2] = new_edge2
        
    return ig.Graph(n=n_vertices, edges=edges, directed=False)

def generate_k_regular_graph(n: int, k: int) -> ig.Graph:
    """Generuje losowy graf k-regularny dla zadanego n i k"""
    if n <= k:
        raise ValueError("Liczba wierzchołków n musi być większa niż stopień k (n > k).")
    if k % 2 != 0 and n % 2 != 0:
        raise ValueError("Jeśli stopień k jest nieparzysty, liczba wierzchołków n musi być parzysta.")
    
    sequence = [k] * n
    
    graph = build_graph_from_graphic_sequence(sequence)
    
    graph = randomize_graph_locally(graph, n_steps=100)
        
    return graph


if __name__ == "__main__":
    print("--- Test Zadania 5: Grafy k-regularne ---")
    
    n, k = 7, 2
    print(f"Generowanie grafu dla n = {n}, k = {k}...")
    
    graph = generate_k_regular_graph(n, k)
    
    img = generate_visualization(graph)
    output_filename = f"k_regular_n{n}_k{k}.png"
    img.save(output_filename)
    
    print(f"[SUKCES] Wygenerowano losowy graf k-regularny!")
    print(f"Liczba wierzchołków: {graph.vcount()}, Liczba krawędzi: {graph.ecount()}")
    print(f"Wizualizację zapisano do pliku: {output_filename}")