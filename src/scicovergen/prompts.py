"""
场景化 Prompt 生成器

基于 baoyu-cover-image 的 5 维度体系，
针对论文封面、课题报告、学术海报三大科研场景进行深度优化。
"""

from typing import Dict


# 学科视觉元素库
FIELD_VISUALS = {
    "机器学习/聚类": [
        "scatter plot clusters with different colors",
        "high-dimensional data points projected to low-dimensional manifold",
        "similarity matrix heatmap",
        "decision boundaries and class regions"
    ],
    "图论/谱聚类": [
        "graph Laplacian matrix with glowing eigenvalue decomposition",
        "network nodes with community structure highlighted",
        "spectral embedding visualization",
        "adjacency matrix with weighted edges"
    ],
    "多视图学习": [
        "multiple parallel data streams converging to unified representation",
        "multi-perspective geometric projections",
        "cross-view alignment and fusion",
        "multi-modal data integration"
    ],
    "正则化/优化": [
        "smooth constraint boundaries and feasible regions",
        "gradient descent trajectories on loss surface",
        "regularization curves and sparsity patterns",
        "optimization landscape with global minimum"
    ],
    "深度学习": [
        "neural network layers with activation patterns",
        "feature map visualizations",
        "attention heatmaps",
        "tensor flow diagrams"
    ],
    "计算机视觉": [
        "image processing pipeline stages",
        "feature extraction landmarks",
        "convolution kernel patterns",
        "semantic segmentation masks"
    ],
    "自然语言处理": [
        "word embedding vector spaces",
        "attention mechanism flow",
        "language model architecture",
        "semantic relationship graphs"
    ],
    "数据挖掘": [
        "association rule networks",
        "frequent pattern trees",
        "data stream processing",
        "anomaly detection boundaries"
    ],
    "强化学习": [
        "agent-environment interaction loops",
        "policy gradient trajectories",
        "reward landscape",
        "state-action value matrices"
    ],
    "数学理论": [
        "abstract mathematical structures",
        "proof tree diagrams",
        "axiom systems",
        "theorem visualization"
    ],
}

# 配色映射
PALETTE_MAP = {
    "cool": {
        "desc": "professional cool blue palette",
        "colors": "deep navy blue background, electric cyan and teal accents, white lines, subtle gradients"
    },
    "warm": {
        "desc": "warm approachable palette",
        "colors": "soft orange, golden yellow, terracotta tones, cream background"
    },
    "dark": {
        "desc": "dark cinematic premium palette",
        "colors": "deep black background, electric purple and magenta accents, neon highlights"
    },
    "vivid": {
        "desc": "vibrant energetic palette",
        "colors": "bright red, neon green, electric blue, high saturation"
    },
    "mono": {
        "desc": "monochrome clean palette",
        "colors": "pure black, near-black, white, clean grayscale gradients"
    },
    "elegant": {
        "desc": "elegant sophisticated palette",
        "colors": "soft coral, muted teal, dusty rose, champagne gold"
    },
    "earth": {
        "desc": "natural earth palette",
        "colors": "forest green, sage, earth brown, sand tones"
    },
    "pastel": {
        "desc": "soft pastel palette",
        "colors": "soft pink, mint, lavender, light cream"
    },
    "retro": {
        "desc": "retro nostalgic palette",
        "colors": "muted orange, dusty pink, maroon, vintage cream"
    },
}

# 风格映射
STYLE_MAP = {
    "geometric": "geometric abstract illustration, clean lines, mathematical precision",
    "flat-vector": "flat vector illustration, clean modern design, simple shapes",
    "digital": "polished digital illustration, precise edges, subtle gradients",
    "minimal": "minimalist design, generous whitespace, single focal element",
    "painterly": "soft watercolor style, brush strokes, artistic",
    "hand-drawn": "hand-drawn sketch style, organic lines, doodle-like",
}

# 情绪映射
MOOD_MAP = {
    "subtle": "low contrast, muted colors, light visual weight, calm professional aesthetic",
    "balanced": "medium contrast, normal saturation, balanced visual weight",
    "bold": "high contrast, vivid saturated colors, heavy visual weight, dynamic energy",
}


