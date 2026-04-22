---
name: college-textbook-review-v2
description: 智能读取大学生教材资料，自动识别大文件分章处理，交互式收集复习重点，结合考点规律生成结构化复习Word文档。
triggers:
  - "复习重点"
  - "考点梳理"
  - "期末突击"
  - "分章复习"
inputs:
  materials_path:
    type: string
    description: 资料文件路径（支持 PDF、DOCX、TXT、MD、HTML、PPTX、XLSX）
  course_name:
    type: string
    description: 课程名称（如：大学物理、线性代数）
  exam_type:
    type: string
    description: 考试形式（可选，如：闭卷笔试、开卷、机考）
  user_focus:
    type: string
    description: 用户指定重点（可选，未提供则触发交互式询问）
---

# 工作流执行步骤

## Step 1: 资料预处理与智能分章
- **命令**: `python 文件预处理.py "{{inputs.materials_path}}" --auto-split --chunk-size 50000`
- **说明**: 读取并清洗资料。若文本长度 > 5万字或检测到明确章节标记（如"第X章""Part X"），自动按章节切分并输出结构化块列表。
- **超时**: 90秒
- **输出**: `processed_chunks`

## Step 2: 交互式重点收集（条件触发）
- **触发条件**: `{{inputs.user_focus}}` 为空或未提供
- **操作**: 向用户输出以下结构化问题，等待回复后提取为 JSON 格式：
  1. 本次复习最关注的章节/知识点是？（可填"全部"或具体名称）
  2. 剩余复习时间与目标强度？（如：考前3天/系统过一遍/只抓及格线）
  3. 薄弱题型或希望强化的方向？（如：计算推导/概念辨析/简答论述）
- **回复格式要求**: `{"focus_chapters": [], "time_goal": "", "weak_points": ""}`
- **输出**: `user_focus_json`

## Step 3: 深度分析与考点提炼
- **操作**: 读取 `analyze_summarize.md` 提示词模板，注入以下变量：
  - `materials`: `{{output.processed_chunks}}`
  - `user_focus`: `{{user_focus_json or inputs.user_focus}}`
  - `course`: `{{inputs.course_name}}`
  - `exam`: `{{inputs.exam_type or '综合笔试'}}`
  - `is_chunked`: `{{len(processed_chunks) > 1}}`
- **说明**: 调用大模型进行结构化分析，生成 Markdown 格式的复习指南。
- **最大 Token**: 12000
- **输出**: `analysis_result`

## Step 4: 资料文件生成
- **命令**: `python 资料文件生成.py "{{output.analysis_result}}" "{{inputs.course_name}}"`
- **说明**: 将分析结果转换为格式规范的 Word 文档（含封面、目录、多级标题、表格等）。
- **超时**: 60秒
- **输出**: `docx_path`

## Step 5: 保存至桌面并返回确认
- **命令**:
  ```bash
  DEST="$HOME/Desktop/{{inputs.course_name}}_复习重点总结.docx"
  cp "{{output.docx_path}}" "$DEST"
  echo "✅ 文档已生成并保存至桌面：$DEST"
  ```
- **说明**: 将生成的 Word 文档复制到用户桌面，并返回确认信息。
- **输出**: `final_path`
