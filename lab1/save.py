import igraph as ig
from datetime import datetime
from pathlib import Path
from PIL import ImageDraw
from lab1.visualization import generate_visualization

def save_igraph_png(graph: ig.Graph, path: str | Path, text: str) -> None:
    """Saves igraph graph to a PNG file"""
    image = generate_visualization(graph)
    path.parent.mkdir(parents=True, exist_ok=True)
    draw = ImageDraw.Draw(image)
    draw.text((10, 10), text, fill="black")
    image.save(path)