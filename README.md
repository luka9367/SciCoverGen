<div align="center">

# SciCoverGen

**面向科研新手的论文封面、课题报告、学术海报一键图像生成工具**

[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey.svg)]()

[English](#english) | [中文](#中文)

</div>

---

## 中文

### 简介

SciCoverGen 是一款专为科研新手打造的封面自动生成工具。只需提供论文/报告/海报的文本内容，即可一键生成专业、美观、符合学术规范的封面图像。

本项目基于 [baoyu-cover-image](https://github.com/macrochen/baoyu-cover-image) skill 深度魔改，**彻底移除所有境外图像模型依赖**，全面对接**智谱开放平台免费图像生成接口 Cogview-3-Flash**。新用户注册即可免费领取 API Key 开始使用，**全程杜绝数据出境风险**。

### 核心特性

- **一键生成**：5 分钟上手，一行代码生成专业封面
- **三大场景**：内置论文封面、课题报告、学术海报专属优化
- **智能分析**：GLM-4-Flash 自动分析内容，精准提取视觉元素
- **国产化**：纯国产 API，数据不出境，安全可靠
- **免费使用**：对接 Cogview-3-Flash 免费模型，零成本科研辅助
- **多格式支持**：支持 Markdown、TXT、PDF 等多种输入格式

### 快速开始

#### 1. 安装

```bash
pip install scicovergen
```

#### 2. 获取免费 API Key

1. 访问 [智谱开放平台](https://open.bigmodel.cn/)
2. 注册账号（**新用户免费领取额度**）
3. 创建 API Key

#### 3. 生成你的第一个封面

```python
import os
from scicovergen import SciCoverGen

# 设置 API Key
os.environ["ZHIPU_API_KEY"] = "your-api-key"

# 创建生成器并生成封面
gen = SciCoverGen()
gen.generate("your_paper.md", scene="paper_cover")
```

或使用命令行：

```bash
export ZHIPU_API_KEY=your-api-key
scicovergen paper.md --scene paper_cover
```

### 三大科研场景

| 场景 | 命令 | 特点 |
|------|------|------|
| **论文封面** | `--scene paper_cover` | 学术专业风格，数学可视化元素，冷色调 |
| **课题报告** | `--scene project_report` | 简洁结构化，数据图表元素，商务风格 |
| **学术海报** | `--scene academic_poster` | 视觉冲击力强，信息丰富，适合大幅展示 |

### 项目结构

```
SciCoverGen/
├── src/scicovergen/          # 核心源码
│   ├── __init__.py
│   ├── api_client.py         # 智谱 API 客户端
│   ├── analyzer.py           # 内容智能分析器
│   ├── prompts.py            # 场景化 Prompt 生成器
│   ├── generator.py          # 主生成器
│   ├── config.py             # 配置管理
│   ├── cli.py                # 命令行接口
│   └── utils.py              # 工具函数
├── examples/                  # 示例代码
│   ├── paper_cover/
│   ├── project_report/
│   └── academic_poster/
├── tests/                     # 单元测试
├── docs/                      # 文档
│   ├── getting_started.md
│   └── api_reference.md
├── .github/workflows/         # CI/CD
├── setup.py
├── pyproject.toml
├── requirements.txt
├── LICENSE
└── README.md
```

### 技术架构

```
用户输入 (论文/报告/海报)
    ↓
内容读取 (支持 MD/TXT/PDF)
    ↓
GLM-4-Flash 智能分析
    ↓
场景化 Prompt 构建
    ↓
Cogview-3-Flash 图像生成
    ↓
封面图像输出
```

### 与 baoyu-cover-image 的改进对比

| 特性 | baoyu-cover-image | SciCoverGen |
|------|-------------------|-------------|
| 目标用户 | 通用文章作者 | **科研新手** |
| 图像模型 | Gemini/Claude/DALL-E 等境外模型 | **智谱 Cogview-3-Flash（国产免费）** |
| 数据安全 | 数据出境 | **纯国产链路，数据不出境** |
| 科研场景 | 无 | **论文/报告/海报三大专属场景** |
| 中文支持 | 一般 | **深度优化，适合中文学术内容** |
| 视觉精度 | 通用 | **学科特定视觉元素库** |
| 使用成本 | 需付费 | **完全免费** |

### 贡献

欢迎提交 Issue 和 Pull Request！

### 许可证

[MIT](LICENSE)

---

## English

### Introduction

SciCoverGen is an automated cover image generator designed for research beginners. Simply provide your paper/report/poster text content, and generate professional, beautiful, academically-standard cover images with one click.

This project is deeply adapted from the [baoyu-cover-image](https://github.com/macrochen/baoyu-cover-image) skill, **completely removing all foreign image model dependencies**, and fully integrating with the **Zhipu AI Platform's free image generation API Cogview-3-Flash**. New users can register and receive a free API Key to start immediately, **ensuring zero data export risk**.

### Key Features

- **One-click generation**: Get started in 5 minutes, generate professional covers with one line of code
- **Three scenarios**: Built-in optimization for paper covers, project reports, and academic posters
- **Smart analysis**: GLM-4-Flash automatically analyzes content and extracts precise visual elements
- **Domestic AI**: Pure domestic API, data stays local, safe and reliable
- **Free to use**: Integrated with Cogview-3-Flash free model, zero-cost research assistance
- **Multi-format support**: Supports Markdown, TXT, PDF, and more input formats

### Quick Start

#### 1. Install

```bash
pip install scicovergen
```

#### 2. Get Free API Key

1. Visit [Zhipu AI Open Platform](https://open.bigmodel.cn/)
2. Register (**new users get free credits**)
3. Create an API Key

#### 3. Generate Your First Cover

```python
import os
from scicovergen import SciCoverGen

# Set API Key
os.environ["ZHIPU_API_KEY"] = "your-api-key"

# Create generator and generate cover
gen = SciCoverGen()
gen.generate("your_paper.md", scene="paper_cover")
```

Or use CLI:

```bash
export ZHIPU_API_KEY=your-api-key
scicovergen paper.md --scene paper_cover
```

### Three Research Scenarios

| Scenario | Command | Characteristics |
|----------|---------|-----------------|
| **Paper Cover** | `--scene paper_cover` | Academic professional style, math visualization, cool tones |
| **Project Report** | `--scene project_report` | Clean structured, data chart elements, business style |
| **Academic Poster** | `--scene academic_poster` | Strong visual impact, information-rich, large-format ready |

### Contributing

Issues and Pull Requests are welcome!

### License

[MIT](LICENSE)
