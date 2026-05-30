#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
高频关键词统计脚本
用途：从 CiteSpace 输入数据中提取作者关键词和 Keywords Plus，统计高频词
输入：CiteSpace 可识别的 WoS 纯文本格式 (.txt)
输出：top_keywords.csv + 词频统计报告
"""

import re
import os
import csv
from collections import Counter

INPUT_FILE = "../data/processed/wos_cleaned_for_citespace.txt"
OUTPUT_CSV = "../results/statistics/top_keywords.csv"
OUTPUT_DIR = "../results/statistics"
TOP_N = 50  # 统计前 N 个高频词

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

def extract_keywords(record):
    """提取 DE (Author Keywords) 和 ID (Keywords Plus)"""
    keywords = []

    # Author Keywords (DE)
    de_match = re.search(r'\nDE\s+(.*?)(?=\n[A-Z]{2}\s|ER)', record, re.DOTALL)
    if de_match:
        de_text = de_match.group(1).replace('\n   ', ' ')
        keywords.extend([k.strip().lower() for k in de_text.split(';') if k.strip()])

    # Keywords Plus (ID)
    id_match = re.search(r'\nID\s+(.*?)(?=\n[A-Z]{2}\s|ER)', record, re.DOTALL)
    if id_match:
        id_text = id_match.group(1).replace('\n   ', ' ')
        keywords.extend([k.strip().lower() for k in id_text.split(';') if k.strip()])

    return keywords

def standardize_keyword(keyword):
    """标准化关键词格式"""
    keyword = keyword.strip()
    # 统一连字符
    keyword = keyword.replace(' - ', '-')
    # 去除多余空格
    keyword = ' '.join(keyword.split())
    return keyword

def main():
    print("=" * 60)
    print("高频关键词统计")
    print("=" * 60)

    if not os.path.exists(INPUT_FILE):
        print(f"错误: 找不到输入文件 {INPUT_FILE}")
        return

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    records = parse_wos_records(INPUT_FILE)
    print(f"读取到 {len(records)} 条记录\n")

    # 统计关键词
    keyword_counter = Counter()
    records_with_keywords = 0

    for record in records:
        keywords = extract_keywords(record)
        if keywords:
            records_with_keywords += 1
        for kw in keywords:
            kw = standardize_keyword(kw)
            if kw and len(kw) > 1:  # 过滤单字符
                keyword_counter[kw] += 1

    print(f"含关键词的记录: {records_with_keywords}/{len(records)}")
    print(f"去重前关键词总数: {sum(keyword_counter.values())}")
    print(f"去重后关键词种类: {len(keyword_counter)}\n")

    # 输出 Top N
    print(f"Top {TOP_N} 高频关键词:")
    print("-" * 50)
    print(f"{'排名':<6}{'关键词':<35}{'频次':<8}{'占比':<8}")
    print("-" * 50)

    top_keywords = keyword_counter.most_common(TOP_N)
    total_kw = sum(keyword_counter.values())
    stats = []

    for rank, (kw, count) in enumerate(top_keywords, 1):
        pct = count / total_kw * 100
        print(f"{rank:<6}{kw:<35}{count:<8}{pct:.2f}%")
        stats.append({
            'Rank': rank,
            'Keyword': kw,
            'Frequency': count,
            'Percentage': f"{pct:.2f}%"
        })

    # 保存 CSV
    with open(OUTPUT_CSV, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['Rank', 'Keyword', 'Frequency', 'Percentage'])
        writer.writeheader()
        writer.writerows(stats)

    print("-" * 50)
    print(f"\n结果已保存: {OUTPUT_CSV}")
    print("=" * 60)

if __name__ == "__main__":
    main()
