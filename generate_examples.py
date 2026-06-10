import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from scicovergen.plot_generator import PlotGenerator
from scicovergen.plot_styles import get_style_config
from scicovergen.diagram_renderer import render_diagram_from_architecture
import numpy as np

out_dir = "docs/images"
os.makedirs(out_dir, exist_ok=True)

# 1. Algorithm diagram
print("Generating diagram...")
architecture = {
    "layout": "horizontal_pipeline",
    "title": "Scalable Multi-View Spectral Clustering",
    "stages": [
        {
            "name": "Input",
            "color": "light_blue",
            "modules": [
                {"name": "Multi-View Data", "type": "input"},
            ]
        },
        {
            "name": "Graph",
            "color": "light_green",
            "modules": [
                {"name": "Graph Construction", "type": "processor"},
            ]
        },
        {
            "name": "Fusion",
            "color": "light_lavender",
            "modules": [
                {"name": "Min-Max Fusion", "type": "attention"},
            ]
        },
        {
            "name": "Embedding",
            "color": "light_yellow",
            "modules": [
                {"name": "Spectral Embedding", "type": "processor"},
            ]
        },
        {
            "name": "Clustering",
            "color": "light_coral",
            "modules": [
                {"name": "K-Means Clustering", "type": "decoder"},
            ]
        },
        {
            "name": "Output",
            "color": "light_blue",
            "modules": [
                {"name": "Cluster Assignments", "type": "output"},
            ]
        },
    ],
    "connections": [
        {"from": "Multi-View Data", "to": "Graph Construction"},
        {"from": "Graph Construction", "to": "Min-Max Fusion"},
        {"from": "Min-Max Fusion", "to": "Spectral Embedding"},
        {"from": "Spectral Embedding", "to": "K-Means Clustering"},
        {"from": "K-Means Clustering", "to": "Cluster Assignments"},
    ]
}
render_diagram_from_architecture(architecture, os.path.join(out_dir, "example_diagram.png"))

# 2. bar_paired_delta
print("Generating bar chart...")
pg = PlotGenerator()
data_bar = {
    "title": "Accuracy Comparison on CIFAR-10",
    "groups": ["SVM", "KNN", "RF", "Ours"],
    "baseline": [72.5, 68.3, 75.1, 70.0],
    "method": [78.2, 71.5, 79.8, 88.6],
    "delta": ["+5.7", "+3.2", "+4.7", "+18.6"],
    "ylabel": "Accuracy (%)",
}
pg.generate(data_bar, "bar_paired_delta", os.path.join(out_dir, "example_bar.png"))

# 3. line_confidence_band
print("Generating line chart...")
np.random.seed(0)
data_line = {
    "title": "Convergence Curve with 95% CI",
    "xlabel": "Epoch",
    "ylabel": "Validation Loss",
    "x": list(range(1, 51)),
    "series": [
        {
            "name": "Baseline",
            "mean": [2.5 - 0.02*i + np.random.normal(0, 0.03) for i in range(50)],
            "std": [0.15] * 50,
            "is_primary": False,
        },
        {
            "name": "Ours",
            "mean": [2.5 - 0.04*i + np.random.normal(0, 0.02) for i in range(50)],
            "std": [0.12] * 50,
            "is_primary": True,
        },
    ],
}
pg.generate(data_line, "line_confidence_band", os.path.join(out_dir, "example_line.png"))

# 4. scatter_tsne_cluster
print("Generating scatter plot...")
np.random.seed(42)
cluster_names = ["Cluster A", "Cluster B", "Cluster C", "Cluster D"]
points = {}
for name in cluster_names:
    cx, cy = np.random.randn(2) * 3
    pts = [(cx + np.random.randn(), cy + np.random.randn()) for _ in range(40)]
    points[name] = pts
data_scatter = {
    "title": "t-SNE Visualization of Learned Representations",
    "points": points,
    "labels": cluster_names,
}
pg.generate(data_scatter, "scatter_tsne_cluster", os.path.join(out_dir, "example_scatter.png"))

print("All examples generated in", out_dir)
