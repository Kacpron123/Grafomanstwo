from lab4.random_strongly_connected_digraph import generate_random_strongly_connected_digraph
from pathlib import Path
from datetime import datetime
from lab1.save import save_igraph_png
from lab1.random_graph.random_graph import generate_random_graph, ErdosRenyiModel, GraphFormat
from lab1.representation import export_igraph
from lab4.kosaraju import kosaraju
from lab4.bellman_ford import bellman_ford
from lab1.random_graph.random_graph import add_weights_to_edges
from lab1.visualization import generate_visualization
from PIL import Image, ImageDraw
from datetime import datetime
from pathlib import Path
from lab4.johnson import johnson


if __name__ == "__main__":

    #zad1
    num_nodes = 10
    probability = 0.5
    model = ErdosRenyiModel.G_N_P
    graph = export_igraph(generate_random_graph(num_nodes=num_nodes, edge_probability=probability, model=model, directed=True), GraphFormat.ADJACENCY_MATRIX, directed=True)
    now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    path = Path("lab4") / "results" / f"random_digraph_{now}.png"
    path.parent.mkdir(parents=True, exist_ok=True)
    save_igraph_png(graph, path, f"Random Directed Graph: nodes: {graph.vcount()}, edges: {graph.ecount()}")

    #zad2
    result = kosaraju(graph)
    print(f"Kosaraju's Algorithm Result: {result}")

    #zad3
    graph, sub_graph = generate_random_strongly_connected_digraph(num_nodes, probability)
    graph = sub_graph
    now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    path = Path("lab4") / "results" / f"random_strongly_connected_digraph_{now}.png"
    text = f"Random Strongly Connected Digraph: nodes: {graph.vcount()}, edges: {graph.ecount()}"
    save_igraph_png(graph, path, text)

    # dodanie wag
    add_weights_to_edges(graph, range_weights=(-5, 10))