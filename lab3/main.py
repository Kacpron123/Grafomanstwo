from lab3.dijkstra import dijkstra, print_dijkstra
from lab3.random_connected_graph import generate_random_connected_graph
from lab1.save import save_igraph_png
from pathlib import Path
from datetime import datetime
from lab3.distance_matrix import distance_matrix, print_distance_matrix
from lab3.center import center, minimax_center
from lab3.minimal_spaning_tree import minimal_spanning_tree

if __name__ == "__main__":
    #zad1
    source_node = 1
    num_nodes = 11
    min_num_edges = 15
    graph = generate_random_connected_graph(num_nodes=num_nodes, min_num_edges=min_num_edges)
    now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    path = Path("lab3") / "results" / f"random_connected_graph_{now}.png"
    text = f"Random Connected Graph: nodes: {graph.vcount()}, edges: {graph.ecount()}"
    save_igraph_png(graph, path, text)

    #zad2
    distances, previous_nodes = dijkstra(graph, source_node)
    print_dijkstra(distances, previous_nodes)
    print()

    #zad3
    dist_matrix = distance_matrix(graph)
    print_distance_matrix(dist_matrix)

    #zad4
    center_node, distances_sum = center(graph)
    print(f"Center node: {center_node}, Sum of distances: {distances_sum}")
    minimax_center_node, max_distance = minimax_center(graph)
    print(f"Minimax center node: {minimax_center_node}, Maximum distance: {max_distance}")

    #zad5
    graph = minimal_spanning_tree(graph)
    now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    path = Path("lab3") / "results" / f"mst_{now}.png"
    text = f"Minimal Spanning Tree: nodes: {graph.vcount()}, edges: {graph.ecount()}"
    save_igraph_png(graph, path, text)