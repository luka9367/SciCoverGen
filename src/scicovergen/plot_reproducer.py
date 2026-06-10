"""
图像转绘图复现引擎 (Plot Reproducer)

深度融合 plot-from-image 能力：
用户上传论文配图 -> 自动分析风格特征 -> 生成 matplotlib 复现代码 -> 输出 300dpi PNG

工作流程：
1. Measure: PIL 分析图像尺寸、宽高比、主导颜色
2. Match: 基于视觉特征匹配 8 种预建风格
3. Analyze: LLM 分析字体、spine、grid、特殊元素
4. Build: 生成并执行 matplotlib 复现代码
"""

import os
import re
import json
import tempfile
import subprocess
from typing import Dict, Any, Optional, Tuple, List

import numpy as np
from PIL import Image

from .plot_styles import get_style_config, list_styles


class PlotReproducer:
    """
    论文配图复现器

    Usage:
        repro = PlotReproducer(api_client)
        repro.reproduce("input_fig.png", "output_repro.png")
    """

    DPI = 300

    def __init__(self, api_client=None):
        """
        Args:
            api_client: 可选的 LLM API 客户端（用于增强分析）
        """
        self.client = api_client

    def reproduce(
        self,
        image_path: str,
        output_path: str,
        use_llm: bool = True,
    ) -> str:
        """
        复现一张论文配图

        Args:
            image_path: 输入图像路径（PNG/JPG）
            output_path: 输出 PNG 路径
            use_llm: 是否使用 LLM 增强分析

        Returns:
            输出文件路径
        """
        print(f"[REPRO] 分析图像: {image_path}")

        # 1. 基础图像分析
        analysis = self._analyze_image(image_path)
        print(f"[OK] 图像分析完成")
        print(f"  - 尺寸: {analysis['width']}x{analysis['height']}")
        print(f"  - 宽高比: {analysis['aspect_ratio']:.2f}")
        print(f"  - 检测风格: {analysis.get('matched_style', 'unknown')}")

        # 2. 匹配预建风格
        matched_style = analysis.get("matched_style")
        style_config = None
        if matched_style:
            try:
                style_config = get_style_config(matched_style)
                print(f"[OK] 匹配到预建风格: {matched_style}")
            except ValueError:
                pass

        # 3. LLM 增强分析（可选）
        llm_code = None
        if use_llm and self.client:
            print(f"[LLM] 请求风格分析与代码生成...")
            llm_code = self._llm_generate_code(analysis, style_config)
            if llm_code:
                print(f"[OK] LLM 代码生成完成")

        # 4. 生成并执行代码
        if llm_code:
            script_path = self._save_and_run(llm_code, output_path)
        elif matched_style:
            # fallback: 基于预建风格生成模板代码
            template_code = self._generate_template_code(analysis, matched_style)
            script_path = self._save_and_run(template_code, output_path)
        else:
            # 最终 fallback: 通用模板
            generic_code = self._generate_generic_code(analysis)
            script_path = self._save_and_run(generic_code, output_path)

        print(f"[DONE] 复现完成: {output_path}")
        return output_path

    # ── Step 1: 基础图像分析 ──────────────────────────
    def _analyze_image(self, image_path: str) -> Dict[str, Any]:
        """用 PIL 分析图像的基本特征"""
        img = Image.open(image_path)
        w, h = img.size
        ar = w / h

        # 主导颜色（简化版：取图像缩略图的主颜色）
        thumb = img.convert("RGB").resize((50, 50))
        pixels = np.array(thumb).reshape(-1, 3)
        # K-means 简化：取均值附近最密集的颜色
        mean_color = pixels.mean(axis=0).astype(int).tolist()

        # 颜色分布特征
        r, g, b = pixels[:, 0], pixels[:, 1], pixels[:, 2]
        color_features = {
            "red_dominant": float(r.mean()) > max(g.mean(), b.mean()) + 20,
            "blue_dominant": float(b.mean()) > max(r.mean(), g.mean()) + 20,
            "green_dominant": float(g.mean()) > max(r.mean(), b.mean()) + 20,
            "warm_tone": float(r.mean()) > float(b.mean()),
            "high_contrast": float(pixels.std()) > 60,
        }

        # 布局推断（基于宽高比）
        layout_hint = "wide" if ar > 1.5 else "tall" if ar < 0.8 else "square"

        analysis = {
            "width": w,
            "height": h,
            "aspect_ratio": ar,
            "figsize": self._compute_figsize(w, h),
            "mean_color": mean_color,
            "color_features": color_features,
            "layout_hint": layout_hint,
        }

        # 风格匹配
        matched = self._match_style(analysis)
        if matched:
            analysis["matched_style"] = matched

        return analysis

    def _compute_figsize(self, px_w: int, px_h: int) -> Tuple[float, float]:
        """根据像素尺寸计算 figsize（inch），保持宽高比"""
        # 通常论文配图宽度在 3.5-7 inches 之间
        target_w = min(max(px_w / self.DPI, 3.5), 7.0)
        target_h = target_w * (px_h / px_w)
        return (round(target_w, 2), round(target_h, 2))

    def _match_style(self, analysis: Dict[str, Any]) -> Optional[str]:
        """
        基于视觉特征匹配预建风格
        """
        cf = analysis["color_features"]
        ar = analysis["aspect_ratio"]

        # 简单启发式规则
        scores = {}

        # bar_paired_delta: 高对比、冷暖对比、宽图
        if cf.get("high_contrast") and ar > 1.2:
            scores["bar_paired_delta"] = scores.get("bar_paired_delta", 0) + 2

        # bar_grouped_hatch: 多色、宽图
        if ar > 1.2:
            scores["bar_grouped_hatch"] = scores.get("bar_grouped_hatch", 0) + 1

        # line_confidence_band: 中等对比、宽图
        if ar > 1.3:
            scores["line_confidence_band"] = scores.get("line_confidence_band", 0) + 1
            scores["line_training_curve"] = scores.get("line_training_curve", 0) + 1
            scores["line_loss_with_inset"] = scores.get("line_loss_with_inset", 0) + 1

        # scatter_tsne_cluster: 方形、多色
        if analysis["layout_hint"] == "square":
            scores["scatter_tsne_cluster"] = scores.get("scatter_tsne_cluster", 0) + 2
            scores["radar_dual_series"] = scores.get("radar_dual_series", 0) + 1

        # scatter_broken_axis: 宽图、可能有空白区域
        if ar > 1.5:
            scores["scatter_broken_axis"] = scores.get("scatter_broken_axis", 0) + 1

        if not scores:
            return None
        return max(scores, key=scores.get)

    # ── Step 3: LLM 代码生成 ──────────────────────────
    def _llm_generate_code(
        self,
        analysis: Dict[str, Any],
        style_config: Optional[Dict[str, Any]] = None,
    ) -> Optional[str]:
        """使用 LLM 生成复现代码"""
        if not self.client:
            return None

        matched = analysis.get("matched_style", "unknown")
        figsize = analysis["figsize"]
        colors = analysis["color_features"]

        system_prompt = """You are an expert scientific figure reproduction engineer.
Generate a complete, runnable Python matplotlib script that reproduces a paper figure.
The script must:
- Use only standard libraries: numpy, matplotlib, PIL
- Save output to OUTPUT_PATH (use a placeholder string)
- Use dpi=300, bbox_inches='tight', facecolor='white'
- Include simulated realistic data if no actual data is provided
- Match the described style as closely as possible
- Be self-contained and executable
"""

        user_prompt = f"""Generate a matplotlib reproduction script for a scientific figure with the following analysis:

IMAGE ANALYSIS:
- Dimensions: {analysis['width']}x{analysis['height']} px
- Aspect Ratio: {analysis['aspect_ratio']:.2f}
- Recommended figsize: {figsize[0]} x {figsize[1]} inches
- Dominant Color: RGB{analysis['mean_color']}
- Color Features: {json.dumps(colors)}
- Layout: {analysis['layout_hint']}

MATCHED STYLE: {matched}
"""

        if style_config:
            user_prompt += f"""
STYLE CONFIGURATION:
- Type: {style_config['type']}
- Description: {style_config['description']}
- Colors: {json.dumps(style_config['colors'])}
- Key Parameters: {json.dumps(style_config['params'])}
"""

        user_prompt += """
Please output ONLY the Python script (no markdown code fences, no explanations).
The script should define a function `generate(output_path)` that creates and saves the figure.
Include `if __name__ == "__main__": generate("output.png")` at the end.
"""

        try:
            result = self.client.chat_completion(
                [{"role": "system", "content": system_prompt},
                 {"role": "user", "content": user_prompt}],
                max_tokens=4000,
                temperature=0.3,
            )
            code = self._extract_code(result)
            return code
        except Exception as e:
            print(f"[!] LLM 代码生成失败: {e}")
            return None

    def _extract_code(self, text: str) -> str:
        """从 LLM 输出中提取 Python 代码"""
        text = text.strip()
        if text.startswith("```"):
            lines = text.split("\n")
            if lines[0].startswith("```python") or lines[0].startswith("```"):
                text = "\n".join(lines[1:])
            if text.endswith("```"):
                text = text[:-3].strip()
        return text

    # ── Step 4: 模板代码生成 ──────────────────────────
    def _generate_template_code(
        self,
        analysis: Dict[str, Any],
        style_name: str,
    ) -> str:
        """基于预建风格生成模板代码"""
        figsize = analysis["figsize"]
        config = get_style_config(style_name)
        colors = config["colors"]
        params = config["params"]

        code = f'''"""
Auto-generated reproduction template
Style: {style_name}
Original aspect ratio: {analysis['aspect_ratio']:.2f}
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# Global style
plt.rcParams.update({{
    "font.family": "{params.get('font_family', 'sans-serif')}",
    "figure.dpi": 300,
}})

fig, ax = plt.subplots(figsize=({figsize[0]}, {figsize[1]}))

# Simulated data (replace with actual values)
np.random.seed(42)
x = np.linspace(0, 10, 50)
y1 = np.sin(x) + np.random.normal(0, 0.1, 50)
y2 = np.cos(x) + np.random.normal(0, 0.1, 50)

# Plot
ax.plot(x, y1, color="{colors.get('primary', '#1F77B4')}", lw=1.8, label="Series A")
ax.plot(x, y2, color="{colors.get('secondary', '#FF7F0E')}", lw=1.8, label="Series B")

# Style
ax.set_xlabel("X Axis", fontsize=11)
ax.set_ylabel("Y Axis", fontsize=11)
ax.legend(frameon=False)

fig.savefig("OUTPUT_PATH", dpi=300, bbox_inches="tight", facecolor="white")
plt.close(fig)
'''
        return code

    def _generate_generic_code(self, analysis: Dict[str, Any]) -> str:
        """通用 fallback 模板"""
        figsize = analysis["figsize"]
        return f'''"""
Generic reproduction template
Aspect ratio: {analysis['aspect_ratio']:.2f}
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize=({figsize[0]}, {figsize[1]}))

np.random.seed(42)
x = np.arange(5)
y = np.random.uniform(50, 100, 5)
ax.bar(x, y, color="#5B9BD5")
ax.set_xticks(x)
ax.set_xticklabels(["A", "B", "C", "D", "E"])
ax.set_ylabel("Value")

fig.savefig("OUTPUT_PATH", dpi=300, bbox_inches="tight", facecolor="white")
plt.close(fig)
'''

    # ── Step 5: 保存并执行 ──────────────────────────
    def _save_and_run(self, code: str, output_path: str) -> str:
        """保存代码到临时文件并执行"""
        # 替换 OUTPUT_PATH 占位符
        code = code.replace('"OUTPUT_PATH"', f'r"{output_path}"')
        code = code.replace("'OUTPUT_PATH'", f'r"{output_path}"')

        # 确保输出目录存在
        out_dir = os.path.dirname(output_path) or "."
        os.makedirs(out_dir, exist_ok=True)

        # 写入临时脚本
        fd, script_path = tempfile.mkstemp(suffix=".py")
        try:
            with os.fdopen(fd, "w", encoding="utf-8") as f:
                f.write(code)

            print(f"[EXEC] 执行复现脚本: {script_path}")
            result = subprocess.run(
                ["python", script_path],
                capture_output=True, text=True, timeout=60
            )
            if result.returncode != 0:
                print(f"[!] 脚本执行出错:\n{result.stderr}")
            else:
                print(f"[OK] 脚本执行成功")
        finally:
            try:
                os.remove(script_path)
            except OSError:
                pass

        return output_path
