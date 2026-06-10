"""
核心功能测试
"""

import os
import unittest
from unittest.mock import Mock, patch

from scicovergen.prompts import PromptBuilder
from scicovergen.utils import read_file, slugify


class TestUtils(unittest.TestCase):
    """测试工具函数"""

    def test_slugify(self):
        """测试文件名转换"""
        self.assertEqual(slugify("Hello World"), "Hello-World")
        self.assertEqual(slugify("多视图谱聚类"), "多视图谱聚类")
        self.assertEqual(slugify("Test!!!123"), "Test-123")

    def test_read_file_not_found(self):
        """测试读取不存在的文件"""
        result = read_file("nonexistent_file.txt")
        self.assertIsNone(result)


class TestPromptBuilder(unittest.TestCase):
    """测试 Prompt 构建器"""

    def test_build_paper_cover_prompt(self):
        """测试论文封面 Prompt 构建"""
        analysis = {
            "title": "Test Paper",
            "core_method": "Spectral clustering",
            "math_objects": "Matrix, Graph",
            "core_operation": "Decomposition",
            "visual_metaphor": "Data streams converging",
            "field": "机器学习/聚类",
            "palette": "cool",
            "style": "geometric",
            "mood": "subtle",
        }
        prompt = PromptBuilder.build_paper_cover_prompt(analysis)

        self.assertIn("Spectral clustering", prompt)
        self.assertIn("NO text", prompt)
        self.assertIn("NO Chinese characters", prompt)
        self.assertIn("Matrix", prompt)

    def test_build_project_report_prompt(self):
        """测试课题报告 Prompt 构建"""
        analysis = {
            "title": "Project Report",
            "project_type": "Research",
            "keywords": "AI, ML",
            "visual_elements": "Charts",
            "palette": "cool",
            "style": "flat-vector",
            "mood": "balanced",
        }
        prompt = PromptBuilder.build_project_report_prompt(analysis)

        self.assertIn("Project Report", prompt)
        self.assertIn("NO text", prompt)

    def test_build_academic_poster_prompt(self):
        """测试学术海报 Prompt 构建"""
        analysis = {
            "title": "Poster Title",
            "highlights": "Novel method",
            "visual_focus": "Architecture diagram",
            "palette": "vivid",
            "style": "digital",
            "mood": "bold",
        }
        prompt = PromptBuilder.build_academic_poster_prompt(analysis)

        self.assertIn("Poster Title", prompt)
        self.assertIn("Bold", prompt)


if __name__ == "__main__":
    unittest.main()
