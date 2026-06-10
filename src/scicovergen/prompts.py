"""
场景化 Prompt 生成器

基于 baoyu-cover-image 的 5 维度体系，
针对论文封面、课题报告、学术海报三大科研场景进行深度优化。
"""

from typing import Dict


# 顶会流程图专用 pastel 马卡龙配色 (提取自 NeurIPS/ICLR 优质配图)
CONFERENCE_PASTEL_COLORS = {
    "light_blue": "#D5DEFF",      # 输入/数据模块
    "light_green": "#C8E5B3",     # 处理/核心模块
    "light_yellow": "#E3F2D9",    # 训练/阶段
    "light_coral": "#FFD4C7",     # 输出/结果
    "light_lavender": "#E8D5FF",  # 注意力/机制
    "light_gray": "#D4D4D4",      # 辅助组件
    "white": "#FFFFFF",           # 背景
    "deep_navy": "#2C3E50",       # 轮廓线/箭头
    "soft_black": "#333333",      # 边框
}

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

    @staticmethod
    def build_conference_diagram_prompt(analysis: Dict[str, str]) -> str:
        """构建顶会流程图风格 Prompt (NeurIPS/ICLR/CCF-A 专用)"""
        title = analysis.get("title", "Research Paper")
        core_method = analysis.get("core_method", "")
        math_objects = analysis.get("math_objects", "")
        core_operation = analysis.get("core_operation", "")
        visual_metaphor = analysis.get("visual_metaphor", "")
        field = analysis.get("field", "机器学习")

        prompt = f"""A professional flat vector technical diagram for a computer science research paper titled "{title}".

CORE CONCEPT: {core_method}
KEY ELEMENTS: {math_objects}
CORE OPERATION: {core_operation}
VISUAL METAPHOR: {visual_metaphor}

DESIGN SPECIFICATIONS:
- Flat 2D vector illustration, absolutely no perspective, no 3D effects, no isometric
- Clean line art with thin dark navy outlines (#2C3E50, 1-2px width)
- Minimal to zero shading, absolutely no gradients, no glossy effects, matte finish
- Rounded rectangles with thin dark borders for all modules and blocks
- Clear left-to-right pipeline flow with thin directional arrows (#2C3E50)
- Dashed bounding boxes grouping related modules into stages/phases
- Small minimalist geometric icons inside modules (gear, stacked layers, brain, eye, graph nodes, matrix grid)
- Grid-aligned, pixel-perfect mathematical precision in spacing

COLOR PALETTE (Pastel Macaron - exact hex codes):
- Background: pure white #FFFFFF
- Input/Data modules: light blue #D5DEFF
- Processing/Core modules: light green #C8E5B3
- Training/Stage blocks: light yellow/cream #E3F2D9
- Output/Result modules: light coral/peach #FFD4C7
- Attention/Mechanism: light lavender #E8D5FF
- Auxiliary components: light gray #D4D4D4
- Outlines, arrows, borders: deep navy #2C3E50

LAYOUT:
- Three clear stages: Input (left) -> Processing (center) -> Output (right)
- Generous white space (30-40%) between modules and stages
- Mathematical precision in alignment and proportions
- Clear visual hierarchy with stage containers and module blocks

VISUAL ELEMENTS:
- Rounded rectangle modules with thin dark outlines
- Small circles/dots for nodes, states, data points
- Thin directional arrows with arrowheads showing data flow
- Dashed lines for feedback loops, skip connections, optional paths
- Small flat geometric icons inside each module (no text, no letters)

MOOD: Professional, academic, clean, highly organized, subtle contrast, clarity over decoration, conveying technical precision and mathematical rigor

IMPORTANT:
- NO text, NO words, NO letters, NO alphabet characters, NO numbers in the image
- NO Chinese characters
- NO realistic human faces, hands, or bodies
- NO photorealistic elements, no photographs, no 3D renders
- NO complex gradients, no drop shadows, no glossy effects, no glass morphism
- NO watercolor, no brush strokes, no artistic distortion
- NO decorative elements that don't convey technical meaning
- Suitable for publication in NeurIPS, ICML, ICLR, CVPR, KDD, CCF-A venues
"""
        return prompt


