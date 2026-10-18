import igraph as ig

from lab1.visualization import generate_visualization

def validate_graphic_sequence(sequence: list[int]) -> bool:
    n=len(sequence)
    degrees = sorted(sequence, reverse=True)
    
    if sum(1 for d in sequence if d % 2 != 0) % 2 != 0:
        return False
    if any(d >= n for d in sequence):
        return False
    
    while True:
        if all(degrees[i] == 0 for i in range(n)):
            return True
        elif any(degrees[i] < 0 for i in range(n)):
            return False
        for i in range(1,degrees[0]+1):
            degrees[i]-=1
        degrees[0]=0
        degrees.sort(reverse=True)

def build_graph_from_graphic_sequence(sequence: list[int], gif=False) -> ig.Graph:
    images = []
    degrees = sequence.copy()
    n=len(sequence)
    if not validate_graphic_sequence(degrees) or any(d < 0 for d in degrees) or sum(degrees)%2 != 0:
        raise ValueError("Invalid graphic sequence")
    ret_graph = ig.Graph(n=len(sequence))
    if gif:
        images.append(generate_visualization(ret_graph))
    while True:
        order = sorted(range(n), key = lambda i: degrees[i], reverse=True)
        u = order[0]
        d_max = degrees[u]
        if d_max==0:
            if gif:
                from lab1 import visualization
                visualization.build_GIF(images).save("graph.gif")
            return ret_graph
        for i in range(1, d_max+1):
            v = order[i]
            ret_graph.add_edge(u, v, color="red")
            degrees[v]-=1
        if gif:
            images.append(generate_visualization(ret_graph))
            for red_edge in ret_graph.es.select(color="red"):
                red_edge["color"] = None
        degrees[u]=0


if __name__ == "__main__":
    build_graph_from_graphic_sequence([1,3,3,4,2,2,1],gif=True)