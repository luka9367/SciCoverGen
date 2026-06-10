"""
课题报告封面生成示例

演示如何使用 SciCoverGen 为课题报告生成专业封面。
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "src"))

from scicovergen import SciCoverGen


def main():
    """生成课题报告封面示例"""

    gen = SciCoverGen()

    print("=" * 60)
    print("📋 课题报告封面生成示例")
    print("=" * 60)

    result = gen.generate(
        source="example_report.md",
        scene="project_report",
        output_dir="./report_output",
    )

    if result:
        print(f"\n✅ 封面已生成: {result}")


if __name__ == "__main__":
    main()
