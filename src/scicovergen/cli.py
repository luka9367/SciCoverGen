"""
命令行接口 (CLI)

提供 scicovergen 命令行工具，支持一键生成科研封面。
"""

import argparse
import os
import sys

from .config import Config
from .generator import SciCoverGen, quick_generate


def main():
    """CLI 主入口"""
    parser = argparse.ArgumentParser(
        prog="scicovergen",
        description="SciCoverGen - 科研封面自动生成工具\n"
                    "面向科研新手的论文封面、课题报告、学术海报一键图像生成",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 生成论文封面
  scicovergen paper.md --scene paper_cover

  # 生成课题报告封面
  scicovergen report.md --scene project_report

  # 生成学术海报
  scicovergen poster.md --scene academic_poster

  # 指定输出目录
  scicovergen paper.md -o ./covers

  # 从环境变量读取 API Key
  export ZHIPU_API_KEY=your-api-key
  scicovergen paper.md

获取 API Key: https://open.bigmodel.cn/
        """,
    )

    parser.add_argument(
        "source",
        help="内容源文件路径（支持 .md, .txt, .pdf）或直接使用文本内容",
    )

    parser.add_argument(
        "--scene", "-s",
        choices=["paper_cover", "project_report", "academic_poster"],
        default="paper_cover",
        help="生成场景类型（默认: paper_cover）",
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
        help="不保存生成的 prompt 文件",
    )

    parser.add_argument(
        "--version", "-v",
        action="version",
        version="%(prog)s 1.0.0",
    )

    args = parser.parse_args()

    # 设置 API Key
    api_key = args.api_key or os.environ.get("ZHIPU_API_KEY")
    if api_key:
        Config.set_api_key(api_key)

    # 生成封面
    try:
        result = quick_generate(
            source=args.source,
            api_key=api_key,
            scene=args.scene,
            output_dir=args.output,
        )
        if result:
            sys.exit(0)
        else:
            sys.exit(1)
    except Exception as e:
        print(f"\n❌ 生成失败: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
