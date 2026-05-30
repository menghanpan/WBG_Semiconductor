#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
WoS 多文件合并脚本
用途：将分批次导出的 Web of Science 纯文本文件合并为单一文件
输入：多个 savedrecs_X.txt 文件
输出：wos_raw_merged.txt（CiteSpace 可识别格式）
"""

import os
import glob
import re

# 配置
INPUT_DIR = "../data/raw"          # 存放分批导出文件的目录
OUTPUT_FILE = "../data/processed/wos_raw_merged.txt"
FILE_PATTERN = "savedrecs_*.txt"   # 文件匹配模式

def get_sorted_files(directory, pattern):
    """获取按序号排序的文件列表"""
    files = glob.glob(os.path.join(directory, pattern))

    # 按文件名中的数字排序
    def extract_number(filepath):
        basename = os.path.basename(filepath)
        match = re.search(r'(\d+)', basename)
        return int(match.group(1)) if match else 0

    return sorted(files, key=extract_number)

def merge_wos_files(files, output_path):
    """
    合并 WoS 文件
    注意：每个文件末尾有 EF（End of File），合并时只保留最后一个
    """
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    total_records = 0

    with open(output_path, 'w', encoding='utf-8') as outfile:
        for i, filepath in enumerate(files):
            filename = os.path.basename(filepath)
            print(f"正在处理: {filename}")

            with open(filepath, 'r', encoding='utf-8') as infile:
                content = infile.read()

            # 统计记录数（通过 PT 字段计数）
            records_in_file = content.count('\nPT ')
            total_records += records_in_file

            # 去除文件末尾的 EF 标记（除了最后一个文件）
            if i < len(files) - 1:
                content = content.rstrip()
                if content.endswith('EF'):
                    content = content[:-2].rstrip()

            outfile.write(content)
            if not content.endswith('\n'):
                outfile.write('\n')

        # 确保文件以 EF 结尾
        outfile.write('EF\n')

    return total_records

def validate_merged_file(filepath):
    """验证合并后的文件"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 检查基本格式
    pt_count = content.count('\nPT ')
    er_count = content.count('\nER\n')
    has_ef = content.strip().endswith('EF')

    print(f"\n文件验证结果:")
    print(f"  PT 标记数: {pt_count}")
    print(f"  ER 标记数: {er_count}")
    print(f"  以 EF 结尾: {'是' if has_ef else '否'}")

    if pt_count == er_count and has_ef:
        print(f"  状态: ✓ 文件格式正确")
        return True
    else:
        print(f"  状态: ⚠ 文件格式可能有问题")
        if pt_count != er_count:
            print(f"    警告: PT ({pt_count}) 和 ER ({er_count}) 数量不匹配")
        if not has_ef:
            print(f"    警告: 文件未以 EF 结尾")
        return False

def main():
    print("=" * 60)
    print("Web of Science 数据文件合并工具")
    print("=" * 60)

    # 查找文件
    files = get_sorted_files(INPUT_DIR, FILE_PATTERN)

    if not files:
        print(f"\n错误: 在 {INPUT_DIR} 中找不到匹配 {FILE_PATTERN} 的文件")
        print("请将分批次导出的 savedrecs_1.txt, savedrecs_2.txt 等文件放入该目录")
        return

    print(f"\n找到 {len(files)} 个文件:")
    for f in files:
        size = os.path.getsize(f)
        print(f"  • {os.path.basename(f)} ({size:,} bytes)")

    # 合并文件
    print(f"\n正在合并到: {OUTPUT_FILE}")
    total_records = merge_wos_files(files, OUTPUT_FILE)

    # 验证
    print(f"\n合并完成!")
    print(f"  总记录数: {total_records}")
    print(f"  输出文件: {OUTPUT_FILE}")
    print(f"  文件大小: {os.path.getsize(OUTPUT_FILE):,} bytes")

    validate_merged_file(OUTPUT_FILE)

    print("\n" + "=" * 60)
    print("下一步: 运行 data_validation.py 检查数据完整性")
    print("=" * 60)

if __name__ == "__main__":
    main()