class PromptBuilder:
    """Prompt 构建器"""

    @staticmethod
    def build_paper_cover_prompt(analysis: Dict[str, str]) -> str:
        """构建论文封面 Prompt"""
        title = analysis.get("title", "Research Paper")
        core_method = analysis.get("core_method", "")
        math_objects = analysis.get("math_objects", "")
        core_operation = analysis.get("core_operation", "")
        visual_metaphor = analysis.get("visual_metaphor", "")
        field = analysis.get("field", "机器学习/聚类")
        palette = analysis.get("palette", "cool").lower()
        style = analysis.get("style", "geometric").lower()
        mood = analysis.get("mood", "subtle").lower()

        # 获取学科视觉元素
        visuals = FIELD_VISUALS.get(field, FIELD_VISUALS["机器学习/聚类"])

        # 获取配色
        palette_info = PALETTE_MAP.get(palette, PALETTE_MAP["cool"])

        # 获取风格
        style_desc = STYLE_MAP.get(style, STYLE_MAP["geometric"])

        # 获取情绪
        mood_desc = MOOD_MAP.get(mood, MOOD_MAP["subtle"])

        prompt = f"""A professional academic paper cover image for a computer science / mathematics research paper titled "{title}".

CORE RESEARCH: {core_method}
KEY MATHEMATICAL ELEMENTS: {math_objects}
CORE ALGORITHM OPERATION: {core_operation}

VISUAL CONCEPT: {visual_metaphor}

MUST-INCLUDE SPECIFIC ELEMENTS:
- {visuals[0]}
- {visuals[1] if len(visuals) > 1 else visuals[0]}
- Graph/network nodes and edges showing data relationships
- Mathematical curves and smooth constraint boundaries
- Abstract geometric shapes (NO realistic human faces)
- Matrix or grid structures showing data organization

COMPOSITION:
- Left/upper area: Input data streams or raw data visualization
- Center: Core algorithm process (matrix operations, graph transformations, spectral decomposition)
- Right/lower area: Output results (clustered groups, unified representation, optimization landscape)
- Flow arrows connecting the three stages

STYLE: {style_desc}
COLOR PALETTE: {palette_info['colors']}
MOOD: {mood_desc}
QUALITY: High resolution, clean background, generous whitespace (40-50%), suitable for academic publication

IMPORTANT:
- NO text, NO words, NO letters, NO alphabet characters in the image
- NO Chinese characters
- NO realistic human faces or bodies
- Pure visual design with mathematical and data visualization elements only
- Professional, technical, elegant aesthetic
"""
        return prompt

    @staticmethod
    def build_project_report_prompt(analysis: Dict[str, str]) -> str:
        """构建课题报告封面 Prompt"""
        title = analysis.get("title", "Project Report")
        project_type = analysis.get("project_type", "Research")
        keywords = analysis.get("keywords", "")
        visual_elements = analysis.get("visual_elements", "")
        palette = analysis.get("palette", "cool").lower()
        style = analysis.get("style", "flat-vector").lower()
        mood = analysis.get("mood", "balanced").lower()

        palette_info = PALETTE_MAP.get(palette, PALETTE_MAP["cool"])
        style_desc = STYLE_MAP.get(style, STYLE_MAP["flat-vector"])
        mood_desc = MOOD_MAP.get(mood, MOOD_MAP["balanced"])

        prompt = f"""A professional project report cover image for a {project_type} project titled "{title}".

PROJECT KEYWORDS: {keywords}
VISUAL ELEMENTS: {visual_elements}

DESIGN REQUIREMENTS:
- Clean and structured layout reflecting project organization
- Professional iconography related to research and development
- Data visualization elements (charts, graphs, progress indicators)
- Hierarchical information structure
- Modern corporate aesthetic

STYLE: {style_desc}
COLOR PALETTE: {palette_info['colors']}
MOOD: {mood_desc}
QUALITY: High resolution, clean background, generous whitespace, suitable for formal report

IMPORTANT:
- NO text, NO words, NO letters, NO alphabet characters
- NO Chinese characters
- NO realistic human faces
- Professional, organized, clear visual communication
"""
        return prompt

    @staticmethod
    def build_academic_poster_prompt(analysis: Dict[str, str]) -> str:
        """构建学术海报封面 Prompt"""
        title = analysis.get("title", "Academic Poster")
        highlights = analysis.get("highlights", "")
        visual_focus = analysis.get("visual_focus", "")
        palette = analysis.get("palette", "vivid").lower()
        style = analysis.get("style", "bold").lower()
        mood = analysis.get("mood", "bold").lower()

        palette_info = PALETTE_MAP.get(palette, PALETTE_MAP["vivid"])
        style_desc = STYLE_MAP.get(style, STYLE_MAP["digital"])
        mood_desc = MOOD_MAP.get(mood, MOOD_MAP["bold"])

        prompt = f"""A striking academic conference poster cover image for "{title}".

RESEARCH HIGHLIGHTS: {highlights}
VISUAL FOCUS: {visual_focus}

DESIGN REQUIREMENTS:
- Eye-catching, designed to attract attention from distance
- Bold visual hierarchy with clear focal point
- Rich information visualization (charts, diagrams, comparison graphics)
- Dynamic composition with energy and movement
- Professional but visually impactful
- Multiple layered elements showing research depth

STYLE: {style_desc}
COLOR PALETTE: {palette_info['colors']}
MOOD: {mood_desc}
QUALITY: Ultra high resolution, vivid colors, maximum visual impact, suitable for large format printing

IMPORTANT:
- NO text, NO words, NO letters, NO alphabet characters
- NO Chinese characters
- NO realistic human faces
- Bold, dynamic, information-rich visual design
"""
        return prompt
