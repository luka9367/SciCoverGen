"""
核心功能测试
"""

import os
import unittest
from unittest.mock import Mock, patch

from scicovergen.prompts import LLMPromptBuilder, PromptBuilder
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


class TestLLMPromptBuilder(unittest.TestCase):
    """测试 LLM 动态 Prompt 生成器"""

    def test_build_user_prompt_structure(self):
        """测试 user prompt 结构正确"""
        analysis = {
            "title": "Test Paper",
            "core_method": "Spectral clustering",
            "field": "机器学习/聚类",
            "palette": "cool",
            "style": "geometric",
            "mood": "subtle",
        }
        user_prompt = LLMPromptBuilder._build_user_prompt(analysis, "paper_cover")

        self.assertIn("学术论文封面", user_prompt)
        self.assertIn("Spectral clustering", user_prompt)
        self.assertIn("cool", user_prompt)
        self.assertIn("5 维度配置", user_prompt)
        self.assertIn("NO text", user_prompt)

    def test_static_build_fallback(self):
        """测试静态模板 fallback"""
        analysis = {
            "title": "Fallback Test",
            "core_method": "Test",
            "palette": "cool",
            "style": "geometric",
            "mood": "subtle",
        }
        prompt = LLMPromptBuilder._static_build(analysis, "paper_cover")
        self.assertIn("Fallback Test", prompt)
        self.assertIn("NO text", prompt)

    @patch("scicovergen.prompts.LLMPromptBuilder._build_user_prompt")
    def test_build_prompt_llm_success(self, mock_build_user):
        """测试 LLM 成功生成 prompt"""
        mock_client = Mock()
        mock_client.chat_completion.return_value = "A luminous hypersphere with crystalline facets..."

        analysis = {"title": "Test", "palette": "cool"}
        result = LLMPromptBuilder.build_prompt(analysis, "paper_cover", mock_client)

        mock_client.chat_completion.assert_called_once()
        self.assertEqual(result, "A luminous hypersphere with crystalline facets...")

    @patch("scicovergen.prompts.LLMPromptBuilder._static_build")
    def test_build_prompt_llm_failure_fallback(self, mock_static):
        """测试 LLM 失败时回退到静态模板"""
        mock_client = Mock()
        mock_client.chat_completion.side_effect = Exception("API Error")
        mock_static.return_value = "fallback prompt"

        analysis = {"title": "Test", "palette": "cool"}
        result = LLMPromptBuilder.build_prompt(analysis, "paper_cover", mock_client)

        self.assertEqual(result, "fallback prompt")
        mock_static.assert_called_once()


if __name__ == "__main__":
    unittest.main()
