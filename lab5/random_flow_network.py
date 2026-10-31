import random

import igraph as ig
from PIL import Image

from lab1.visualization import generate_visualization


class RandomFlowNetwork:
    def __init__(self, N: int) -> None:
        if N < 2:
            raise ValueError("Liczba pośrednich warstw powinna wynosić co najmniej 2")
        self.N = N
        self._initialize()

    def run(self) -> ig.Graph:
        self._initialize()
        self._generate_layers()
        self._generate_flow_edges()
        self._generate_random_edges()
        self._create_graph()
        return self.graph

    def _initialize(self) -> None:
        self.s = 0
        self.t = self.s
        self.layers = [(self.s,)]
        self.edges = []
        self.graph = ig.Graph(directed=True)

    def _generate_layers(self) -> None:
        for _ in range(1, self.N + 1):
            vertices_in_layer = random.randint(2, self.N)
            self.layers.append(
                tuple(self.t + vertex for vertex in range(1, vertices_in_layer + 1))
            )
            self.t += vertices_in_layer
        self.t += 1
        self.layers.append((self.t,))

    def _generate_flow_edges(self) -> None:
        for layer_id, vertices in enumerate(self.layers):
            if layer_id == 0:
                continue

            previous_layer = self.layers[layer_id - 1]
            not_seen = set(previous_layer)
            for vertex in vertices:
                if not_seen:
                    choice = random.choice(list(not_seen))
                    self.edges.append((choice, vertex))
                    not_seen.remove(choice)
                    continue

                choice = random.choice(previous_layer)
                self.edges.append((choice, vertex))

            for vertex in not_seen:
                self.edges.append((vertex, random.choice(vertices)))

    def _generate_random_edges(self) -> None:
        tails = range(self.s, self.t)
        heads = range(self.s + 1, self.t + 1)
        i = 0
        while i < 2 * self.N:
            u = random.choice(tails)
            v = random.choice(heads)

            # bez lukow przeciwnych - wymaga tego wzor na c_f(u, v) w Fordzie-Fulkersonie
            if u != v and (u, v) not in self.edges and (v, u) not in self.edges:
                self.edges.append((u, v))
                i += 1

    def _create_graph(self) -> None:
        self.graph.add_vertices(self.t + 1)
        for layer_id, vertices in enumerate(self.layers):
            self.graph.vs[vertices]["layer"] = layer_id
        self.graph.add_edges(self.edges)
        self.graph.es["weight"] = [random.randint(1, 10) for _ in self.edges]
        self.graph.vs[self.s]["label"] = "s"
        self.graph.vs[self.t]["label"] = "t"


def draw_flow_network(
    graph: ig.Graph, size: tuple[int, int] = (900, 500)
) -> Image.Image:
    width, height = size
    n_layers = max(graph.vs["layer"]) + 1
    column_width = width / n_layers

    positions = [(0, 0)] * graph.vcount()
    for layer in range(n_layers):
        same_layer = graph.vs.select(layer=layer).indices
        row_height = height / len(same_layer)
        x = (layer + 0.5) * column_width

        for row, vertex in enumerate(same_layer):
            y = (row + 0.5) * row_height
            positions[vertex] = (int(x), int(y))

    return generate_visualization(graph, positions, size)


if __name__ == "__main__":
    rfn = RandomFlowNetwork(3)
    draw_flow_network(rfn.run()).save("graph.png")