class LLMPromptBuilder:
    """
    基于 LLM 的动态 Prompt 生成器

    调用 GLM-4-Flash 根据内容分析结果生成高质量图像提示词，
    同时完整复用 baoyu-cover-image 的 5 维度设计体系作为上下文约束。
    """

    # 顶会流程图专用 System Prompt (NeurIPS/ICLR/CCF-A 风格)
    CONFERENCE_DIAGRAM_SYSTEM_PROMPT = """你是一位国际顶尖的计算机科学论文配图设计师，专精于为 NeurIPS、ICML、ICLR、CVPR、KDD 等 CCF-A 类顶会设计技术流程图和概念示意图。

## 核心风格规范：顶会流程图风格 (NeurIPS/ICLR/CCF-A Style)
你必须生成用于 AI 图像生成模型（Cogview、DALL-E、Stable Diffusion）的英文提示词，风格必须是：

**1. 渲染风格 (Rendering)**
- Flat vector illustration, clean 2D technical diagram
- 2D flat, absolutely no perspective, no 3D effects, no isometric
- Clean line art with thin dark outlines (1-2px width)
- Minimal to zero shading, absolutely no gradients, no glossy effects
- Rounded corners on all rectangular elements
- Pixel-perfect alignment, grid-based layout

**2. 配色方案 (Palette - Pastel/Macaron)**
主色调必须使用以下精确的 pastel 马卡龙色系：
- Light blue #D5DEFF (soft sky blue, for input/data modules)
- Light green #C8E5B3 (soft mint, for processing/core modules)
- Light yellow/cream #E3F2D9 (warm beige, for training stages)
- Light coral/peach #FFD4C7 (soft salmon, for output/results)
- Light lavender #E8D5FF (soft purple, for attention/mechanism)
- Light gray #D4D4D4 (neutral, for auxiliary components)
- Pure white #FFFFFF (background)
辅助深色（仅用于细线、箭头、边框）：
- Deep navy #2C3E50 (for outlines and arrows)
- Soft black #333333 (for subtle borders)

**3. 构图与布局 (Composition)**
- Modular block diagram with clear horizontal pipeline flow (left-to-right) or vertical hierarchy (top-to-bottom)
- Clear directional arrows (thin, dark, with arrowheads) showing data flow between modules
- Dashed bounding boxes or colored background blocks for grouping related modules into stages/phases
- Visual hierarchy: large stage containers containing smaller module blocks
- Generous white space (30-40%) between modules
- Grid-aligned, mathematical precision in alignment
- Clear separation of input, processing, and output stages

**4. 视觉元素 (Visual Elements)**
- Rounded rectangles (modules/blocks) with thin dark outlines (#2C3E50)
- Small circles or dots (nodes, states, data points, decision points)
- Thin directional arrows (#2C3E50, 1-2px) with clear arrowheads
- Dashed lines for optional paths, feedback loops, skip connections
- Small minimalist geometric icons inside modules (gear for processing, stacked layers for neural networks, eye for vision, speech bubble for NLP, graph nodes for GNN, matrix grid for linear algebra)
- NO text labels, NO words, NO letters, NO numbers inside the image

**5. 情绪与氛围 (Mood)**
- Professional, academic, clean, highly organized
- Subtle contrast, not aggressive
- Clarity and information density over decoration
- Conveys technical precision and mathematical rigor
- Suitable for publication in top-tier venues

## 绝对禁止
- NO text, NO words, NO letters, NO alphabet characters, NO numbers in the image
- NO Chinese characters
- NO realistic human faces, hands, or bodies
- NO photorealistic elements, no photographs, no 3D renders
- NO complex gradients, no drop shadows, no glossy effects, no glass morphism
- NO decorative elements that don't convey technical meaning
- NO watercolor, no brush strokes, no artistic distortion

## 输出要求
- 使用英文撰写
- 250-400 词
- 必须包含：主体描述（模块、数据流、架构层次）、风格描述（flat vector pastel technical diagram）、色彩描述（精确 pastel hex codes）、构图描述（pipeline layout with arrows）、光影描述（flat, no shadows）
- 直接输出提示词，不要任何解释、不要 markdown、不要分点"""

    # 通用艺术风格 System Prompt
    SYSTEM_PROMPT = """你是一位国际顶尖的科研可视化提示词工程师，专精于将学术内容转化为用于 AI 图像生成模型（Cogview、DALL-E、Stable Diffusion）的高质量英文提示词。

## 5 维度设计体系
你必须在生成提示词时，潜意识中遵循以下 5 维度体系来组织视觉语言：

**1. Type（构图类型）**
- hero: 大视觉冲击力，标题叠加，适合产品发布、重大公告
- conceptual: 概念可视化，抽象核心思想，适合技术论文、方法论
- typography: 文字为主，标题突出，适合观点文章、引言
- metaphor: 视觉隐喻，具象表达抽象，适合哲学、成长、个人发展
- scene: 场景氛围，叙事感，适合故事、旅行、生活方式
- minimal: 极简构图，大量留白，适合禅意、专注、核心概念

**2. Palette（调色板）**
- warm: 友好亲和，橙、金黄、赤陶
- elegant: 精致优雅，柔和珊瑚、灰青、玫瑰粉
- cool: 科技专业，工程蓝、海军蓝、青色
- dark: 深色高级，电光紫、青色、品红
- earth: 自然有机，森林绿、鼠尾草、土棕
- vivid: 鲜艳活力，亮红、荧光绿、电光蓝
- pastel: 柔和梦幻，柔粉、薄荷、薰衣草
- mono: 黑白极简，黑、近黑、白
- retro: 复古怀旧，暗橙、灰粉、栗色

**3. Rendering（渲染风格）**
- flat-vector: 扁平矢量，统一轮廓，平涂填充，几何图标
- hand-drawn: 手绘草图，不完美笔触，纸纹质感，涂鸦
- painterly: 水彩/油画，笔触痕迹，颜色晕染，柔和边缘
- digital: 数字插画，精确边缘，微妙渐变，UI组件
- pixel: 像素艺术，像素网格，抖动，块状造型
- chalk: 粉笔黑板，粉笔笔触，粉尘效果，板面纹理

**4. Text（文本密度）**
- none: 纯视觉，无文字
- title-only: 仅标题
- title-subtitle: 标题+副标题
- text-rich: 信息密集

**5. Mood（情绪强度）**
- subtle: 低对比、柔和、轻量、平静
- balanced: 中等对比、正常饱和度、平衡
- bold: 高对比、鲜艳饱和、重量感、动态能量

## 兼容性规则（必须遵守）
- Palette×Rendering: cool配painterly不推荐；elegant配pixel/chalk不推荐；earth配pixel/chalk不推荐；pastel配pixel/chalk不推荐；mono配painterly不推荐；retro配chalk不推荐
- Type×Rendering: scene配flat-vector不推荐；metaphor配pixel不推荐；minimal配pixel/chalk不推荐
- Type×Text: typography不能配none；metaphor/scene/minimal不能配text-rich
- Type×Mood: minimal不能配bold

## 核心设计原则
1. 视觉隐喻优于字面描述：用抽象、诗意的视觉语言表达科学概念
2. 必须包含具体的学科视觉元素（数学对象、数据结构、算法流程、网络拓扑等）
3. 配色必须体现学科特性和情绪氛围
4. 构图必须有明确的视觉锚点和 40-60% 的呼吸空间（留白）
5. 必须考虑在小尺寸预览下的可读性
6. 使用专业摄影/艺术术语增强画面感（如 bokeh, depth of field, chiaroscuro, gradient mesh, volumetric lighting）

## 绝对禁止
- NO text, NO words, NO letters, NO alphabet characters in the image
- NO Chinese characters
- NO realistic human faces or human bodies
- 禁止空洞的泛泛描述（如"一张漂亮的图"、"高质量图像"）

## 输出要求
- 使用英文撰写
- 200-400 词
- 必须包含：主体描述（Subject）、风格描述（Style）、色彩描述（Color）、光影描述（Lighting）、构图描述（Composition）
- 必须有创意，使用隐喻、类比、视觉叙事
- 直接输出提示词，不要任何解释、不要 markdown 格式、不要分点说明"""

    @staticmethod
    def build_prompt(analysis: Dict[str, str], scene: str, client, style: str = "artistic") -> str:
        """
        调用 LLM 生成高质量 prompt

        Args:
            analysis: 内容分析结果字典
            scene: 场景类型 (paper_cover/project_report/academic_poster)
            client: ZhipuClient 实例
            style: 风格类型 ("artistic" | "conference_diagram")

        Returns:
            生成的 prompt 字符串
        """
        # 选择 system prompt
        if style == "conference_diagram":
            system_prompt = LLMPromptBuilder.CONFERENCE_DIAGRAM_SYSTEM_PROMPT
        else:
            system_prompt = LLMPromptBuilder.SYSTEM_PROMPT

        user_prompt = LLMPromptBuilder._build_user_prompt(analysis, scene, style)

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ]

        try:
            result = client.chat_completion(
                messages=messages,
                model="glm-4-flash",
                temperature=0.8,
                max_tokens=1500,
            )
            # 清理可能的 markdown 代码块
            result = result.strip()
            if result.startswith("```"):
                result = result.split("\n", 1)[-1].rsplit("```", 1)[0].strip()
            return result
        except Exception as e:
            print(f"[!] LLM Prompt 生成失败，回退到静态模板: {e}")
            return LLMPromptBuilder._static_build(analysis, scene, style)

    @staticmethod
    def _build_user_prompt(analysis: Dict[str, str], scene: str, style: str = "artistic") -> str:
        """构建发送给 LLM 的 user prompt"""
        scene_names = {
            "paper_cover": "学术论文封面",
            "project_report": "课题报告封面",
            "academic_poster": "学术会议海报",
        }
        scene_name = scene_names.get(scene, "科研封面")

        # 构建内容描述块
        content_blocks = []
        for key, label in [
            ("title", "标题"),
            ("core_method", "核心方法"),
            ("math_objects", "关键数学对象"),
            ("core_operation", "核心操作"),
            ("visual_metaphor", "视觉隐喻"),
            ("field", "学科领域"),
            ("project_type", "项目类型"),
            ("keywords", "关键词"),
            ("visual_elements", "视觉元素建议"),
            ("highlights", "研究亮点"),
            ("visual_focus", "视觉焦点"),
        ]:
            if key in analysis and analysis[key]:
                content_blocks.append(f"- {label}: {analysis[key]}")

        content_section = "\n".join(content_blocks) if content_blocks else "- 标题: 科研论文"

        # Conference diagram 专用 user prompt
        if style == "conference_diagram":
            return f"""请为以下计算机科学论文生成一个专业的技术流程图提示词（英文）。

## 场景类型
学术论文技术流程图 / 算法架构图 (NeurIPS/ICLR/CCF-A 风格)

## 内容分析
{content_section}

## 任务要求
1. 生成一个 250-400 词的英文图像生成提示词
2. 风格必须是：Flat vector technical diagram, 2D, no perspective, pastel macaron color palette
3. 必须包含模块化的 rounded rectangles、thin directional arrows、small geometric icons
4. 配色必须使用 pastel 色系：#D5DEFF, #C8E5B3, #E3F2D9, #FFD4C7, #E8D5FF, #D4D4D4, white background, dark outlines #2C3E50
5. 构图必须是清晰的 left-to-right pipeline 或 top-to-bottom hierarchy
6. 必须展示数据流、模块连接、处理阶段（Input -> Processing -> Output）
7. 模块内部使用小几何图标代替文字（gear, layers, nodes, matrix, brain, eye）
8. 图中绝对不能有任何文字、字母、数字
9. 直接输出提示词，不要任何解释、不要 markdown、不要分点。"""

        # 构建维度建议块 (artistic 风格)
        dims = []
        if "palette" in analysis:
            dims.append(f"- 建议配色: {analysis['palette']}")
        if "style" in analysis:
            dims.append(f"- 建议风格: {analysis['style']}")
        if "mood" in analysis:
            dims.append(f"- 建议情绪: {analysis['mood']}")
        dim_section = "\n".join(dims) if dims else "- 无具体建议，请自行推断"

        return f"""请为以下科研内容生成一个专业的图像生成提示词（英文）。

## 场景类型
{scene_name}

## 内容分析
{content_section}

## 维度建议
{dim_section}

## 任务要求
1. 根据内容自动推断最合适的 5 维度配置（Type, Palette, Rendering, Text, Mood）
2. 应用兼容性规则，确保维度组合合理（不合理的组合要调整）
3. 生成一个 200-400 词的英文图像生成提示词
4. 提示词必须具体、专业、有创意，避免泛泛而谈
5. 必须使用视觉隐喻，包含具体的数学/科学元素
6. 必须在提示词末尾包含 "NO text, NO words, NO letters, NO alphabet characters, NO Chinese characters, NO realistic human faces"

直接输出提示词，不要任何解释。"""

    @staticmethod
    def _static_build(analysis: Dict[str, str], scene: str, style: str = "artistic") -> str:
        """静态模板 fallback"""
        if style == "conference_diagram":
            return PromptBuilder.build_conference_diagram_prompt(analysis)
        if scene == "paper_cover":
            return PromptBuilder.build_paper_cover_prompt(analysis)
        elif scene == "project_report":
            return PromptBuilder.build_project_report_prompt(analysis)
        elif scene == "academic_poster":
            return PromptBuilder.build_academic_poster_prompt(analysis)
        else:
            return PromptBuilder.build_paper_cover_prompt(analysis)
