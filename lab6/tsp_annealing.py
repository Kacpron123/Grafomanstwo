"""
Zadanie 2: Problem Komiwojażera (TSP) przy użyciu symulowanego wyżarzania i operacji 2-opt.
"""

import math
import random
import time
from pathlib import Path
from PIL import Image, ImageDraw
from datetime import datetime


def load_tsp_data(filepath: str) -> list[tuple[float, float]]:
    """Wczytuje współrzędne wierzchołków z pliku .dat."""
    points = []
    with open(filepath, "r") as f:
        for line in f:
            parts = line.strip().split()
            if len(parts) >= 2:
                x, y = float(parts[0]), float(parts[1])
                points.append((x, y))
    return points


def calculate_distance(p1: tuple[float, float], p2: tuple[float, float]) -> float:
    """Oblicza odległość euklidesową między dwoma punktami."""
    return math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)


def calculate_total_distance(path: list[int], points: list[tuple[float, float]]) -> float:
    """Oblicza całkowitą długość zamkniętego cyklu Hamiltona."""
    total = 0.0
    n = len(path)
    for i in range(n):
        p1 = points[path[i]]
        p2 = points[path[(i + 1) % n]]
        total += calculate_distance(p1, p2)
    return total


def simulated_annealing(points: list[tuple[float, float]], max_it: int = 1500) -> tuple[list[int], float, float]:
    """
    Algorytm symulowanego wyżarzania z operacją 2-opt i kryterium Metropolisa-Hastingsa.
    """
    n = len(points)
    current_path = list(range(n))
    current_dist = calculate_total_distance(current_path, points)
    
    best_path = list(current_path)
    best_dist = current_dist
    
    print(f"Początkowa długość cyklu: {current_dist:.3f}")
    
    for i in range(100, 0, -1):
        T = 0.001 * (i ** 2)
        
        for _ in range(max_it):
            i_idx, j_idx = random.sample(range(n), 2)
            if abs(i_idx - j_idx) <= 1 or abs(i_idx - j_idx) == n - 1:
                continue
            if i_idx > j_idx:
                i_idx, j_idx = j_idx, i_idx
                
            new_path = current_path[:i_idx + 1] + current_path[i_idx + 1:j_idx + 1][::-1] + current_path[j_idx + 1:]
            new_dist = calculate_total_distance(new_path, points)
            
            delta = new_dist - current_dist
            
            if delta < 0 or random.random() < math.exp(-delta / T):
                current_path = new_path
                current_dist = new_dist
                
                if current_dist < best_dist:
                    best_path = list(current_path)
                    best_dist = current_dist
                    
    return best_path, best_dist


def draw_tsp_solution(points: list[tuple[float, float]], path: list[int], filename: str) -> None:
    """Rysuje znaleziony cykl Hamiltona i zapisuje do pliku PNG."""
    width, height = 1200, 700
    image = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(image)
    
    xs = [p[0] for p in points]
    ys = [p[1] for p in points]
    min_x, max_x = min(xs), max(xs)
    min_y, max_y = min(ys), max(ys)
    
    margin = 80
    usable_w = width - 2 * margin
    usable_h = height - 2 * margin
    
    def scale(pt):
        x = margin + (pt[0] - min_x) / (max_x - min_x) * usable_w if max_x != min_x else margin
        y = height - (margin + (pt[1] - min_y) / (max_y - min_y) * usable_h) if max_y != min_y else margin
        return (x, y)
        
    scaled_points = [scale(p) for p in points]
    
    n = len(path)
    for i in range(n):
        p1 = scaled_points[path[i]]
        p2 = scaled_points[path[(i + 1) % n]]
        draw.line([p1, p2], fill="red", width=2)
        
    for pt in scaled_points:
        r = 4
        draw.ellipse([pt[0] - r, pt[1] - r, pt[0] + r, pt[1] + r], fill="black")
        
    path_parent = Path(filename)
    path_parent.parent.mkdir(parents=True, exist_ok=True)
    image.save(filename)
    print(f"Zapisano wizualizację trasy do pliku: {filename}")


if __name__ == "__main__":
    data_path = Path("lab6") / "xqf_100_nodes_2026-11-09_20-39-16.dat"
    if not data_path.exists():
        data_path = Path("xqf131.dat")
        if not data_path.exists():
            data_path = Path("lab6") / "xqf131.dat"
        
    print(f"Wczytywanie danych z pliku {data_path}...")
    points = load_tsp_data(str(data_path))
    print(f"Wczytano wierzchołków: {len(points)}")
    
    start_time = time.time()
    best_path, best_distance = simulated_annealing(points, max_it=2000)
    end_time = time.time()

    print(f"\nZakończono optymalizację w czasie: {end_time - start_time:.2f} s")
    print(f"Końcowa długość zoptymalizowanego cyklu: {best_distance:.3f}")
    
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    
    input_file_stem = data_path.stem
    
    output_image_path = Path("lab6") / "results" / f"tsp_{input_file_stem}_result_{timestamp}.png"
    draw_tsp_solution(points, best_path, str(output_image_path))