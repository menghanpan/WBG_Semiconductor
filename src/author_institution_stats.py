#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
核心作者与机构统计脚本
用途：从 CiteSpace 输入数据中提取高频作者和机构
输入：CiteSpace 可识别的 WoS 纯文本格式 (.txt)
输出：top_authors.csv + top_institutions.csv
"""

import re
import os
import csv
from collections import Counter

INPUT_FILE = "../data/processed/wos_cleaned_for_citespace.txt"
OUTPUT_DIR = "../results/statistics"
TOP_N = 20  # 统计前 N 个

def parse_wos_records(filepath):
    """解析 WoS 记录"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    records = []
    raw_records = re.split(r'(?=\nPT\s)', content)
    for raw in raw_records:
        raw = raw.strip()
        if raw.startswith('PT ') and 'ER' in raw:
            records.append(raw)
    return records

def extract_authors(record):
    """提取作者列表 (AU 字段)"""
    au_match = re.search(r'\nAU\s+(.*?)(?=\n[A-Z]{2}\s|ER)', record, re.DOTALL)
    if au_match:
        au_text = au_match.group(1).replace('\n   ', ' ')
        authors = [a.strip() for a in au_text.split('\n') if a.strip()]
        # 处理同一行多个作者（用 ; 分隔的情况）
        result = []
        for a in authors:
            result.extend([x.strip() for x in a.split(';') if x.strip()])
        return result
    return []

def extract_institutions(record):
    """提取机构 (C1 字段)"""
    c1_match = re.search(r'\nC1\s+(.*?)(?=\n[A-Z]{2}\s|ER)', record, re.DOTALL)
    if c1_match:
        c1_text = c1_match.group(1).replace('\n   ', ' ')
        # 提取机构名（去除 [作者名] 前缀）
        institutions = []
        for line in c1_text.split(';'):
            # 去除 [Zhang, J] 这类前缀
            line = re.sub(r'\[.*?\]\s*', '', line).strip()
            if line:
                # 提取主要机构名（取第一个逗号前的部分）
                inst = line.split(',')[0].strip()
                institutions.append(inst)
        return institutions
    return []

def standardize_author(author):
    """标准化作者名格式"""
    author = author.strip()
    # 确保逗号后有空格: "Zhang, J" -> "Zhang, J"
    author = re.sub(r',\s*', ', ', author)
    return author

def main():
    print("=" * 60)
    print("核心作者与机构统计")
    print("=" * 60)

    if not os.path.exists(INPUT_FILE):
        print(f"错误: 找不到输入文件 {INPUT_FILE}")
        return

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    records = parse_wos_records(INPUT_FILE)
    print(f"读取到 {len(records)} 条记录\n")

    # 统计作者
    author_counter = Counter()
    institution_counter = Counter()

    for record in records:
        authors = extract_authors(record)
        for author in authors:
            author = standardize_author(author)
            if author and len(author) > 2:
                author_counter[author] += 1

        institutions = extract_institutions(record)
        for inst in institutions:
            if inst and len(inst) > 3:
                institution_counter[inst] += 1

    # 输出作者统计
    print(f"Top {TOP_N} 核心作者:")
    print("-" * 50)
    print(f"{'排名':<6}{'作者':<30}{'发文量':<8}")
    print("-" * 50)

    top_authors = author_counter.most_common(TOP_N)
    author_stats = []
    for rank, (author, count) in enumerate(top_authors, 1):
        print(f"{rank:<6}{author:<30}{count:<8}")
        author_stats.append({
            'Rank': rank,
            'Author': author,
            'Publications': count
        })

    # 保存作者统计
    author_csv = os.path.join(OUTPUT_DIR, "top_authors.csv")
    with open(author_csv, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['Rank', 'Author', 'Publications'])
        writer.writeheader()
        writer.writerows(author_stats)

    print(f"\n作者统计已保存: {author_csv}\n")

    # 输出机构统计
    print(f"Top {TOP_N} 核心机构:")
    print("-" * 60)
    print(f"{'排名':<6}{'机构':<45}{'发文量':<8}")
    print("-" * 60)

    top_institutions = institution_counter.most_common(TOP_N)
    inst_stats = []
    for rank, (inst, count) in enumerate(top_institutions, 1):
        # 截断过长的机构名
        inst_display = inst[:42] + "..." if len(inst) > 45 else inst
        print(f"{rank:<6}{inst_display:<45}{count:<8}")
        inst_stats.append({
            'Rank': rank,
            'Institution': inst,
            'Publications': count
        })

    # 保存机构统计
    inst_csv = os.path.join(OUTPUT_DIR, "top_institutions.csv")
    with open(inst_csv, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['Rank', 'Institution', 'Publications'])
        writer.writeheader()
        writer.writerows(inst_stats)

    print(f"\n机构统计已保存: {inst_csv}")
    print("=" * 60)

if __name__ == "__main__":
    main()
