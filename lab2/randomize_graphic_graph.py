import igraph as ig
import random

from lab1 import visualization
from lab2 import graphic_sequence
def randomize_graphic_graph(graph: ig.Graph) -> None:
    def rewire(graph: ig.Graph, n_steps) -> ig.Graph:
        n_verticies = graph.vcount()
        edges = [tuple(sorted(e.tuple)) for e in g.es]
        m = len(edges)

        if m < 2:
            return graph.copy()

        for _ in range(n_steps):
            idx1,idx2 = random.sample(range(m), 2)
            u1,v1 = edges[idx1]
            u2,v2 = edges[idx2]
            if len({u1,u2,v1,v2}) != 4:
                continue
            new_edge1 ,new_edge2 = (u1,v2),(u2,v1)
            if(new_edge1 in edges or new_edge2 in edges):
                continue
            edges.remove((u1,v1))
            edges.remove((u2,v2))
            edges.append(new_edge1)
            edges.append(new_edge2)
            return ig.Graph(n=n_verticies, edges=edges)
        return graph.copy()

    # check for density to determine if working on reverse graph
    n_edges = graph.ecount()
    n_vertices = graph.vcount()
    max_edges = n_vertices * (n_vertices - 1) // 2
    density = n_edges / max_edges if max_edges > 0 else 0

    use_complement = density > 0.5
    work_graph = graph.complementer(loops=False) if use_complement else g.copy()

    return_graph = rewire(work_graph, n_steps=1000)

    # Przywrócenie do pierwotnej postaci, jeśli robiliśmy dopełnienie
    if use_complement:
        return return_graph.complementer(loops=False)
    
    return return_graph

if __name__ == "__main__":
    graphic_seq = [6,6,6,4,4,3,3]
    g = graphic_sequence.build_graph_from_graphic_sequence(graphic_sequence)
    images=[]
    for i in range(100):
        g = randomize_graphic_graph(g)
        images.append(visualization.generate_visualization(g))
        visualization.generate_visualization(g).save("graph.png")
    visualization.build_GIF(images).save("graph.gif")