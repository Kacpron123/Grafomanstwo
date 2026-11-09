"""
Generator losowych danych dla problemu komiwojażera (TSP)
z unikalną nazwą zawierającą datę i godzinę.
"""

import random
from datetime import datetime
from pathlib import Path

def generate_custom_tsp_dataset(num_nodes: int = 80) -> str:
    """Generuje losowe punkty na planszy i zapisuje plik z datą i godziną."""
    
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"xqf_{num_nodes}_nodes_{timestamp}.dat"
    
    filepath = Path("lab6") / filename
    filepath.parent.mkdir(parents=True, exist_ok=True)
    
    points = []
    for _ in range(num_nodes):
        x = round(random.uniform(0.0, 100.0), 3)
        y = round(random.uniform(0.0, 50.0), 3)
        points.append((x, y))
        
    with open(filepath, "w") as f:
        for p in points:
            f.write(f"{p[0]} {p[1]}\n")
            
    print(f"Wygenerowano nowy zestaw danych!")
    print(f"Liczba wierzchołków: {num_nodes}")
    print(f"Zapisano do pliku: {filepath.absolute()}")
    
    return str(filepath)

if __name__ == "__main__":
    generate_custom_tsp_dataset(num_nodes=100)