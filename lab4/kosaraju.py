""" Implementation of the Kosaraju algorithm for finding strongly connected components in a directed graph."""

import igraph as ig

def dfs(G: ig.Graph, v: int, d: list[int], f: list[int], t: int) -> int:
    """
    Depth-First Search (DFS) to compute discovery and finish times of nodes.
    
    Args:
        G (ig.Graph): The directed graph.
        v (int): The current node being visited.
        d (list[int]): List to store discovery times of nodes.
        f (list[int]): List to store finish times of nodes.
        t (int): Global time counter for DFS.
        
    Returns:
        int: Updated global time counter after visiting the node and its descendants.
    """
    t += 1  # Increment global time counter
    d[v] = t  # Set discovery time for the current node
    
    for u in G.neighbors(v, mode="out"):  # Explore all outgoing neighbors
        if d[u] == -1:  # If the neighbor hasn't been visited yet
            t = dfs(G, u, d, f, t)  # Recursively visit the neighbor
    
    t += 1  # Increment global time counter
    f[v] = t  # Set finish time for the current node
    return t

def components_r(nr: int, v: int, G_transpose: ig.Graph, comp: list[int]) -> None:
    """
    Recursively assign component numbers to connected nodes in the transposed graph.
    
    Args:
        nr (int): The component number to assign.
        v (int): The current node being visited.
        G_transpose (ig.Graph): The transposed graph.
        comp (list[int]): The list of component assignments for each node.
    """    
    for u in G_transpose.neighbors(v, mode="out"):  # Explore all outgoing neighbors in the transposed graph
        if comp[u] == -1:  # If the neighbor hasn't been assigned to a component yet
            comp[u] = nr  # Assign the current component number to the neighbor
            components_r(nr, u, G_transpose, comp)  # Recursively visit the neighbor


def kosaraju(G: ig.Graph) -> list[int]:
    """
    Kosaraju's algorithm for finding strongly connected components in a directed graph.
    
    Args:
        G (ig.Graph): A directed graph represented as an igraph.Graph object.
        
    Returns:
        list[list[int]]: A list of strongly connected components, where each component is represented as a list of node indices.
    """
    d = [-1] * G.vcount()  # Discovery times of nodes
    f = [-1] * G.vcount()  # Finish times of nodes
    
    t = 0  # Global time counter for DFS
    for v in range(G.vcount()):
        if d[v] == -1:
            t = dfs(G, v, d, f, t)
            
    G_transpose = G.copy()
    G_transpose.reverse_edges()
        
    nr = 0  # Component number
    comp: list[int] = [-1] * G.vcount()  # Component list initialized to -1
    
    for v in sorted(range(G.vcount()), key=lambda x: f[x], reverse=True):  # Process nodes in decreasing order of finish times
        if comp[v] == -1:  # If the node hasn't been assigned to a component yet
            nr += 1  # Increment component number
            comp[v] = nr  # Assign the current node to the new component
            components_r(nr, v, G_transpose, comp)  # Recursively assign component numbers to connected nodes in the transposed graph
            
    return comp

if __name__ == "__main__":
    from lab3.random_connected_graph import generate_random_connected_graph
    from lab1.random_graph.random_graph import generate_random_graph
    from datetime import datetime
    from pathlib import Path
    from PIL import Image, ImageDraw
    from lab1.visualization import generate_visualization
    from lab1.representation import export_igraph
    from lab1.representation import GraphFormat
    from lab1.random_graph.enums import ErdosRenyiModel
    # Example usage
    num_nodes = 12
    probability = 0.3
    model = ErdosRenyiModel.G_N_P
    graph = export_igraph(generate_random_graph(num_nodes=num_nodes, edge_probability=probability, model=model, directed=True), GraphFormat.ADJACENCY_MATRIX, directed=True)
    #graph = generate_random_connected_graph(num_nodes=num_nodes, min_num_edges=min_num_edges, directed=True)
    now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    path = Path("lab4") / "results" / f"kosaraju_{now}.png"
    path.parent.mkdir(parents=True, exist_ok=True)
    image: Image.Image = generate_visualization(graph)
    draw = ImageDraw.Draw(image)
    image.save(path.absolute().as_posix())
    result = kosaraju(graph)
    draw.text((10, 10), f"Kosaraju's Algorithm Result: {result}", fill="black")
    image.save(path.absolute().as_posix())