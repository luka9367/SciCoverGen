"""
科研内容智能分析器

基于 baoyu-cover-image 的 auto-selection 理念，
使用 GLM-4-Flash 自动分析科研文档，提取关键信息用于封面生成。
"""

import json
import re
from typing import Dict, List, Optional, Any

from .api_client import ZhipuClient


class ContentAnalyzer:
    """科研内容分析器"""

    def __init__(self, client: ZhipuClient = None):
        self.client = client or ZhipuClient()

    def analyze(self, content: str, scene: str = "paper_cover") -> Dict[str, str]:
        """
        分析科研内容

        Args:
            content: 文章内容文本
            scene: 场景类型 (paper_cover/project_report/academic_poster)

        Returns:
            分析结果字典
        """
        # 截取前 4000 字符进行分析
        truncated = content[:4000]

        if scene == "paper_cover":
            return self._analyze_paper(truncated)
        elif scene == "project_report":
            return self._analyze_project_report(truncated)
        elif scene == "academic_poster":
            return self._analyze_poster(truncated)
        else:
            return self._analyze_paper(truncated)

    def _analyze_paper(self, content: str) -> Dict[str, str]:
        """分析学术论文"""
        prompt = f"""你是一位学术论文可视化专家。请深度分析以下论文内容，提取可用于生成专业学术封面的精确视觉元素。

论文内容：
{content}

请严格按照以下格式输出（每点要具体、可视觉化，用中文）：

## 标题
[论文标题，精确提取]

## 核心方法
[用1-2句话精确描述论文的核心数学/算法方法]

## 关键数学对象
[列出3-5个可以可视化的数学对象，如：矩阵、图、流形、特征向量等]

## 核心操作
[描述算法的核心操作，如：分解、投影、融合、约束、谱分解、拉普拉斯矩阵等]

## 视觉隐喻
[提供一个精准的视觉隐喻，必须包含具体的数学/计算机视觉元素，例如"多路数据流汇聚到统一的谱分解网格"]

## 学科领域
[从以下选择最相关的：机器学习/聚类、图论/谱聚类、多视图学习、正则化/优化、深度学习、计算机视觉、自然语言处理、数据挖掘、强化学习、数学理论]

## 配色建议
[cool(冷色科技蓝)/warm(暖色亲和)/dark(深色高级)/vivid(鲜艳活力)/mono(黑白极简)/elegant(优雅)]

## 风格建议
[geometric(几何抽象)/flat-vector(扁平矢量)/digital(数字插画)/minimal(极简)]

## 情绪强度
[subtle(低调专业)/balanced(平衡)/bold(大胆突出)]

不要输出任何解释，只输出上述格式内容。"""

        result = self.client.chat_completion([{"role": "user", "content": prompt}], max_tokens=2000)
        return self._parse_analysis(result)

    def _analyze_project_report(self, content: str) -> Dict[str, str]:
        """分析课题报告"""
        prompt = f"""你是一位科研项目封面设计专家。请分析以下课题报告内容，提取关键信息用于生成专业封面。

报告内容：
{content}

请严格按照以下格式输出（用中文）：

## 标题
[报告标题]

## 项目类型
[基础研究/应用研究/技术开发/调研报告/实验报告]

## 核心内容
[2-3句话概括项目核心内容和目标]

## 关键词
[5-8个关键词]

## 视觉元素建议
[建议的视觉元素，如：实验器材、数据图表、流程图、原型产品、调研场景等]

## 配色建议
[cool/warm/dark/vivid/mono/elegant]

## 风格建议
[flat-vector/digital/minimal/geometric]

## 情绪强度
[subtle/balanced/bold]

不要输出解释。"""

        result = self.client.chat_completion([{"role": "user", "content": prompt}], max_tokens=2000)
        return self._parse_analysis(result)

    def _analyze_poster(self, content: str) -> Dict[str, str]:
        """分析学术海报"""
        prompt = f"""你是一位学术海报设计专家。请分析以下学术内容，提取关键信息用于生成海报封面。

内容：
{content}

请严格按照以下格式输出（用中文）：

## 标题
[海报标题]

## 研究类型
[理论研究/实验研究/系统演示/综述/新方法]

## 核心亮点
[3-5个研究亮点，适合在海报上突出展示]

## 视觉焦点
[海报最核心的视觉元素，如：系统架构图、实验结果图、对比图表、创新模型图等]

## 配色建议
[cool/warm/dark/vivid/mono/elegant]

## 风格建议
[flat-vector/digital/geometric/bold]

## 情绪强度
[bold(海报需要视觉冲击)/balanced]

不要输出解释。"""

        result = self.client.chat_completion([{"role": "user", "content": prompt}], max_tokens=2000)
        return self._parse_analysis(result)

    def extract_architecture(self, content: str, title: str = "") -> Dict[str, Any]:
        """
        提取论文的算法架构信息，用于生成精确的技术流程图

        Args:
            content: 论文内容文本
            title: 论文标题

        Returns:
            结构化架构数据字典，可直接传给 diagram_renderer
        """
        truncated = content[:3000]

        prompt = f"""你是一位计算机科学论文可视化专家。请分析以下论文内容，提取算法的模块化架构信息，用于生成技术流程图。

论文标题：{title}
论文内容（前3000字符）：
{truncated}

请严格按照以下 JSON 格式输出（不要有任何额外文字，只输出 JSON）：

{{
    "title": "论文标题",
    "layout": "horizontal_pipeline",
    "stages": [
        {{
            "name": "Stage 1: Input",
            "color": "light_blue",
            "modules": [
                {{"name": "Raw Data", "type": "input"}},
                {{"name": "Similarity Graph", "type": "data"}}
            ]
        }},
        {{
            "name": "Stage 2: Processing",
            "color": "light_green",
            "modules": [
                {{"name": "Graph Laplacian", "type": "processor"}},
                {{"name": "Spectral Embedding", "type": "processor"}},
                {{"name": "Min-Max Fusion", "type": "attention"}}
            ]
        }},
        {{
            "name": "Stage 3: Output",
            "color": "light_coral",
            "modules": [
                {{"name": "K-Means", "type": "output"}},
                {{"name": "Cluster Labels", "type": "output"}}
            ]
        }}
    ],
    "connections": [
        {{"from": "Raw Data", "to": "Similarity Graph"}},
        {{"from": "Similarity Graph", "to": "Graph Laplacian"}},
        {{"from": "Graph Laplacian", "to": "Spectral Embedding"}},
        {{"from": "Spectral Embedding", "to": "Min-Max Fusion"}},
        {{"from": "Min-Max Fusion", "to": "K-Means"}},
        {{"from": "K-Means", "to": "Cluster Labels"}}
    ]
}}

规则：
1. stages 数量 2-5 个，每个 stage 的 modules 数量 1-4 个
2. module 的 type 必须从以下选择：input, data, encoder, processor, decoder, output, attention, training, loss, auxiliary
3. stage 的 color 必须从以下选择：light_blue, light_green, light_yellow, light_coral, light_lavender, light_gray
4. layout 必须是 "horizontal_pipeline"
5. connections 必须正确连接所有 stage 之间的模块
6. 模块名称要简洁（1-3个英文单词），适合放在流程图框内
7. 只输出 JSON，不要任何解释、不要 markdown 代码块"""

        try:
            result = self.client.chat_completion(
                [{"role": "user", "content": prompt}],
                max_tokens=2000,
                temperature=0.3
            )
            # 清理可能的 markdown 代码块
            result = result.strip()
            if result.startswith("```"):
                result = result.split("\n", 1)[-1].rsplit("```", 1)[0].strip()
            if result.startswith("json"):
                result = result[4:].strip()

            architecture = json.loads(result)
            # 基础校验
            if "stages" not in architecture or "connections" not in architecture:
                raise ValueError("Missing required keys in architecture JSON")
            return architecture

        except Exception as e:
            print(f"[!] 架构提取失败 ({e})，使用默认架构")
            return self._default_architecture(title)

    @staticmethod
    def _default_architecture(title: str = "") -> Dict[str, Any]:
        """默认架构（当 LLM 提取失败时使用）"""
        return {
            "title": title or "Algorithm Architecture",
            "layout": "horizontal_pipeline",
            "stages": [
                {
                    "name": "Input",
                    "color": "light_blue",
                    "modules": [
                        {"name": "Raw Data", "type": "input"},
                        {"name": "Preprocess", "type": "data"}
                    ]
                },
                {
                    "name": "Processing",
                    "color": "light_green",
                    "modules": [
                        {"name": "Core Model", "type": "processor"},
                        {"name": "Attention", "type": "attention"}
                    ]
                },
                {
                    "name": "Output",
                    "color": "light_coral",
                    "modules": [
                        {"name": "Prediction", "type": "output"},
                        {"name": "Result", "type": "output"}
                    ]
                }
            ],
            "connections": [
                {"from": "Raw Data", "to": "Preprocess"},
                {"from": "Preprocess", "to": "Core Model"},
                {"from": "Core Model", "to": "Attention"},
                {"from": "Attention", "to": "Prediction"},
                {"from": "Prediction", "to": "Result"}
            ]
        }

    def _parse_analysis(self, text: str) -> Dict[str, str]:
        """解析分析结果"""
        info = {}
        patterns = {
            "title": r"## 标题\n(.+?)(?=\n##|$)",
            "core_method": r"## 核心方法\n(.+?)(?=\n##|$)",
            "math_objects": r"## 关键数学对象\n(.+?)(?=\n##|$)",
            "core_operation": r"## 核心操作\n(.+?)(?=\n##|$)",
            "visual_metaphor": r"## 视觉隐喻\n(.+?)(?=\n##|$)",
            "field": r"## 学科领域\n(.+?)(?=\n##|$)",
            "palette": r"## 配色建议\n(.+?)(?=\n##|$)",
            "style": r"## 风格建议\n(.+?)(?=\n##|$)",
            "mood": r"## 情绪强度\n(.+?)(?=\n##|$)",
            "project_type": r"## 项目类型\n(.+?)(?=\n##|$)",
            "keywords": r"## 关键词\n(.+?)(?=\n##|$)",
            "visual_elements": r"## 视觉元素建议\n(.+?)(?=\n##|$)",
            "highlights": r"## 核心亮点\n(.+?)(?=\n##|$)",
            "visual_focus": r"## 视觉焦点\n(.+?)(?=\n##|$)",
        }

        for key, pattern in patterns.items():
            match = re.search(pattern, text, re.DOTALL)
            if match:
                info[key] = match.group(1).strip()

        return info
