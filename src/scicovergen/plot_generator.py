"""
数据转绘图引擎 (Plot Generator)

深度融合 plot-from-data 能力：
用户提供数据 + 选择顶会风格 -> 自动生成 300dpi  publication-quality 图表。

支持 8 种预建风格：
- bar_paired_delta:    配对对比柱 + 增益箭头
- bar_grouped_hatch:   多方法分组柱 + 斜线填充
- line_confidence_band: 折线 + 置信区间阴影
- line_training_curve:  训练曲线 + 垂直断点线
- line_loss_with_inset: L 形 spine + 局部放大 inset
- scatter_tsne_cluster: t-SNE 聚类 + 注释框
- scatter_broken_axis:  折断 X 轴 + 多 marker
- radar_dual_series:    双方法雷达对比
"""

import os
import json
import shutil
import warnings
from typing import Dict, Any, List, Optional, Tuple

import numpy as np
import matplotlib
matplotlib.use("Agg")  # 无头环境
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch

from .plot_styles import get_style_config, validate_data


def _usetex_available() -> bool:
    """检查系统是否可用 LaTeX（用于 text.usetex）"""
    return shutil.which("latex") is not None


def _apply_rc(params: Dict[str, Any]):
    """安全应用 matplotlib rcParams，LaTeX 不可用时自动降级"""
    rc = {}
    if params.get("usetex") and not _usetex_available():
        # 降级：关闭 usetex，使用 mathtext 替代
        rc["text.usetex"] = False
        rc["mathtext.fontset"] = params.get("mathtext_fontset", "stix")
    else:
        rc["text.usetex"] = params.get("usetex", False)
        if rc["text.usetex"]:
            rc["font.family"] = params.get("font_family", "serif")
            if "font_serif" in params:
                rc["font.serif"] = params["font_serif"]
            if "font_sans_serif" in params:
                rc["font.sans-serif"] = params["font_sans_serif"]

    for key in ("font.family", "font.serif", "font.sans-serif",
                "axes.unicode_minus", "mathtext.fontset"):
        if key in params:
            rc[key] = params[key]

    if rc:
        plt.rcParams.update(rc)


