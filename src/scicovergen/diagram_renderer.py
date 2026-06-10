"""
Conference Diagram Renderer

使用 Matplotlib 根据结构化架构数据生成精确的矢量流程图。
风格：NeurIPS/ICLR/CCF-A 顶会论文配图风格
- Pastel 马卡龙配色
- 扁平 2D 矢量
- 圆角矩形模块 + 细箭头数据流
- 文字清晰可读
- 输出 PNG/SVG，可直接用于论文
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Circle, Rectangle
import numpy as np
from typing import Dict, List, Tuple, Optional, Any
import os


class ConferenceDiagramRenderer:
    """
    顶会论文流程图渲染器

    支持三种布局模板：
    - horizontal_pipeline: 水平流水线 (Input -> Processing -> Output)
    - encoder_decoder: 编码器-解码器 (U型或对称结构)
    - multi_branch: 多分支并行 (一个输入，多路处理，融合输出)
    """

    # Pastel 马卡龙配色
    COLORS = {
        "light_blue": "#D5DEFF",
        "light_green": "#C8E5B3",
        "light_yellow": "#E3F2D9",
        "light_coral": "#FFD4C7",
        "light_lavender": "#E8D5FF",
        "light_gray": "#D4D4D4",
        "white": "#FFFFFF",
        "deep_navy": "#2C3E50",
        "soft_black": "#333333",
    }

    # 模块类型到颜色的映射
    MODULE_TYPE_COLORS = {
        "input": "light_blue",
        "data": "light_blue",
        "encoder": "light_green",
        "processor": "light_green",
        "decoder": "light_coral",
        "output": "light_coral",
        "attention": "light_lavender",
        "training": "light_yellow",
        "loss": "light_yellow",
        "auxiliary": "light_gray",
        "default": "light_gray",
    }

    # 图标映射 (使用 Unicode 几何符号)
    ICONS = {
        "input": "\u25A0",      # 方块
        "data": "\u25A0",
        "encoder": "\u25B2",    # 三角
        "processor": "\u25C6",  # 菱形
        "decoder": "\u25BC",    # 倒三角
        "output": "\u25CF",     # 圆点
        "attention": "\u2605",  # 星
        "training": "\u2699",   # 齿轮
        "loss": "\u2211",       # 求和
        "auxiliary": "\u25CB",  # 空心圆
        "default": "\u25A1",    # 空心方块
    }

    def __init__(self, figsize: Tuple[int, int] = (14, 10), dpi: int = 300):
        self.figsize = figsize
        self.dpi = dpi
        self.fig, self.ax = plt.subplots(1, 1, figsize=figsize)
        self.ax.set_xlim(0, 100)
        self.ax.set_ylim(0, 100)
        self.ax.axis('off')
        self.ax.set_facecolor(self.COLORS["white"])
        self.fig.patch.set_facecolor(self.COLORS["white"])

    def _get_color(self, module_type: str) -> str:
        """根据模块类型获取颜色"""
        color_key = self.MODULE_TYPE_COLORS.get(module_type, "default")
        return self.COLORS[color_key]

    def _get_icon(self, module_type: str) -> str:
        """根据模块类型获取图标"""
        return self.ICONS.get(module_type, self.ICONS["default"])

    def draw_module(self, x: float, y: float, width: float, height: float,
                    label: str, module_type: str = "default",
                    fontsize: int = 9, fontweight: str = "medium",
                    icon: Optional[str] = None) -> Dict[str, float]:
        """
        绘制单个模块（圆角矩形 + 文字标签 + 小图标）

        Returns:
            模块边界框 {"x1", "y1", "x2", "y2", "cx", "cy"}
        """
        color = self._get_color(module_type)
        x1, y1 = x - width / 2, y - height / 2
        x2, y2 = x + width / 2, y + height / 2

        # 圆角矩形
        box = FancyBboxPatch(
            (x1, y1), width, height,
            boxstyle="round,pad=0.02,rounding_size=1.2",
            facecolor=color,
            edgecolor=self.COLORS["deep_navy"],
            linewidth=1.5,
            zorder=2
        )
        self.ax.add_patch(box)

        # 图标 (左上角小区域)
        if icon is None:
            icon = self._get_icon(module_type)
        self.ax.text(
            x1 + 1.5, y2 - 1.5, icon,
            ha='left', va='top',
            fontsize=fontsize + 2,
            color=self.COLORS["deep_navy"],
            fontfamily='sans-serif',
            zorder=3
        )

        # 文字标签 (居中)
        self.ax.text(
            x, y - 0.5, label,
            ha='center', va='center',
            fontsize=fontsize,
            color=self.COLORS["soft_black"],
            fontweight=fontweight,
            fontfamily='sans-serif',
            wrap=True,
            zorder=3
        )

        return {"x1": x1, "y1": y1, "x2": x2, "y2": y2, "cx": x, "cy": y}

    def draw_arrow(self, x1: float, y1: float, x2: float, y2: float,
                   style: str = "->", color: Optional[str] = None,
                   linewidth: float = 1.2, linestyle: str = "-"):
        """绘制箭头连接线"""
        if color is None:
            color = self.COLORS["deep_navy"]

        arrow = FancyArrowPatch(
            (x1, y1), (x2, y2),
            arrowstyle=style,
            color=color,
            linewidth=linewidth,
            linestyle=linestyle,
            mutation_scale=12,
            zorder=1
        )
        self.ax.add_patch(arrow)

    def draw_group_box(self, x: float, y: float, width: float, height: float,
                       label: str, color_key: str = "light_gray"):
        """绘制分组框（虚线背景块 + 标签）"""
        # 背景色块
        bg = FancyBboxPatch(
            (x - width / 2, y - height / 2), width, height,
            boxstyle="round,pad=0.02,rounding_size=2",
            facecolor=self.COLORS[color_key],
            edgecolor=self.COLORS["deep_navy"],
            linewidth=1.0,
            linestyle='--',
            alpha=0.4,
            zorder=0
        )
        self.ax.add_patch(bg)

        # 分组标签
        self.ax.text(
            x, y + height / 2 + 1.5, label,
            ha='center', va='bottom',
            fontsize=10,
            color=self.COLORS["deep_navy"],
            fontweight='bold',
            fontfamily='sans-serif',
            style='italic',
            zorder=1
        )

    def render(self, architecture: Dict[str, Any], output_path: str) -> str:
        """
        根据结构化架构数据渲染流程图

        architecture 格式:
        {
            "title": "论文标题",
            "layout": "horizontal_pipeline",  # 或 "encoder_decoder", "multi_branch"
            "stages": [
                {
                    "name": "Stage 1: Input",
                    "color": "light_blue",
                    "modules": [
                        {"name": "Raw Data", "type": "input", "icon": "optional"}
                    ]
                }
            ],
            "connections": [
                {"from": "Raw Data", "to": "Preprocessor", "style": "->"}
            ]
        }
        """
        layout = architecture.get("layout", "horizontal_pipeline")

        if layout == "horizontal_pipeline":
            self._render_horizontal_pipeline(architecture)
        elif layout == "encoder_decoder":
            self._render_encoder_decoder(architecture)
        elif layout == "multi_branch":
            self._render_multi_branch(architecture)
        else:
            self._render_horizontal_pipeline(architecture)

        # 标题
        title = architecture.get("title", "")
        if title:
            self.ax.text(
                50, 96, title,
                ha='center', va='top',
                fontsize=13,
                color=self.COLORS["deep_navy"],
                fontweight='bold',
                fontfamily='sans-serif'
            )

        plt.tight_layout()
        plt.savefig(
            output_path,
            dpi=self.dpi,
            bbox_inches='tight',
            facecolor=self.COLORS["white"],
            edgecolor='none',
            pad_inches=0.3
        )
        plt.close()
        return output_path

    def _render_horizontal_pipeline(self, architecture: Dict[str, Any]):
        """渲染水平流水线布局"""
        stages = architecture.get("stages", [])
        if not stages:
            return

        n_stages = len(stages)
        stage_width = 80 / max(n_stages, 1)
        start_x = 10 + stage_width / 2

        module_positions = {}  # 记录每个模块的位置用于画箭头

        for i, stage in enumerate(stages):
            sx = start_x + i * stage_width
            modules = stage.get("modules", [])
            n_modules = len(modules)

            # 绘制分组框
            group_height = max(n_modules * 14 + 10, 30)
            self.draw_group_box(
                sx, 50, stage_width - 4, group_height,
                stage.get("name", f"Stage {i+1}"),
                stage.get("color", "light_gray")
            )

            # 垂直均匀分布模块
            if n_modules == 1:
                y_positions = [50]
            else:
                y_start = 50 + (n_modules - 1) * 7
                y_positions = [y_start - j * 14 for j in range(n_modules)]

            for j, mod in enumerate(modules):
                pos = self.draw_module(
                    sx, y_positions[j], 16, 8,
                    mod.get("name", ""),
                    mod.get("type", "default"),
                    mod.get("fontsize", 8),
                    mod.get("fontweight", "medium"),
                    mod.get("icon")
                )
                module_positions[mod.get("name", f"mod_{i}_{j}")] = pos

        # 绘制连接
        for conn in architecture.get("connections", []):
            from_name = conn.get("from")
            to_name = conn.get("to")
            if from_name in module_positions and to_name in module_positions:
                p1 = module_positions[from_name]
                p2 = module_positions[to_name]
                # 自动判断连接方向
                if p1["cx"] < p2["cx"]:
                    x1, y1 = p1["x2"], p1["cy"]
                    x2, y2 = p2["x1"], p2["cy"]
                elif p1["cx"] > p2["cx"]:
                    x1, y1 = p1["x1"], p1["cy"]
                    x2, y2 = p2["x2"], p2["cy"]
                else:
                    x1, y1 = p1["cx"], p1["y1"]
                    x2, y2 = p2["cx"], p2["y2"]

                self.draw_arrow(
                    x1, y1, x2, y2,
                    conn.get("style", "->"),
                    conn.get("color"),
                    conn.get("linewidth", 1.2),
                    conn.get("linestyle", "-")
                )

    def _render_encoder_decoder(self, architecture: Dict[str, Any]):
        """渲染编码器-解码器布局 (简化版，使用水平流水线近似)"""
        # 先用水平流水线实现基础版本
        self._render_horizontal_pipeline(architecture)

    def _render_multi_branch(self, architecture: Dict[str, Any]):
        """渲染多分支布局 (简化版，使用水平流水线近似)"""
        # 先用水平流水线实现基础版本
        self._render_horizontal_pipeline(architecture)


def render_diagram_from_architecture(architecture: Dict[str, Any], output_path: str,
                                     figsize: Tuple[int, int] = (14, 10), dpi: int = 300) -> str:
    """
    便捷函数：根据架构数据渲染流程图

    Args:
        architecture: 结构化架构数据
        output_path: 输出文件路径 (.png 或 .svg)
        figsize: 画布尺寸
        dpi: 分辨率

    Returns:
        输出文件路径
    """
    renderer = ConferenceDiagramRenderer(figsize=figsize, dpi=dpi)
    return renderer.render(architecture, output_path)
