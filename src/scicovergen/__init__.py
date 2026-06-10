"""
SciCoverGen - 科研封面自动生成工具

面向科研新手的论文封面、课题报告、学术海报一键图像生成工具。
基于 baoyu-cover-image skill 魔改，对接智谱 Cogview-3-Flash 免费图像生成接口。
"""

__version__ = "1.0.0"
__author__ = "SciCoverGen Team"
__license__ = "MIT"

from .generator import SciCoverGen

__all__ = ["SciCoverGen"]
