"""
命令行接口 (CLI)

提供 scicovergen 命令行工具，支持一键生成科研配图。
支持四种模式：
- image:       文生图（Cogview-3-Flash），适合概念性配图
- diagram:     代码精确绘图（Matplotlib），适合算法流程图
- data_plot:   数据转绘图（8种顶会预建风格），适合实验图表
- image_repro: 图像复现（分析配图风格并 matplotlib 还原），适合复现论文图
"""

import argparse
import json
import os
import sys

from .config import Config
from .generator import SciCoverGen


def main():
    """CLI 主入口"""
    parser = argparse.ArgumentParser(
        prog="scicovergen",
        description="SciCoverGen - 科研配图自动生成工具\n"
                    "面向科研人员的论文封面、算法流程图、实验图表、图像复现一键生成\n"
                    "支持文生图、代码绘图、数据绘图、图像复现四大模式",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # === 文生图模式 ===
  # 生成论文概念配图（通用艺术风格）
  scicovergen paper.md --mode image --style artistic

  # 生成顶会风格流程图（pastel 扁平矢量风格）
  scicovergen paper.md --mode image --style conference_diagram

  # === 代码绘图模式 ===
  # 生成精确矢量流程图（Matplotlib，可直接用于论文）
  scicovergen paper.md --mode diagram

  # === 数据绘图模式 ===
  # 从 JSON 数据生成配对对比柱状图
  scicovergen data.json --mode data_plot --plot-style bar_paired_delta

  # 从 JSON 数据生成 t-SNE 聚类散点图
  scicovergen tsne_data.json --mode data_plot --plot-style scatter_tsne_cluster

  # === 图像复现模式 ===
  # 分析论文配图并 matplotlib 还原
  scicovergen reference_fig.png --mode image_repro

  # === 其他 ===
  # 指定输出目录
  scicovergen paper.md -o ./covers

  # 从环境变量读取 API Key
  export ZHIPU_API_KEY=your-api-key
  scicovergen paper.md

获取 API Key: https://open.bigmodel.cn/
注意: Cogview-3-Flash 免费版生成的图片带有 "AI生成" 水印，
      如需无水印请使用 --mode diagram / data_plot / image_repro
        """,
    )

    parser.add_argument(
        "source",
        help="内容源（取决于 mode: 文件路径/文本/JSON数据文件/图像路径）",
    )

    parser.add_argument(
        "--scene", "-s",
        choices=["paper_cover", "project_report", "academic_poster"],
        default="paper_cover",
        help="生成场景类型（默认: paper_cover，仅 image/diagram 模式有效）",
    )

    parser.add_argument(
        "--mode", "-m",
        choices=["image", "diagram", "data_plot", "image_repro"],
        default="image",
        help="生成模式（默认: image）",
    )

    parser.add_argument(
        "--style", "-st",
        choices=["artistic", "conference_diagram"],
        default="artistic",
        help="风格类型（仅 image 模式有效，默认: artistic）",
    )

    parser.add_argument(
        "--plot-style", "-ps",
        choices=[
            "bar_paired_delta", "bar_grouped_hatch",
            "line_confidence_band", "line_training_curve", "line_loss_with_inset",
            "scatter_tsne_cluster", "scatter_broken_axis",
            "radar_dual_series",
        ],
        default=None,
        help="绘图风格（仅 data_plot 模式有效）",
    )

    parser.add_argument(
        "--data", "-d",
        default=None,
        help="JSON 数据文件路径（data_plot 模式下，也可直接传入 source）",
    )

    parser.add_argument(
        "--output", "-o",
        default="./scicovergen_output",
        help="输出目录（默认: ./scicovergen_output）",
    )

    parser.add_argument(
        "--api-key", "-k",
        default=None,
        help="智谱 API Key（默认从环境变量 ZHIPU_API_KEY 读取）",
    )

    parser.add_argument(
        "--no-prompt",
        action="store_true",
        help="不保存生成的 prompt 文件（仅 image 模式）",
    )

    parser.add_argument(
        "--version", "-v",
        action="version",
        version="%(prog)s 1.3.0",
    )

    args = parser.parse_args()

    # 设置 API Key
    api_key = args.api_key or os.environ.get("ZHIPU_API_KEY")
    if api_key:
        Config.set_api_key(api_key)

    # 数据绘图模式：读取 JSON 数据
    plot_data = None
    if args.mode == "data_plot":
        data_source = args.data or args.source
        if os.path.isfile(data_source):
            try:
                with open(data_source, "r", encoding="utf-8") as f:
                    plot_data = json.load(f)
            except json.JSONDecodeError as e:
                print(f"[ERROR] JSON 解析失败: {e}")
                sys.exit(1)
        else:
            print(f"[ERROR] 数据文件不存在: {data_source}")
            sys.exit(1)

        if not args.plot_style:
            print("[ERROR] data_plot 模式需要指定 --plot-style")
            print("  可用风格: bar_paired_delta, bar_grouped_hatch,")
            print("            line_confidence_band, line_training_curve,")
            print("            line_loss_with_inset, scatter_tsne_cluster,")
            print("            scatter_broken_axis, radar_dual_series")
            sys.exit(1)

    # 初始化生成器
    gen = SciCoverGen(api_key=api_key, output_dir=args.output)

    # 生成配图
    try:
        if args.mode == "data_plot":
            result = gen.generate(
                source=plot_data,
                mode="data_plot",
                style=args.plot_style,
                output_dir=args.output,
            )
        elif args.mode == "image_repro":
            result = gen.generate(
                source=args.source,
                mode="image_repro",
                output_dir=args.output,
            )
        else:
            result = gen.generate(
                source=args.source,
                scene=args.scene,
                mode=args.mode,
                style=args.style,
                output_dir=args.output,
                save_prompt=not args.no_prompt,
            )

        if result:
            sys.exit(0)
        else:
            sys.exit(1)
    except Exception as e:
        print(f"\n[ERROR] 生成失败: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
