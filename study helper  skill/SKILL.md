---
name: college-textbook-review-v2
description: 智能读取大学生教材资料，自动识别大文件分章处理，交互式收集复习重点，结合考点规律生成结构化复习Word文档。
triggers:
  - "复习重点"
  - "考点梳理"
  - "期末突击"
  - "分章复习"
inputs:
  materials_path: string   # 资料文件路径
  course_name: string      # 课程名称
  exam_type: string        # 考试形式（可选）
  user_focus: string       # 用户指定重点（可选，未提供则触发交互）
---
# 工作流执行步骤

## Step 1: 资料预处理与智能分章
type: run
command: python 文件预处理.py "{{inputs.materials_path}}" --auto-split --chunk-size 50000
description: 读取并清洗资料。若文本长度 > 5万字或检测到明确章节标记（如“第X章”“Part X”），自动按章节切分并输出结构化块列表。
output: processed_chunks
timeout: 90s

## Step 2: 交互式重点收集（若未提供）
type: prompt
template: |
  请向用户输出以下结构化问题，等待回复后提取为JSON格式：
  1. 本次复习最关注的章节/知识点是？（可填“全部”或具体名称）
  2. 剩余复习时间与目标强度？（如：考前3天/系统过一遍/只抓及格线）
  3. 薄弱题型或希望强化的方向？（如：计算推导/概念辨析/简答论述）
  回复格式要求：{"focus_chapters": [], "time_goal": "", "weak_points": ""}
interactive: true
output: user_focus_json
condition: "{{inputs.user_focus}} == null or {{inputs.user_focus}} == ''"

## Step 3: 深度分析与考点提炼
type: prompt
template_file: analyze_summarize.md
variables:
  materials: "{{output.processed_chunks}}"
  user_focus: "{{user_focus_json or inputs.user_focus}}"
  course: "{{inputs.course_name}}"
  exam: "{{inputs.exam_type or '综合笔试'}}"
  is_chunked: "{{len(processed_chunks) > 1}}"
output: analysis_result
max_tokens: 12000

## Step 4: 资料文件生成
type: run
command: python 资料文件生成.py "{{output.analysis_result}}" "{{inputs.course_name}}"
output: docx_path
timeout: 60s

## Step 5: 保存至桌面并返回确认
type: run
command: |
  DEST="$HOME/Desktop/{{inputs.course_name}}_复习重点总结.docx"
  cp "{{output.docx_path}}" "$DEST"
  echo "✅ 文档已生成并保存至桌面：$DEST"
output: final_path