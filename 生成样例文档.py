"""
样例文档生成脚本
将 样例数据.md 转换为格式规范的 Word 文档
用法: python 生成样例文档.py
"""

import os
import re
from pathlib import Path

from docx import Document
from docx.shared import Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn

from 资料文件生成 import QuickDocument


def parse_markdown_sections(md_text: str):
    """
    简单解析 Markdown，提取章节结构和内容
    返回 sections 列表，适配 QuickDocument.generate_full_document
    """
    lines = md_text.split('\n')
    sections = []
    current_section = None
    current_content = []
    in_table = False
    table_headers = []
    table_rows = []
    in_code = False
    code_lines = []

    def flush_section():
        nonlocal current_section, current_content
        if current_section:
            current_section["content"] = current_content
            sections.append(current_section)
            current_section = None
            current_content = []

    def flush_table():
        nonlocal in_table, table_headers, table_rows, current_content
        if in_table and table_headers:
            current_content.append({
                "type": "table",
                "headers": table_headers,
                "rows": table_rows,
                "col_widths": [Cm(4)] * len(table_headers)
            })
        in_table = False
        table_headers = []
        table_rows = []

    def flush_code():
        nonlocal in_code, code_lines, current_content
        if in_code and code_lines:
            current_content.append({
                "type": "text",
                "text": "[代码/公式区块]\n" + "\n".join(code_lines)
            })
        in_code = False
        code_lines = []

    i = 0
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        # 代码块
        if stripped.startswith('```'):
            if in_code:
                flush_code()
            else:
                flush_table()
                in_code = True
            i += 1
            continue

        if in_code:
            code_lines.append(line)
            i += 1
            continue

        # 标题
        if stripped.startswith('# ') and not stripped.startswith('## '):
            flush_table()
            flush_section()
            current_section = {
                "level": 1,
                "title": stripped.lstrip('#').strip(),
                "content": []
            }
            i += 1
            continue

        if stripped.startswith('## '):
            flush_table()
            if current_section is None:
                current_section = {"level": 1, "title": "正文", "content": []}
            current_content.append({"type": "page_break"})
            current_section["content"] = current_content
            sections.append(current_section)
            current_section = {
                "level": 2,
                "title": stripped.lstrip('#').strip(),
                "content": []
            }
            current_content = []
            i += 1
            continue

        if stripped.startswith('### '):
            flush_table()
            current_content.append({
                "type": "text",
                "text": stripped.lstrip('#').strip(),
                "style": "heading3"
            })
            i += 1
            continue

        # 表格
        if '|' in stripped and not stripped.startswith('*') and not stripped.startswith('-'):
            if not in_table:
                in_table = True
                table_headers = []
                table_rows = []

            cells = [c.strip() for c in stripped.split('|')]
            cells = [c for c in cells if c]  # 移除空单元格

            if cells and all(c.replace('-', '') == '' for c in cells):
                # 分隔行，跳过
                i += 1
                continue

            if table_headers and cells:
                table_rows.append(cells)
            elif cells:
                table_headers = cells

            i += 1
            continue
        else:
            if in_table:
                flush_table()

        # 列表
        if stripped.startswith(('- ', '* ')):
            item_text = stripped[2:].strip()
            # 检查是否是列表项中的子内容
            current_content.append({
                "type": "list",
                "items": [item_text],
                "ordered": False
            })
            i += 1
            continue

        if re.match(r'^\d+\.', stripped):
            item_text = re.sub(r'^\d+\.', '', stripped).strip()
            current_content.append({
                "type": "list",
                "items": [item_text],
                "ordered": True
            })
            i += 1
            continue

        # 普通段落
        if stripped:
            # 清理 Markdown 格式标记（粗体、斜体等）
            cleaned = stripped
            cleaned = re.sub(r'\*\*\*([^*]+)\*\*\*', r'\1', cleaned)
            cleaned = re.sub(r'\*\*([^*]+)\*\*', r'\1', cleaned)
            cleaned = re.sub(r'\*([^*]+)\*', r'\1', cleaned)
            cleaned = re.sub(r'`([^`]+)`', r'\1', cleaned)
            current_content.append({"type": "text", "text": cleaned})

        i += 1

    flush_table()
    flush_section()

    return sections


def build_sections_for_generator(sections):
    """
    将解析后的 sections 转换为 QuickDocument 可用的格式
    合并连续的列表项
    """
    result = []
    for sec in sections:
        new_sec = {
            "level": sec["level"],
            "title": sec["title"],
            "content": []
        }

        i = 0
        content = sec.get("content", [])
        while i < len(content):
            item = content[i]

            # 合并连续的同类型列表
            if item.get("type") == "list":
                merged_items = item["items"][:]
                j = i + 1
                while j < len(content) and content[j].get("type") == "list" and content[j].get("ordered") == item.get("ordered"):
                    merged_items.extend(content[j]["items"])
                    j += 1
                new_sec["content"].append({
                    "type": "list",
                    "items": merged_items,
                    "ordered": item.get("ordered", False)
                })
                i = j
                continue

            # 处理 heading3 样式标记
            if item.get("type") == "text" and item.get("style") == "heading3":
                # 作为二级标题下的强调段落
                new_sec["content"].append({
                    "type": "text",
                    "text": item["text"],
                    "bold": True
                })
                i += 1
                continue

            new_sec["content"].append(item)
            i += 1

        result.append(new_sec)

    return result


def main():
    md_path = Path("样例数据.md")
    output_path = "大学物理-力学部分_复习指南.docx"

    if not md_path.exists():
        print(f"[错误] 找不到文件: {md_path}")
        print("请确保 样例数据.md 与脚本在同一目录下。")
        return

    print(f"[信息] 正在读取: {md_path}")
    with open(md_path, 'r', encoding='utf-8') as f:
        md_text = f.read()

    print("[信息] 正在解析 Markdown 结构...")
    raw_sections = parse_markdown_sections(md_text)
    sections = build_sections_for_generator(raw_sections)

    print(f"[信息] 解析完成，共 {len(sections)} 个章节")

    print("[信息] 正在生成 Word 文档...")
    doc = QuickDocument(
        title="大学物理-力学部分 复习指南",
        author="AI 学习助手",
        organization="期末突击小组"
    )

    doc.generate_full_document(
        sections=sections,
        output_path=output_path,
        include_cover=True,
        include_toc=True,
        header_text="大学物理-力学部分 复习指南",
        footer_page_number=True
    )

    abs_path = os.path.abspath(output_path)
    print(f"\n✅ 样例文档生成完成: {abs_path}")
    print("\n📋 使用说明：")
    print("1. 用 Microsoft Word 或 WPS 打开文档")
    print("2. 右键目录区域选择「更新域」→「更新整个目录」")
    print("3. 页码显示为「1」时，选中页脚按 F9 更新域")


if __name__ == "__main__":
    main()
