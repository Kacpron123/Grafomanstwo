"""
Module for graph components analysis.

Implementation is taken from https://upel.agh.edu.pl/pluginfile.php/39501/mod_resource/content/6/alg_2.pdf
"""

from lab1.representation import GraphFormat, convert
import igraph as ig

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
            comp[u] = nr  # Assign the current component number to the node
            components_R(nr, u, graph, comp)  # Recursively process the connected node

def components(graph: ig.Graph) -> list[int]:
    """
    Function that returns the number of connected components in a graph.
    
    Parameters:
        - graph: igraph.Graph object
        
    Returns:
        - list[int], a list for each node indicating the component it belongs to.
    """
    graph = convert(graph, GraphFormat.ADJACENCY_MATRIX)
    
    nr = 0 # component number
    comp = [-1] * len(graph) # component list initialized to -1 for each node
    
    for v in range(len(graph)):
        if comp[v] == -1: # if the node has not been assigned a component
            nr += 1 # increment component number
            comp[v] = nr # assign the current node to the new component
            components_R(nr, v, graph, comp) # recursively assign component numbers to connected nodes

    return comp
    
    