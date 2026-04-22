"""
本地调试测试脚本 - 测试文件解析和分块功能
用法: python test_pipeline.py <文件路径>
"""

import argparse
import os
import sys
import traceback

from 文件预处理 import DocumentProcessor


class FileNotFoundErrorCustom(Exception):
    """自定义文件不存在异常"""
    pass


class UnsupportedFormatError(Exception):
    """自定义格式不支持异常"""
    pass


def main():
    parser = argparse.ArgumentParser(
        description="测试文档预处理管道的本地脚本",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="示例: python test_pipeline.py ./example.docx"
    )
    parser.add_argument(
        "file_path",
        type=str,
        help="待测试的文件路径（支持 PDF、DOCX、TXT、MD、HTML、PPTX、XLSX）"
    )
    parser.add_argument(
        "--chunk-size",
        type=int,
        default=800,
        help="分块大小（默认 800）"
    )
    parser.add_argument(
        "--chunk-overlap",
        type=int,
        default=100,
        help="块间重叠大小（默认 100）"
    )

    args = parser.parse_args()

    file_path = args.file_path

    # 检查文件是否存在
    if not os.path.exists(file_path):
        print(f"[错误] 文件不存在: {file_path}")
        print("请检查路径是否正确，或提供绝对路径。")
        sys.exit(1)

    # 检查是否为文件
    if not os.path.isfile(file_path):
        print(f"[错误] 指定路径不是文件: {file_path}")
        sys.exit(1)

    # 检查文件扩展名
    supported_exts = ('.pdf', '.docx', '.txt', '.md', '.markdown', '.html', '.htm', '.pptx', '.xlsx', '.xls')
    _, ext = os.path.splitext(file_path.lower())
    if ext not in supported_exts:
        print(f"[错误] 不支持的文件格式: {ext}")
        print(f"当前支持的格式: {', '.join(supported_exts)}")
        sys.exit(1)

    print(f"[信息] 开始处理文件: {file_path}")
    print(f"[信息] 分块参数: chunk_size={args.chunk_size}, chunk_overlap={args.chunk_overlap}")
    print("-" * 50)

    try:
        processor = DocumentProcessor(
            chunk_size=args.chunk_size,
            chunk_overlap=args.chunk_overlap,
            extract_images=False
        )

        result = processor.process(file_path)

        print(f"[成功] 文档处理完成！")
        print(f"  - 文件名: {result.source_file}")
        print(f"  - 文件类型: {result.file_type}")
        print(f"  - 总页数: {result.total_pages}")
        print(f"  - 总块数: {result.total_chunks}")
        print()

        # 打印摘要统计
        if result.summary:
            print("[摘要统计]")
            print(f"  - 总字数: {result.summary.get('total_words', 0)}")
            print(f"  - 总字符数: {result.summary.get('total_chars', 0)}")
            print(f"  - 平均块长度: {result.summary.get('avg_chunk_length', 0):.1f}")
            print(f"  - 关键词: {', '.join(result.summary.get('top_keywords', [])[:5])}")
            print()

        # 打印第一个 chunk 的详情
        if result.chunks:
            first_chunk = result.chunks[0]
            print("[第一个 Chunk 详情]")
            print(f"  - ID: {first_chunk.id}")
            print(f"  - 类型: {first_chunk.type}")
            print(f"  - 页码: {first_chunk.page_num or 'N/A'}")
            print(f"  - 章节标题: {first_chunk.section_title or '未命名段落'}")
            print(f"  - 字数: {first_chunk.word_count}")
            print(f"  - 字符数: {first_chunk.char_count}")
            print()
            print("[内容预览 - 前500字符]")
            preview = first_chunk.content[:500]
            if len(first_chunk.content) > 500:
                preview += "..."
            print(preview)
            print()

        # 打印块类型分布
        if result.summary and 'chunk_types' in result.summary:
            print("[块类型分布]")
            for ctype, count in result.summary['chunk_types'].items():
                print(f"  - {ctype}: {count} 个")
            print()

        print("-" * 50)
        print("[信息] 测试通过，文件解析和分块功能正常。")

    except ImportError as e:
        print(f"[错误] 缺少必要的依赖库: {e}")
        print("请根据文件类型安装对应的依赖:")
        print("  PDF  -> pip install PyMuPDF")
        print("  DOCX -> pip install python-docx")
        print("  PPTX -> pip install python-pptx")
        print("  XLSX -> pip install openpyxl")
        print("  HTML -> pip install beautifulsoup4 lxml")
        print("  MD   -> pip install markdown")
        sys.exit(1)

    except Exception as e:
        print(f"[错误] 处理过程中发生异常: {type(e).__name__}: {e}")
        print()
        print("[详细堆栈]")
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
