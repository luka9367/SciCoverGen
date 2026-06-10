<div align="center">

# SciCoverGen

**面向 CS & AI 科研工作者的图像生成与复现引擎**

[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey.svg)]()

[English](#english) | [中文](#中文)

</div>

---

## 中文

### 简介

SciCoverGen 融合国内免费大模型能力，参考上海交通大学、中国科学院大学、香港中文大学（深圳）、上海 AI Lab、香港科技大学（广州）等顶级学府与研究机构的先进经验，专为 **CS & AI 方向学生与科研工作者** 提供 **高效、专业、一站式** 图片复现与生图解决方案。

从论文概念配图、算法流程图到实验数据图表、图像风格复现，四大生成模式全覆盖，零成本产出可直接用于 CCF-A 顶级论文的高质量图像。我们将 NeurIPS、ICML、ICLR 等顶会的视觉规范工程化，打造开源国内免费模型赛道内实力顶尖的科研图像生成工具。

### 核心特性

- **四大生成模式**：
  - `image` — 文生图（Cogview-3-Flash），LLM 动态生成 Prompt，支持顶会风格概念配图
  - `diagram` — 代码精确绘图（Matplotlib），生成带可读文字的 300dpi 矢量流程图
  - `data_plot` — 数据转绘图（8 种顶会预建风格），JSON 数据一键生成 publication-quality 图表
  - `image_repro` — 图像复现（plot-from-image），上传参考图自动分析并 matplotlib 还原
- **顶会视觉规范**：配色、字体、spine、网格全部按 NeurIPS / ICML / ICLR 标准调优
- **国产免费链路**：对接智谱 Cogview-3-Flash 与 GLM-4-Flash，数据不出境，零费用
- **多格式输入**：支持 Markdown、TXT、PDF 论文、JSON 数据、参考图像
- **Python API + CLI 双接口**：一行代码或一条命令即可生成

### 快速开始

#### 1. 安装

```bash
pip install scicovergen
```

> PDF 支持需额外安装（可选）：`pip install pdfplumber`

#### 2. 获取免费 API Key

1. 访问 [智谱开放平台](https://open.bigmodel.cn/)
2. 注册账号（**新用户免费领取额度**）
3. 创建 API Key

#### 3. 生成图像

**命令行（CLI）**

```bash
export ZHIPU_API_KEY=your-api-key

# 模式 1: 文生图 — 论文概念配图
scicovergen paper.md --mode image --style conference_diagram

# 模式 2: 代码精确绘图 — 算法流程图
scicovergen paper.md --mode diagram

# 模式 3: 数据转绘图 — 实验图表
scicovergen data.json --mode data_plot --plot-style bar_paired_delta

# 模式 4: 图像复现 — 还原参考配图风格
scicovergen reference.png --mode image_repro
```

**Python API**

```python
from scicovergen import SciCoverGen

# 统一入口
gen = SciCoverGen(api_key="your-api-key")

# 文生图
gen.generate("paper.md", mode="image", style="conference_diagram")

# 精确流程图
gen.generate("paper.md", mode="diagram")

# 数据绘图（传入数据字典）
data = {
    "title": "Accuracy Comparison",
    "groups": ["A", "B", "C"],
    "baseline": [50, 60, 55],
    "method": [70, 75, 80],
    "delta": ["+20", "+15", "+25"],
    "ylabel": "Accuracy (%)"
}
gen.generate(data, mode="data_plot", style="bar_paired_delta")

# 图像复现
gen.generate("reference.png", mode="image_repro")
```

### 四大生成模式详解

| 模式 | 命令 | 说明 | 输出特点 |
|------|------|------|----------|
| **文生图** | `--mode image` | Cogview-3-Flash 生成概念配图 | 创意丰富，适合封面/海报 |
| **精确流程图** | `--mode diagram` | Matplotlib 渲染算法架构图 | 文字清晰，300dpi，直接投稿 |
| **数据转绘图** | `--mode data_plot` | 8 种顶会风格图表 | 配色规范，数据驱动 |
| **图像复现** | `--mode image_repro` | 分析参考图并 matplotlib 还原 | 风格迁移，可编辑复现 |

### 8 种顶会预建图表风格

- `bar_paired_delta` — 配对对比柱 + 增益箭头
- `bar_grouped_hatch` — 多方法分组柱 + 斜线填充
- `line_confidence_band` — 折线 + 半透明置信区间阴影
- `line_training_curve` — 训练曲线 + 垂直断点线
- `line_loss_with_inset` — L 形 spine + 局部放大 inset
- `scatter_tsne_cluster` — t-SNE 聚类 + 注释框
- `scatter_broken_axis` — 折断 X 轴 + 多 marker 系列
- `radar_dual_series` — 双方法雷达对比 + 正八边形网格

### 项目结构

```
SciCoverGen/
├── src/scicovergen/          # 核心源码
│   ├── __init__.py
│   ├── api_client.py         # 智谱 API 客户端
│   ├── analyzer.py           # 内容智能分析器 + 架构提取
│   ├── prompts.py            # 场景化 Prompt 生成器（LLM 增强）
│   ├── generator.py          # 主生成器（支持 4 种模式）
│   ├── diagram_renderer.py   # Matplotlib 矢量流程图渲染器
│   ├── plot_generator.py     # 数据转绘图引擎（8 种风格）
│   ├── plot_reproducer.py    # 图像复现引擎（plot-from-image）
│   ├── plot_styles.py        # 顶会图表风格配置库
│   ├── config.py             # 配置管理
│   ├── cli.py                # 命令行接口（支持 4 种模式）
│   └── utils.py              # 工具函数
├── examples/                  # 示例代码
│   ├── paper_cover/
│   ├── project_report/
│   └── academic_poster/
├── tests/                     # 单元测试
├── docs/                      # 文档
│   ├── index.html             # 项目宣传页
│   ├── getting_started.md
│   └── api_reference.md
├── .github/workflows/         # CI/CD
├── setup.py
├── requirements.txt
├── LICENSE
└── README.md
```

### 技术架构

```
用户输入 (论文/报告/海报/数据/图像)
    ↓
内容读取 (支持 MD/TXT/PDF/JSON/PNG)
    ↓
模式路由 (image / diagram / data_plot / image_repro)
    ↓
├─ image:   GLM-4-Flash 分析 → Prompt 构建 → Cogview-3-Flash 生图
├─ diagram: GLM-4-Flash 架构提取 → Matplotlib 精确渲染 → 300dpi PNG
├─ data_plot: 数据验证 → 风格匹配 → PlotGenerator 渲染 → 300dpi PNG
└─ image_repro: PIL 图像分析 → 风格匹配/LLM 代码生成 → Matplotlib 复现
```

### 学术背景

本项目深度参考以下顶尖学府与研究机构的先进经验：

- **上海交通大学** (SJTU)
- **中国科学院大学** (UCAS)
- **香港中文大学（深圳）** (CUHK-Shenzhen)
- **上海人工智能实验室** (Shanghai AI Lab)
- **香港科技大学（广州）** (HKUST(GZ))

我们将学术界在 NeurIPS、ICML、ICLR 等顶会中沉淀的视觉设计方法论融入工程实践，从配色体系、字体规范到布局美学，全部按投稿标准调优。

### 贡献

欢迎提交 Issue 和 Pull Request！

### 许可证

[MIT](LICENSE)

---

## English

### Introduction

SciCoverGen is an all-in-one image generation and reproduction engine designed for **CS & AI researchers and students**. Covering four generation modes — concept images, algorithm diagrams, data plots, and image reproduction — it leverages domestic free large-model capabilities to produce publication-ready visuals at zero cost.

The project draws on advanced expertise from top institutions including Shanghai Jiao Tong University, University of Chinese Academy of Sciences, CUHK-Shenzhen, Shanghai AI Lab, and HKUST(Guangzhou), engineering academic visual standards into an accessible open-source tool.

### Key Features

- **Four Generation Modes**:
  - `image` — Text-to-image via Cogview-3-Flash with LLM-enhanced prompts
  - `diagram` — Matplotlib code-generated vector diagrams at 300dpi
  - `data_plot` — 8 pre-built conference chart styles from JSON data
  - `image_repro` — Upload a reference figure, analyze and reproduce with matplotlib
- **Conference-Grade Visuals**: Colors, fonts, spines, and grids tuned to NeurIPS / ICML / ICLR standards
- **Free Domestic Pipeline**: Zhipu AI Cogview-3-Flash & GLM-4-Flash, zero data export
- **Multi-format Input**: Markdown, TXT, PDF papers, JSON data, reference images
- **Python API + CLI**: One line of code or one command to generate

### Quick Start

```bash
pip install scicovergen
```

```bash
export ZHIPU_API_KEY=your-api-key

# Mode 1: Text-to-image
scicovergen paper.md --mode image --style conference_diagram

# Mode 2: Precise vector diagram
scicovergen paper.md --mode diagram

# Mode 3: Data to plot
scicovergen data.json --mode data_plot --plot-style bar_paired_delta

# Mode 4: Image reproduction
scicovergen reference.png --mode image_repro
```

### Contributing

Issues and Pull Requests are welcome!

### License

[MIT](LICENSE)
