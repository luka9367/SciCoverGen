"""
科研内容智能分析器

基于 baoyu-cover-image 的 auto-selection 理念，
使用 GLM-4-Flash 自动分析科研文档，提取关键信息用于封面生成。
"""

import re
from typing import Dict, List, Optional

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
