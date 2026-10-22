from PIL import Image, ImageDraw
import igraph as ig
import math

SIZE = 500
# procent of halfradius
radius = 0.8 
RADIUS_NODE = 10

def generate_visualization(graph: ig.Graph) -> Image.Image:
    center = SIZE // 2
    radius = center * 0.8
    def calculate_pos(alpha: float) -> tuple[int, int]:
        x = center + radius * math.cos(alpha)
        y = center + radius * math.sin(alpha)
        return int(x), int(y)
    alpha = math.pi *2 / graph.vcount()
    positions = [calculate_pos(math.pi*3/2+alpha*x) for x in range(graph.vcount())]

    image = Image.new("RGB", (SIZE, SIZE), (255, 255, 255))
    draw = ImageDraw.Draw(image)
    for edge in graph.es:
        x1, y1 = positions[edge.source]
        x2, y2 = positions[edge.target]
        attrs = edge.attributes()
        color = attrs.get("color") or "gray"
        wid = attrs.get("width") or 2
        draw.line((x1, y1, x2, y2), fill=color, width=wid)
        # Draw the edge weight if it exists
        weight = attrs.get("weight")
        if weight is not None:
            mid_x = (x1 + x2) / 2 + 7  # Offset the text slightly to avoid overlapping with the edge
            mid_y = (y1 + y2) / 2 + 7
            draw.text((mid_x, mid_y), str(weight), fill="black", anchor="mm")

    for i, (x, y) in enumerate(positions):
        attrs = graph.vs[i].attributes()
        color = attrs.get("color") or "black"
        draw.ellipse(
            (x - RADIUS_NODE, y - RADIUS_NODE, x + RADIUS_NODE, y + RADIUS_NODE),
            fill="white",
            outline=color,
            width=3,
        )
        draw.text((x, y), str(i + 1), fill="black", anchor="mm")
    return image

class build_GIF:
    def __init__(self, images: list[Image.Image], duration=1000) -> None:
        self.images = images
        self.duration = duration

    def add_image(self, image: Image.Image):
        self.images.append(image)
    def save(self, path: str):
        self.images[0].save(
            path,
            save_all=True,
            append_images=self.images[1:],
            duration=self.duration,
            loop=0,
        )
# examples
if __name__ == "__main__":
    g = ig.Graph.Erdos_Renyi(n=15, p=1, directed=False)
    g.es[0]["color"] = "red"
    g.vs[3]["color"] = "green"
    generate_visualization(g).save("graph.png")

    gif_list = []
    for i in range(15):
        g.es[i]["color"] = "red"
        im = generate_visualization(g)
        gif_list.append(im)

    gif = build_GIF(gif_list)
    gif.save("graph.gif")