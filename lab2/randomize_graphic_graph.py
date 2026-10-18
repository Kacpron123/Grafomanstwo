import igraph as ig
import random

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
    from lab1 import visualization
    from lab2 import graphic_sequence
    g = graphic_sequence.build_graph_from_graphic_sequence([1, 3, 2, 3, 2, 4, 1])
    images=[]
    for i in range(10):
        g = randomize_graphic_graph(g)
        images.append(visualization.generate_visualization(g))
    visualization.build_GIF(images).save("graph.gif")