"""
学术海报生成示例

演示如何使用 SciCoverGen 为学术海报生成封面。
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "src"))

from scicovergen import SciCoverGen


def main():
    """生成学术海报封面示例"""

    gen = SciCoverGen()

    print("=" * 60)
    print("🎨 学术海报封面生成示例")
    print("=" * 60)

    result = gen.generate(
        source="example_poster.md",
        scene="academic_poster",
        output_dir="./poster_output",
    )

    if result:
        print(f"\n✅ 海报已生成: {result}")


if __name__ == "__main__":
    main()
