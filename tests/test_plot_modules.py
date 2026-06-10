"""
测试 plot 相关模块：plot_styles、plot_generator、plot_reproducer
"""
import os
import tempfile
import unittest

import numpy as np
from PIL import Image

from scicovergen.plot_styles import get_style_config, list_styles
from scicovergen.plot_generator import PlotGenerator
from scicovergen.plot_reproducer import PlotReproducer


class TestPlotStyles(unittest.TestCase):
    """测试 plot_styles 模块"""

    def test_list_styles(self):
        styles = list_styles()
        self.assertEqual(len(styles), 8)
        expected = [
            "bar_paired_delta", "bar_grouped_hatch",
            "line_confidence_band", "line_training_curve", "line_loss_with_inset",
            "scatter_tsne_cluster", "scatter_broken_axis", "radar_dual_series",
        ]
        for s in expected:
            self.assertIn(s, styles)

    def test_get_style_config(self):
        config = get_style_config("bar_paired_delta")
        self.assertEqual(config["type"], "bar")
        self.assertIn("colors", config)
        self.assertIn("params", config)
        self.assertIn("required_data", config)

    def test_get_style_config_unknown(self):
        with self.assertRaises(ValueError):
            get_style_config("nonexistent_style")


class TestPlotGenerator(unittest.TestCase):
    """测试 plot_generator 模块"""

    def setUp(self):
        self.gen = PlotGenerator()
        self.tmpdir = tempfile.mkdtemp()

    def _get_output(self, name):
        return os.path.join(self.tmpdir, name)

    def test_bar_paired_delta(self):
        data = {
            "title": "Test Delta",
            "groups": ["A", "B", "C"],
            "baseline": [50, 60, 55],
            "method": [70, 75, 80],
            "delta": [20, 15, 25],
            "ylabel": "Accuracy (%)",
            "ylim": [0, 100],
        }
        out = self._get_output("bar_paired_delta.png")
        path = self.gen.generate(data, "bar_paired_delta", out)
        self.assertTrue(os.path.exists(path))
        self.assertGreater(os.path.getsize(path), 0)

    def test_line_confidence_band(self):
        data = {
            "title": "Test Line",
            "x": [0, 1, 2, 3, 4],
            "series": [
                {
                    "mean": [50, 55, 60, 58, 65],
                    "std": [2, 3, 3, 2, 3],
                    "name": "Method",
                    "is_primary": True,
                }
            ],
            "xlabel": "Epoch",
            "ylabel": "Accuracy",
        }
        out = self._get_output("line_confidence_band.png")
        path = self.gen.generate(data, "line_confidence_band", out)
        self.assertTrue(os.path.exists(path))
        self.assertGreater(os.path.getsize(path), 0)

    def test_scatter_tsne_cluster(self):
        np.random.seed(42)
        pts = np.random.randn(30, 2).tolist()
        data = {
            "title": "t-SNE",
            "points": {
                "Cluster A": pts[0:10],
                "Cluster B": pts[10:20],
                "Cluster C": pts[20:30],
            },
            "labels": ["Cluster A", "Cluster B", "Cluster C"],
        }
        out = self._get_output("scatter_tsne_cluster.png")
        path = self.gen.generate(data, "scatter_tsne_cluster", out)
        self.assertTrue(os.path.exists(path))
        self.assertGreater(os.path.getsize(path), 0)


class TestPlotReproducer(unittest.TestCase):
    """测试 plot_reproducer 模块"""

    def setUp(self):
        self.repro = PlotReproducer(api_client=None)
        self.tmpdir = tempfile.mkdtemp()

    def _create_test_image(self, name, size=(600, 400), color=(100, 150, 200)):
        path = os.path.join(self.tmpdir, name)
        img = Image.new("RGB", size, color)
        img.save(path, "PNG")
        return path

    def test_analyze_image(self):
        img_path = self._create_test_image("test_img.png", size=(800, 600), color=(200, 100, 50))
        analysis = self.repro._analyze_image(img_path)
        self.assertEqual(analysis["width"], 800)
        self.assertEqual(analysis["height"], 600)
        self.assertAlmostEqual(analysis["aspect_ratio"], 800/600, places=2)
        self.assertIn("figsize", analysis)
        self.assertIn("matched_style", analysis)

    def test_reproduce_without_llm(self):
        img_path = self._create_test_image("repro.png", size=(600, 400))
        out_path = os.path.join(self.tmpdir, "output_repro.png")
        result = self.repro.reproduce(img_path, out_path, use_llm=False)
        self.assertTrue(os.path.exists(result))
        self.assertGreater(os.path.getsize(result), 0)


if __name__ == "__main__":
    unittest.main()