class PlotGenerator:
    """
    学术论文图表生成器

    Usage:
        gen = PlotGenerator()
        gen.generate(data_dict, "bar_paired_delta", "output.png")
    """

    DPI = 300

    def generate(
        self,
        data: Dict[str, Any],
        style: str,
        output_path: str,
        figsize: Optional[Tuple[float, float]] = None,
    ) -> str:
        """
        根据数据和风格生成图表

        Args:
            data: 数据字典，具体内容取决于风格
            style: 风格名称（8种预建风格之一）
            output_path: 输出 PNG 路径
            figsize: 可选的 (宽, 高) 英寸元组

        Returns:
            输出文件路径
        """
        validate_data(data, style)
        config = get_style_config(style)

        # 确保输出目录存在
        out_dir = os.path.dirname(output_path) or "."
        os.makedirs(out_dir, exist_ok=True)

        renderer = getattr(self, f"_render_{style}")
        renderer(data, config, output_path, figsize)
        return output_path

    # ──────────────────────────────────────────────
    # 风格 1: bar_paired_delta
    # ──────────────────────────────────────────────
    def _render_bar_paired_delta(
        self,
        data: Dict[str, Any],
        config: Dict[str, Any],
        output_path: str,
        figsize: Optional[Tuple[float, float]] = None,
    ):
        """配对对比柱 + 增益箭头"""
        colors = config["colors"]
        params = config["params"]

        _apply_rc(params)

        panels = data.get("panels", [data])
        n_panels = len(panels)
        figsize = figsize or (5 * n_panels, 4.5)

        fig, axes = plt.subplots(1, n_panels, figsize=figsize, sharey=False)
        if n_panels == 1:
            axes = [axes]
        fig.subplots_adjust(wspace=0.35)

        BAR_W = params["bar_width"]
        GAP = params["gap"]
        ARROW_KW = dict(arrowstyle="->", color="black", lw=1.2)

        for ax, panel in zip(axes, panels):
            groups = panel["groups"]
            baseline = np.array(panel["baseline"])
            method = np.array(panel["method"])
            delta = panel.get("delta", [])
            n = len(groups)
            x = np.arange(n)

            bars_b = ax.bar(
                x - (BAR_W + GAP) / 2, baseline, width=BAR_W,
                color=colors["baseline"], zorder=3
            )
            bars_m = ax.bar(
                x + (BAR_W + GAP) / 2, method, width=BAR_W,
                color=colors["method"], zorder=3
            )

            for i, (bl, me) in enumerate(zip(baseline, method)):
                ax.plot(
                    [x[i] - BAR_W, x[i] + BAR_W + GAP / 2],
                    [bl, bl], color="black", lw=0.9, ls="--", zorder=4
                )
                ax.annotate(
                    "", xy=(x[i] + (BAR_W + GAP) / 2, me - 0.3),
                    xytext=(x[i] + (BAR_W + GAP) / 2, bl + 0.3),
                    arrowprops=ARROW_KW, zorder=5
                )
                if i < len(delta):
                    ax.text(
                        x[i] + (BAR_W + GAP) / 2, me + 0.6,
                        delta[i], color=colors["delta"],
                        ha="center", va="bottom", fontsize=9.5, fontweight="bold"
                    )

            ax.set_xticks(x)
            ax.set_xticklabels(groups, fontsize=10.5, fontweight="bold")
            ax.set_ylabel(
                panel.get("ylabel", data.get("ylabel", "")),
                fontsize=10.5, fontweight="bold"
            )
            if "ylim" in panel:
                ax.set_ylim(*panel["ylim"])
            elif "ylim" in data:
                ax.set_ylim(*data["ylim"])

            for spine in ax.spines.values():
                spine.set_linewidth(params["spine_linewidth"])
                spine.set_color("black")
            ax.tick_params(length=0)
            ax.set_axisbelow(True)

            title = panel.get("title", data.get("title", ""))
            if title:
                ax.text(
                    0.04, 0.97, title, transform=ax.transAxes,
                    fontsize=12, fontweight="bold", va="top", ha="left",
                    color="#003F6C", fontfamily="serif"
                )

        fig.savefig(output_path, dpi=self.DPI, bbox_inches="tight", facecolor="white")
        plt.close(fig)

    # ──────────────────────────────────────────────
    # 风格 2: bar_grouped_hatch
    # ──────────────────────────────────────────────
    def _render_bar_grouped_hatch(
        self,
        data: Dict[str, Any],
        config: Dict[str, Any],
        output_path: str,
        figsize: Optional[Tuple[float, float]] = None,
    ):
        """多方法分组柱 + 斜线填充"""
        colors = config["colors"]
        params = config["params"]

        _apply_rc(params)

        groups = data["groups"]
        series_names = data["series_names"]
        values = np.array(data["values"])  # shape: (n_groups, n_series)
        highlight = data.get("highlight_index", 0)

        n_groups, n_series = values.shape
        x = np.arange(n_groups)
        bar_w = params["bar_width"]
        group_gap = params["group_gap"]

        figsize = figsize or (max(6, n_groups * 1.2), 4.5)
        fig, ax = plt.subplots(figsize=figsize)

        sec_colors = colors["secondary"]
        for i in range(n_series):
            offset = (i - n_series / 2 + 0.5) * (bar_w + 0.02)
            color = colors["primary"] if i == highlight else sec_colors[(i - 1) % len(sec_colors)]
            hatch = colors["hatch"] if i == highlight else None
            bars = ax.bar(
                x + offset, values[:, i], width=bar_w,
                color=color, hatch=hatch, edgecolor="black" if hatch else "none",
                label=series_names[i], zorder=3
            )
            if params.get("show_values"):
                for bar, val in zip(bars, values[:, i]):
                    ax.text(
                        bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.01 * values.max(),
                        f"{val:.1f}", ha="center", va="bottom", fontsize=8
                    )

        ax.set_xticks(x)
        ax.set_xticklabels(groups, fontsize=10)
        ax.set_ylabel(data.get("ylabel", ""), fontsize=10)
        if "title" in data:
            ax.set_title(data["title"], fontsize=12, fontweight="bold")

        for side, sp in ax.spines.items():
            sp.set_visible(side in ("left", "bottom"))
            sp.set_linewidth(params["spine_linewidth"])
        ax.tick_params(direction="out", length=4)
        ax.legend(frameon=True, fontsize=9)

        fig.savefig(output_path, dpi=self.DPI, bbox_inches="tight", facecolor="white")
        plt.close(fig)

    # ──────────────────────────────────────────────
    # 风格 3: line_confidence_band
    # ──────────────────────────────────────────────
    def _render_line_confidence_band(
        self,
        data: Dict[str, Any],
        config: Dict[str, Any],
        output_path: str,
        figsize: Optional[Tuple[float, float]] = None,
    ):
        """折线 + 半透明置信区间阴影"""
        colors = config["colors"]
        params = config["params"]

        _apply_rc(params)

        x = np.array(data["x"])
        series_list = data["series"]  # list of dicts: {name, mean, std, is_primary}

        figsize = figsize or (6.5, 4.5)
        fig, ax = plt.subplots(figsize=figsize)

        for s in series_list:
            mean = np.array(s["mean"])
            std = np.array(s.get("std", np.zeros_like(mean)))
            color = colors["primary"] if s.get("is_primary") else colors["secondary"]
            lw = params["lw_primary"] if s.get("is_primary") else params["lw_secondary"]
            label = s["name"]

            ax.fill_between(
                x, mean - std, mean + std,
                color=color, alpha=params["fill_alpha"], zorder=1
            )
            ax.plot(x, mean, color=color, lw=lw, label=label, zorder=3)

        ref_y = data.get("reference_y")
        if ref_y is not None:
            ax.axhline(ref_y, color=colors["baseline"], ls="--", lw=1.0, zorder=2)

        ax.set_xlabel(data.get("xlabel", ""), fontsize=11)
        ax.set_ylabel(data.get("ylabel", ""), fontsize=11)
        if "title" in data:
            ax.set_title(data["title"], fontsize=12)

        for side, sp in ax.spines.items():
            sp.set_visible(side in params["spine_visible"])
            sp.set_linewidth(0.9)

        leg = ax.legend(
            loc=data.get("legend_loc", "best"),
            framealpha=0, edgecolor="none", fontsize=9.5
        )
        for text in leg.get_texts():
            if any(s.get("is_primary") and s["name"] in text.get_text() for s in series_list):
                text.set_fontweight("bold")

        fig.savefig(output_path, dpi=self.DPI, bbox_inches="tight", facecolor="white")
        plt.close(fig)

    # ──────────────────────────────────────────────
    # 风格 4: line_training_curve
    # ──────────────────────────────────────────────
    def _render_line_training_curve(
        self,
        data: Dict[str, Any],
        config: Dict[str, Any],
        output_path: str,
        figsize: Optional[Tuple[float, float]] = None,
    ):
        """训练曲线 + 垂直断点线 + 水平参考线"""
        colors = config["colors"]
        params = config["params"]

        _apply_rc(params)

        x = np.array(data["x"])
        series_list = data["series"]
        cut_x = data.get("cut_x")

        figsize = figsize or (7, 4.5)
        fig, ax = plt.subplots(figsize=figsize)

        for s in series_list:
            y = np.array(s["y"])
            color = colors["primary"] if s.get("is_primary") else colors["secondary"]
            lw = params["lw_primary"] if s.get("is_primary") else params["lw_secondary"]
            ax.plot(x, y, color=color, lw=lw, label=s["name"], zorder=3)

        if cut_x is not None:
            for cx in cut_x if isinstance(cut_x, list) else [cut_x]:
                ax.axvline(cx, color=colors["cutline"], ls=params["cut_style"],
                           lw=params["lw_cut"], zorder=2)

        ref_y = data.get("reference_y")
        if ref_y is not None:
            ax.axhline(ref_y, color=colors["reference"], ls=params["ref_style"],
                       lw=params["lw_ref"], zorder=2)

        ax.set_xlabel(data.get("xlabel", ""), fontsize=11)
        ax.set_ylabel(data.get("ylabel", ""), fontsize=11)
        if "title" in data:
            ax.set_title(data["title"], fontsize=12, fontweight="bold")

        for side, sp in ax.spines.items():
            sp.set_visible(side in params["spine_visible"])
        ax.tick_params(direction="out", length=4)
        ax.legend(frameon=False, fontsize=9)

        fig.savefig(output_path, dpi=self.DPI, bbox_inches="tight", facecolor="white")
        plt.close(fig)

    # ──────────────────────────────────────────────
    # 风格 5: line_loss_with_inset
    # ──────────────────────────────────────────────
    def _render_line_loss_with_inset(
        self,
        data: Dict[str, Any],
        config: Dict[str, Any],
        output_path: str,
        figsize: Optional[Tuple[float, float]] = None,
    ):
        """L 形 spine + 局部放大 inset"""
        colors = config["colors"]
        params = config["params"]

        _apply_rc(params)

        x = np.array(data["x"])
        train = np.array(data["train"])
        val = np.array(data["val"])

        figsize = figsize or (7, 4.5)
        fig, ax = plt.subplots(figsize=figsize)

        ax.plot(x, train, color=colors["train"], lw=params["lw_train"], label="Train", zorder=3)
        ax.plot(x, val, color=colors["val"], lw=params["lw_val"], label="Val", zorder=3)

        ax.set_xlabel(data.get("xlabel", "Epoch"), fontsize=11)
        ax.set_ylabel(data.get("ylabel", "Loss"), fontsize=11)
        if "title" in data:
            ax.set_title(data["title"], fontsize=12)

        for side, sp in ax.spines.items():
            sp.set_visible(side in params["spine_visible"])
        ax.grid(params["grid"], color=params["grid_color"],
                linewidth=params["grid_linewidth"], linestyle=params["grid_linestyle"])
        ax.set_axisbelow(True)
        ax.legend(frameon=False, fontsize=9)

        # Inset
        zoom_xlim = data.get("zoom_xlim")
        zoom_ylim = data.get("zoom_ylim")
        inset_pos = data.get("inset_pos", [0.55, 0.55, 0.35, 0.35])
        if zoom_xlim and zoom_ylim:
            ax_inset = fig.add_axes(inset_pos)
            ax_inset.plot(x, train, color=colors["train"], lw=1.2)
            ax_inset.plot(x, val, color=colors["val"], lw=1.2)
            ax_inset.set_xlim(*zoom_xlim)
            ax_inset.set_ylim(*zoom_ylim)
            ax_inset.tick_params(labelsize=7)
            for side, sp in ax_inset.spines.items():
                sp.set_visible(side in params["spine_visible"])

            # Zoom box indicator
            from matplotlib.patches import Rectangle
            rect = Rectangle(
                (zoom_xlim[0], zoom_ylim[0]),
                zoom_xlim[1] - zoom_xlim[0],
                zoom_ylim[1] - zoom_ylim[0],
                linewidth=1.2, edgecolor=colors["zoom_box"],
                facecolor="none", linestyle=params["zoom_box_style"], zorder=4
            )
            ax.add_patch(rect)

        fig.savefig(output_path, dpi=self.DPI, bbox_inches="tight", facecolor="white")
        plt.close(fig)

    # ──────────────────────────────────────────────
    # 风格 6: scatter_tsne_cluster
    # ──────────────────────────────────────────────
    def _render_scatter_tsne_cluster(
        self,
        data: Dict[str, Any],
        config: Dict[str, Any],
        output_path: str,
        figsize: Optional[Tuple[float, float]] = None,
    ):
        """t-SNE 聚类 + 注释框"""
        colors = config["colors"]
        params = config["params"]

        _apply_rc(params)

        points = data["points"]  # dict: {label: [(x,y), ...]}
        labels = data["labels"]  # list of label names
        palette = colors["clusters"]
        color_map = {lab: palette[i % len(palette)] for i, lab in enumerate(labels)}

        figsize = figsize or (7.5, 6.2)
        fig, ax = plt.subplots(figsize=figsize)

        for lab in labels:
            pts = np.array(points[lab])
            ax.scatter(
                pts[:, 0], pts[:, 1],
                c=color_map[lab], s=params["point_size"],
                alpha=params["point_alpha"], linewidths=0,
                rasterized=True, label=lab, zorder=2
            )

        annotations = data.get("annotations", [])
        for ann in annotations:
            lab = ann["name"]
            color = color_map[lab]
            import matplotlib.colors as mcolors
            rgba = list(mcolors.to_rgba(color))
            rgba[3] = params["bbox_alpha"]
            ax.annotate(
                ann.get("text", lab),
                xy=ann.get("xy", (0, 0)),
                xytext=ann.get("xytext", ann.get("xy", (0, 0))),
                fontsize=ann.get("fontsize", 10.0),
                bbox=dict(
                    boxstyle=f"round,pad={params['bbox_pad']}",
                    facecolor=tuple(rgba),
                    edgecolor=colors["bbox_edge"],
                    linewidth=params["bbox_linewidth"],
                ),
                ha="center", va="center", zorder=5,
            )

        ax.set_xlabel(data.get("xlabel", "t-SNE Component 1"), fontsize=12)
        ax.set_ylabel(data.get("ylabel", "t-SNE Component 2"), fontsize=12)
        if "title" in data:
            ax.set_title(data["title"], fontsize=13.5, pad=8, linespacing=1.4)

        for sp in ax.spines.values():
            sp.set_visible(True)
            sp.set_linewidth(params["spine_linewidth"])
            sp.set_color(params["spine_color"])

        ax.tick_params(
            direction=params["tick_direction"], length=params["tick_length"],
            width=0.8, labelsize=10, color=params["spine_color"]
        )
        ax.grid(
            params["grid"], color=params["grid_color"],
            linewidth=params["grid_linewidth"], linestyle=params["grid_linestyle"], zorder=0
        )
        ax.set_axisbelow(True)

        if params.get("legend_frame"):
            ax.legend(
                loc="upper right", fontsize=9.5, frameon=True,
                facecolor="white", edgecolor=params.get("legend_edgecolor", "#CCCCCC"),
                framealpha=1.0, markerscale=1.0, handlelength=0.8, handleheight=0.8
            )
        else:
            ax.legend(loc="best", frameon=False)

        fig.savefig(output_path, dpi=self.DPI, bbox_inches="tight", facecolor="white")
        plt.close(fig)

    # ──────────────────────────────────────────────
    # 风格 7: scatter_broken_axis
    # ──────────────────────────────────────────────
    def _render_scatter_broken_axis(
        self,
        data: Dict[str, Any],
        config: Dict[str, Any],
        output_path: str,
        figsize: Optional[Tuple[float, float]] = None,
    ):
        """折断 X 轴 + 多 marker 系列"""
        colors = config["colors"]
        params = config["params"]

        _apply_rc(params)

        x = np.array(data["x"])
        y = np.array(data["y"])
        series_idx = np.array(data["series"])
        break_ranges = data.get("break_ranges", [])

        figsize = figsize or (8, 4.5)
        fig, axes = plt.subplots(1, len(break_ranges), figsize=figsize,
                                  sharey=True)
        if len(break_ranges) == 1:
            axes = [axes]
        fig.subplots_adjust(wspace=params["break_gap"])

        palette = colors["series"]
        markers = colors["markers"]

        for ax, (xmin, xmax) in zip(axes, break_ranges):
            mask = (x >= xmin) & (x <= xmax)
            for s_id in np.unique(series_idx):
                smask = mask & (series_idx == s_id)
                ax.scatter(
                    x[smask], y[smask],
                    c=palette[s_id % len(palette)],
                    marker=markers[s_id % len(markers)],
                    s=params["point_size"], alpha=params["point_alpha"],
                    label=f"Series {s_id}" if ax == axes[0] else "", zorder=3
                )
            ax.set_xlim(xmin, xmax)
            for sp in ax.spines.values():
                sp.set_linewidth(params["spine_linewidth"])

        # Break symbols
        for ax in axes[:-1]:
            ax.spines["right"].set_visible(False)
        for ax in axes[1:]:
            ax.spines["left"].set_visible(False)
            ax.tick_params(left=False)

        axes[0].set_ylabel(data.get("ylabel", ""), fontsize=11)
        fig.text(0.5, 0.02, data.get("xlabel", ""), ha="center", fontsize=11)
        if "title" in data:
            fig.suptitle(data["title"], fontsize=12, fontweight="bold", y=0.98)

        axes[0].legend(frameon=False, fontsize=9)
        fig.savefig(output_path, dpi=self.DPI, bbox_inches="tight", facecolor="white")
        plt.close(fig)

    # ──────────────────────────────────────────────
    # 风格 8: radar_dual_series
    # ──────────────────────────────────────────────
    def _render_radar_dual_series(
        self,
        data: Dict[str, Any],
        config: Dict[str, Any],
        output_path: str,
        figsize: Optional[Tuple[float, float]] = None,
    ):
        """双方法雷达对比 + 正八边形网格"""
        colors = config["colors"]
        params = config["params"]

        _apply_rc(params)

        categories = data["categories"]
        series_a = np.array(data["series_a"])
        series_b = np.array(data["series_b"])
        labels = data.get("labels", ["Method A", "Method B"])

        N = len(categories)
        angles = np.linspace(0, 2 * np.pi, N, endpoint=False).tolist()
        angles += angles[:1]
        series_a = np.concatenate([series_a, [series_a[0]]])
        series_b = np.concatenate([series_b, [series_b[0]]])

        figsize = figsize or (6.5, 6)
        fig, ax = plt.subplots(figsize=figsize, subplot_kw=dict(polar=True))

        ax.fill(angles, series_a, color=colors["series_a"], alpha=params["fill_alpha"])
        ax.plot(angles, series_a, color=colors["series_a"], lw=params["line_width"], label=labels[0])

        ax.fill(angles, series_b, color=colors["series_b"], alpha=params["fill_alpha"])
        ax.plot(angles, series_b, color=colors["series_b"], lw=params["line_width"], label=labels[1])

        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(categories, fontsize=10)

        for spine in ax.spines.values():
            spine.set_linewidth(params["grid_linewidth"])
            spine.set_linestyle(params["grid_linestyle"])
            spine.set_color(params["grid"])

        ax.set_rlabel_position(30)
        ax.tick_params(pad=8)

        if "title" in data:
            ax.set_title(data["title"], fontsize=12, pad=20)

        ax.legend(loc="upper right", bbox_to_anchor=(1.15, 1.1), frameon=False)

        fig.savefig(output_path, dpi=self.DPI, bbox_inches="tight", facecolor="white")
        plt.close(fig)
