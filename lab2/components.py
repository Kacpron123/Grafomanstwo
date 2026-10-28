"""
Module for graph components analysis.

Implementation is taken from https://upel.agh.edu.pl/pluginfile.php/39501/mod_resource/content/6/alg_2.pdf
"""

import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.abspath(os.path.join(current_dir, '..'))
sys.path.append(root_dir)
sys.path.append(os.path.join(root_dir, 'lab1'))

from lab1.representation import GraphFormat, convert
import igraph as ig
from lab2.graphic_sequence import build_graph_from_graphic_sequence

def components_R(nr: int, v: int, graph: list[list[int]], comp: list[int]) -> None:
    """
    Recursive function to assign component numbers to connected nodes.
    
    Parameters:
        - nr: Current component number
        - v: Current node being processed
        - graph: Adjacency matrix representation of the graph
        - comp: List indicating the component number for each node
    """
    for u in range(len(graph)):
        if graph[v][u] == 1 and comp[u] == -1:  # if there's an edge and the node hasn't been assigned a component
            comp[u] = nr 
            components_R(nr, u, graph, comp)  # Recursively process the connected node

def components(graph: ig.Graph) -> list[int]:
    """
    Function that returns the number of connected components in a graph.
    
    Parameters:
        - graph: igraph.Graph object
        - directed (bool): Whether the graph is directed.
        
    Returns:
        - list[int], a list for each node indicating the component it belongs to.
    """
    adj_matrix = convert(graph, GraphFormat.ADJACENCY_MATRIX)
    
    nr = 0 # component number
    comp = [-1] * len(adj_matrix) # component list initialized to -1 for each node
    
    for v in range(len(adj_matrix)):
        if comp[v] == -1: # if the node has not been assigned a component
            nr += 1
            comp[v] = nr # assign the current node to the new component
            components_R(nr, v, adj_matrix, comp) # recursively assign component numbers to connected nodes

    return comp


def print_largest_component_info(graph: ig.Graph) -> None:
    """Wypisuje spójne składowe w formacie zgodnym z Listingiem 1 oraz wskazuje największą"""
    comp = components(graph)
    
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
    print("--- Zadanie 3 - Ciąg graficzny ---")
    
    sequence = [4, 2, 2, 3, 2, 1, 4, 2, 2, 2, 2]
    
    print(f"Wejściowy ciąg stopni: {sequence}")
    
    graph = build_graph_from_graphic_sequence(sequence)
    
    print("\nWynik:")
    print_largest_component_info(graph)