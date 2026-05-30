#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据完整性验证脚本
用途：在运行分析前检查 CiteSpace 输入数据的质量和完整性
输入：wos_cleaned_for_citespace.txt
输出：数据质量报告
"""

import re
import os
from collections import Counter

INPUT_FILE = "../data/processed/wos_cleaned_for_citespace.txt"

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

def check_field_completeness(records, field_tag, field_name):
    """检查指定字段的完整性"""
    total = len(records)
    present = 0
    empty = 0

    for record in records:
        match = re.search(rf'\n{re.escape(field_tag)}\s+\\S', record)
        if match:
            present += 1
        else:
            empty += 1

    completeness = present / total * 100 if total > 0 else 0
    return {
        'field': field_name,
        'tag': field_tag,
        'total': total,
        'present': present,
        'empty': empty,
        'completeness': completeness
    }

def check_doi_uniqueness(records):
    """检查 DOI 唯一性"""
    dois = []
    duplicates = []

    for record in records:
        match = re.search(r'\nDI\s+(\S+)', record)
        if match:
            doi = match.group(1).strip().lower()
            if doi in dois:
                duplicates.append(doi)
            else:
                dois.append(doi)

    return {
        'total_dois': len(dois),
        'duplicate_dois': len(duplicates),
        'unique_dois': len(set(dois))
    }

def check_year_distribution(records):
    """检查年份分布"""
    years = []
    for record in records:
        match = re.search(r'\nPY\s+(\d{4})', record)
        if match:
            years.append(int(match.group(1)))

    year_counter = Counter(years)
    return dict(sorted(year_counter.items()))

def check_document_types(records):
    """检查文献类型分布"""
    types = []
    for record in records:
        match = re.search(r'\nDT\s+(.*?)(?=\n[A-Z]{2}\s|ER)', record, re.DOTALL)
        if match:
            dt = match.group(1).replace('\n   ', ' ').strip()
            types.append(dt)

    return Counter(types)

def main():
    print("=" * 60)
    print("数据完整性验证报告")
    print("=" * 60)

    if not os.path.exists(INPUT_FILE):
        print(f"错误: 找不到输入文件 {INPUT_FILE}")
        return

    records = parse_wos_records(INPUT_FILE)
    print(f"总记录数: {len(records)}\n")

    # 1. 关键字段完整性检查
    print("【字段完整性检查】")
    print("-" * 60)

    fields_to_check = [
        ('TI', '标题 (Title)'),
        ('AU', '作者 (Author)'),
        ('PY', '出版年 (Year)'),
        ('DI', 'DOI'),
        ('DE', '作者关键词 (Author Keywords)'),
        ('ID', 'Keywords Plus'),
        ('AB', '摘要 (Abstract)'),
        ('C1', '机构地址 (Affiliation)'),
        ('CR', '参考文献 (References)'),
        ('TC', '被引频次 (Times Cited)'),
    ]

    for tag, name in fields_to_check:
        result = check_field_completeness(records, tag, name)
        status = "✓" if result['completeness'] >= 95 else "⚠" if result['completeness'] >= 80 else "✗"
        print(f"{status} {name:<30} {result['present']}/{result['total']} ({result['completeness']:.1f}%)")

    # 2. DOI 唯一性检查
    print("\n【DOI 唯一性检查】")
    print("-" * 60)
    doi_info = check_doi_uniqueness(records)
    print(f"总 DOI 数: {doi_info['total_dois']}")
    print(f"唯一 DOI 数: {doi_info['unique_dois']}")
    print(f"重复 DOI 数: {doi_info['duplicate_dois']}")
    if doi_info['duplicate_dois'] > 0:
        print("⚠ 警告: 发现重复 DOI，建议检查去重效果")
    else:
        print("✓ DOI 唯一性检查通过")

    # 3. 年份分布检查
    print("\n【年份分布检查】")
    print("-" * 60)
    year_dist = check_year_distribution(records)
    print(f"{'年份':<10}{'数量':<10}{'占比':<10}")
    print("-" * 30)
    total = len(records)
    for year, count in year_dist.items():
        pct = count / total * 100
        marker = "✓" if 2020 <= year <= 2026 else "✗ 超出范围"
        print(f"{year:<10}{count:<10}{pct:.1f}% {marker}")

    # 检查是否有超出范围的年份
    out_of_range = [y for y in year_dist.keys() if y < 2020 or y > 2026]
    if out_of_range:
        print(f"\n⚠ 警告: 发现 {len(out_of_range)} 个超出范围的年份: {out_of_range}")

    # 4. 文献类型检查
    print("\n【文献类型分布】")
    print("-" * 60)
    doc_types = check_document_types(records)
    for dtype, count in doc_types.most_common():
        pct = count / len(records) * 100
        print(f"{dtype:<30} {count:<10} ({pct:.1f}%)")

    # 5. 综合评估
    print("\n【综合评估】")
    print("=" * 60)

    issues = []

    # 检查关键字段
    ti_check = check_field_completeness(records, 'TI', 'Title')
    if ti_check['completeness'] < 100:
        issues.append(f"标题缺失: {ti_check['empty']} 条")

    au_check = check_field_completeness(records, 'AU', 'Author')
    if au_check['completeness'] < 100:
        issues.append(f"作者缺失: {au_check['empty']} 条")

    py_check = check_field_completeness(records, 'PY', 'Year')
    if py_check['completeness'] < 100:
        issues.append(f"年份缺失: {py_check['empty']} 条")

    if doi_info['duplicate_dois'] > 0:
        issues.append(f"DOI 重复: {doi_info['duplicate_dois']} 条")

    if issues:
        print("发现以下问题:")
        for issue in issues:
            print(f"  ⚠ {issue}")
        print("\n建议: 请检查数据清洗步骤，确保去重和字段提取正确")
    else:
        print("✓ 数据完整性检查通过，可以进行后续分析")

    print("=" * 60)

if __name__ == "__main__":
    main()
