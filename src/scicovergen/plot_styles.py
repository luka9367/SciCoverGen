"""
顶会论文图表风格配置库

提取自 plot-from-data / plot-from-image 的 8 种预建风格，
覆盖柱状图、折线图、散点图、雷达图四大类。
"""

from typing import Dict, Any

# ── 8 种预建风格全局参数 ──────────────────────────────────

STYLE_CONFIGS: Dict[str, Dict[str, Any]] = {
    "bar_paired_delta": {
        "type": "bar",
        "description": "配对对比柱 + 增益箭头（baseline vs method）",
        "colors": {
            "baseline": "#A8C8E8",
            "method": "#1B3D6E",
            "delta": "#CC2200",
        },
        "params": {
            "bar_width": 0.28,
            "gap": 0.01,
            "spine_linewidth": 1.5,
            "grid": False,
            "font_family": "serif",
            "font_serif": ["STIXGeneral", "DejaVu Serif", "Times New Roman"],
            "mathtext_fontset": "stix",
        },
        "required_data": ["groups", "baseline", "method", "delta"],
        "optional_data": ["title", "ylabel", "ylim"],
    },

    "bar_grouped_hatch": {
        "type": "bar",
        "description": "多方法分组柱 + 斜线填充主方法 + 柱顶数值",
        "colors": {
            "primary": "#5B9BD5",
            "secondary": ["#ED7D31", "#A5A5A5", "#FFC000", "#70AD47"],
            "hatch": "///",
        },
        "params": {
            "bar_width": 0.15,
            "group_gap": 0.25,
            "spine_linewidth": 1.0,
            "grid": False,
            "font_family": "sans-serif",
            "font_sans_serif": ["DejaVu Sans", "Arial"],
            "show_values": True,
        },
        "required_data": ["groups", "series_names", "values"],
        "optional_data": ["title", "ylabel", "ylim", "highlight_index"],
    },

    "line_confidence_band": {
        "type": "line",
        "description": "折线 + 半透明置信区间阴影",
        "colors": {
            "primary": "#3A8B3A",
            "secondary": "#3B6BB5",
            "baseline": "#999999",
        },
        "params": {
            "lw_primary": 1.8,
            "lw_secondary": 1.8,
            "lw_baseline": 1.4,
            "fill_alpha": 0.15,
            "marker_size": 6,
            "spine_visible": ["left", "bottom"],
            "grid": False,
            "font_family": "serif",
            "font_serif": ["Computer Modern Roman", "STIX Two Text", "DejaVu Serif"],
            "usetex": True,
            "legend_frame": False,
        },
        "required_data": ["x", "series"],
        "optional_data": ["title", "xlabel", "ylabel", "reference_y", "legend_loc"],
    },

    "line_training_curve": {
        "type": "line",
        "description": "训练曲线 + 垂直断点线 + 水平参考线",
        "colors": {
            "primary": "#D62728",
            "secondary": "#1F77B4",
            "cutline": "#888888",
            "reference": "#AAAAAA",
        },
        "params": {
            "lw_primary": 2.0,
            "lw_cut": 1.0,
            "lw_ref": 1.0,
            "cut_style": "--",
            "ref_style": "--",
            "spine_visible": ["left", "bottom"],
            "grid": False,
            "font_family": "sans-serif",
            "font_sans_serif": ["DejaVu Sans", "Arial"],
            "usetex": False,
        },
        "required_data": ["x", "series"],
        "optional_data": ["title", "xlabel", "ylabel", "cut_x", "reference_y"],
    },

    "line_loss_with_inset": {
        "type": "line",
        "description": "L 形 spine + 局部放大 inset",
        "colors": {
            "train": "#1F77B4",
            "val": "#FF7F0E",
            "zoom_box": "#666666",
        },
        "params": {
            "lw_train": 1.5,
            "lw_val": 1.5,
            "zoom_box_style": "--",
            "spine_visible": ["left", "bottom"],
            "grid": True,
            "grid_color": "#E8E8E8",
            "grid_linewidth": 0.6,
            "grid_linestyle": "--",
            "font_family": "serif",
            "font_serif": ["STIXGeneral", "DejaVu Serif"],
            "usetex": True,
        },
        "required_data": ["x", "train", "val"],
        "optional_data": ["title", "xlabel", "ylabel", "zoom_xlim", "zoom_ylim", "inset_pos"],
    },

    "scatter_tsne_cluster": {
        "type": "scatter",
        "description": "t-SNE 聚类 + 注释框 + 点线网格",
        "colors": {
            "clusters": ["#6A4C93", "#D651A0", "#F06292", "#FF8A65",
                         "#FFB74D", "#FFF176", "#C888E8"],
            "bbox_edge": "#2C3E50",
        },
        "params": {
            "point_size": 14,
            "point_alpha": 0.55,
            "bbox_alpha": 0.28,
            "bbox_pad": 0.30,
            "bbox_linewidth": 0.9,
            "spine_linewidth": 0.9,
            "spine_color": "#333333",
            "grid": True,
            "grid_color": "#E0E0E0",
            "grid_linewidth": 0.6,
            "grid_linestyle": ":",
            "tick_direction": "in",
            "tick_length": 4,
            "font_family": "serif",
            "font_serif": ["Computer Modern Roman", "STIX Two Text", "DejaVu Serif"],
            "usetex": True,
            "legend_frame": True,
            "legend_edgecolor": "#CCCCCC",
        },
        "required_data": ["points", "labels"],
        "optional_data": ["title", "xlabel", "ylabel", "annotations"],
    },

    "scatter_broken_axis": {
        "type": "scatter",
        "description": "折断 X 轴 + 多 marker 系列",
        "colors": {
            "series": ["#1F77B4", "#FF7F0E", "#2CA02C", "#D62728"],
            "markers": ["o", "s", "D", "^"],
        },
        "params": {
            "point_size": 25,
            "point_alpha": 0.7,
            "spine_linewidth": 1.0,
            "grid": False,
            "font_family": "sans-serif",
            "font_sans_serif": ["DejaVu Sans", "Arial"],
            "break_gap": 0.05,
            "break_symbol": "//",
        },
        "required_data": ["x", "y", "series"],
        "optional_data": ["title", "xlabel", "ylabel", "break_ranges"],
    },

    "radar_dual_series": {
        "type": "radar",
        "description": "双方法多维对比 + 正八边形网格 + 值标注",
        "colors": {
            "series_a": "#5A8A5A",
            "series_b": "#4169E1",
            "grid": "#CCCCCC",
        },
        "params": {
            "fill_alpha": 0.20,
            "line_width": 1.8,
            "grid_linewidth": 0.8,
            "grid_linestyle": "--",
            "label_radius": 1.12,
            "value_label_offset": 0.08,
            "font_family": "serif",
            "font_serif": ["STIXGeneral", "DejaVu Serif"],
            "usetex": True,
        },
        "required_data": ["categories", "series_a", "series_b"],
        "optional_data": ["title", "labels"],
    },
}


def list_styles() -> list:
    """列出所有可用风格"""
    return list(STYLE_CONFIGS.keys())


def get_style_config(style_name: str) -> Dict[str, Any]:
    """获取指定风格的完整配置"""
    if style_name not in STYLE_CONFIGS:
        raise ValueError(
            f"未知风格 '{style_name}'。可用风格: {', '.join(list_styles())}"
        )
    return STYLE_CONFIGS[style_name]


def validate_data(data: Dict[str, Any], style_name: str) -> bool:
    """验证数据是否包含风格所需的必要字段"""
    config = get_style_config(style_name)
    required = config.get("required_data", [])
    missing = [k for k in required if k not in data]
    if missing:
        raise ValueError(
            f"风格 '{style_name}' 缺少必要数据字段: {missing}"
        )
    return True
