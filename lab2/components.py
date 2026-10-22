import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.abspath(os.path.join(current_dir, '..'))
sys.path.append(root_dir)
sys.path.append(os.path.join(root_dir, 'lab1'))

import igraph as ig
from lab1.representation import export_adjacency_list
from lab2.graphic_sequence import build_graph_from_graphic_sequence

def components_R(nr: int, v: int, adjacency: list[list[int]], comp: list[int]) -> None:
    """Rekurencyjny DFS (components_R) z alg_2.pdf"""
    comp[v] = nr
    for u in adjacency[v]:
        if comp[u] == -1:
            components_R(nr, u, adjacency, comp)

def find_connected_components(graph: ig.Graph) -> list[int]:
    """Algorytm 2: components(G) z alg_2.pdf"""
    n = graph.vcount()
    comp = [-1] * n
    nr = 0
    
    raw_adj = export_adjacency_list(graph)
    adjacency = [[neighbour - 1 for neighbour in neighbours] for neighbours in raw_adj]

    for v in range(n):
        if comp[v] == -1:
            nr += 1
            comp[v] = nr
            components_R(nr, v, adjacency, comp)
            
    return comp

def print_largest_component_info(graph: ig.Graph) -> None:
    """Wypisuje spójne składowe w formacie zgodnym z Listingiem 1 oraz wskazuje największą"""
    comp = find_connected_components(graph)
    
    components_dict = {}
    for vertex_idx, comp_id in enumerate(comp):
        if comp_id not in components_dict:
            components_dict[comp_id] = []
        components_dict[comp_id].append(vertex_idx + 1)
        
    max_comp_id = max(components_dict, key=lambda k: len(components_dict[k]))
    
    for comp_id, vertices in sorted(components_dict.items()):
        vertices_str = " ".join(map(str, vertices))
        print(f"{comp_id}) {vertices_str}")
        
    print(f"Największa składowa ma numer {max_comp_id}.")


if __name__ == "__main__":
    print("--- Test Zadania 3 połączonego z Zadaniem 1 (Ciąg graficzny) ---")
    
    sequence = [4, 2, 2, 3, 2, 1, 4, 2, 2, 2, 2]
    
    print(f"Wejściowy ciąg stopni: {sequence}")
    
    graph = build_graph_from_graphic_sequence(sequence)
    
    print("\nWynik (Listing 1):")
    print_largest_component_info(graph)