#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
突现词检测辅助脚本
用途：从 CiteSpace 导出的突现词数据中提取关键信息，生成标准化表格
输入：CiteSpace Burst Detection 结果（手动复制或导出的文本）
输出：burst_keywords.csv（含突现强度、起始/结束年份、持续时间）
"""

import os
import csv
import re
from collections import namedtuple

OUTPUT_DIR = "../results/statistics"

BurstRecord = namedtuple('BurstRecord', [
    'Keyword', 'Year', 'Strength', 'Begin', 'End', 'Duration', 'Status'
])

def parse_burst_text(text):
    """
    解析 CiteSpace 突现检测结果文本
    CiteSpace 突现检测结果格式示例：
    Keywords    Year    Strength    Begin    End    1990-2026
    keyword1    2015    5.21        2018     2020   ▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃
    """
    bursts = []
    lines = text.strip().split('\n')

    # 跳过表头
    for line in lines[1:]:
        line = line.strip()
        if not line:
            continue

        # 使用正则匹配各列
        # 格式: keyword  year  strength  begin  end  timeline
        parts = re.split(r'\s{2,}', line)

        if len(parts) >= 5:
            try:
                keyword = parts[0].strip()
                year = int(parts[1])
                strength = float(parts[2])
                begin = int(parts[3])
                end = int(parts[4])
                duration = end - begin + 1

                # 判断状态：2026年是否仍在突现
                status = "Active" if end >= 2026 else "Ended"

                bursts.append(BurstRecord(
                    Keyword=keyword,
                    Year=year,
                    Strength=strength,
                    Begin=begin,
                    End=end,
                    Duration=duration,
                    Status=status
                ))
            except (ValueError, IndexError):
                continue

    return bursts

def save_burst_table(bursts, output_file):
    """保存突现词表格"""
    fieldnames = ['Rank', 'Keyword', 'Strength', 'Begin', 'End', 'Duration', 'Status']

    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()

        for rank, burst in enumerate(bursts, 1):
            writer.writerow({
                'Rank': rank,
                'Keyword': burst.Keyword,
                'Strength': burst.Strength,
                'Begin': burst.Begin,
                'End': burst.End,
                'Duration': burst.Duration,
                'Status': burst.Status
            })

    print(f"突现词表格已保存: {output_file}")

def generate_burst_report(bursts):
    """生成突现词分析报告"""
    if not bursts:
        print("没有突现词数据")
        return

    print("\n" + "="*60)
    print("突现词分析报告")
    print("="*60)

    # 基本统计
    total = len(bursts)
    active = sum(1 for b in bursts if b.Status == "Active")
    ended = total - active

    print(f"\n总突现词数量: {total}")
    print(f"当前仍在突现: {active}")
    print(f"已结束突现: {ended}")

    # 按强度排序
    sorted_by_strength = sorted(bursts, key=lambda x: x.Strength, reverse=True)

    print(f"\n突现强度 Top 10:")
    print("-"*60)
    print(f"{'排名':<6}{'关键词':<25}{'强度':<10}{'起止年份':<15}{'状态':<10}")
    print("-"*60)

    for i, burst in enumerate(sorted_by_strength[:10], 1):
        period = f"{burst.Begin}-{burst.End}"
        print(f"{i:<6}{burst.Keyword:<25}{burst.Strength:<10.2f}{period:<15}{burst.Status:<10}")

    # 持续中的突现词
    active_bursts = [b for b in bursts if b.Status == "Active"]
    if active_bursts:
        print(f"\n当前持续中的突现词 ({len(active_bursts)}个):")
        print("-"*60)
        for burst in sorted(active_bursts, key=lambda x: x.Strength, reverse=True):
            print(f"  • {burst.Keyword} (强度: {burst.Strength:.2f}, 始于: {burst.Begin})")

    # 时间分布
    begin_years = [b.Begin for b in bursts]
    from collections import Counter
    year_dist = Counter(begin_years)

    print(f"\n突现起始年份分布:")
    for year in sorted(year_dist.keys()):
        print(f"  {year}: {year_dist[year]} 个")

    print("\n" + "="*60)

def create_burst_template():
    """创建突现词数据录入模板"""
    template_text = r"""
# CiteSpace 突现词数据录入模板
# 使用说明：
# 1. 在 CiteSpace 中完成 Burst Detection 后，点击 "Export" 导出数据
# 2. 或从 CiteSpace 界面手动复制突现词表格
# 3. 将数据粘贴到下方（替换此模板内容）
# 4. 运行 burst_detection.py 解析

# 数据格式（制表符分隔）：
# Keywords    Year    Strength    Begin    End    Timeline
# 示例：
# gan hemt    2020    8.52        2022     2026   ▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃
# sic mosfet  2020    7.31        2021     2025   ▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃

# 请将实际数据粘贴在此处：

"""

    template_file = os.path.join(OUTPUT_DIR, "burst_data_template.txt")
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    with open(template_file, 'w', encoding='utf-8') as f:
        f.write(template_text)

    print(f"突现词数据模板已创建: {template_file}")
    print("请将 CiteSpace 导出的突现词数据粘贴到该文件中，然后运行本脚本")

def main():
    print("="*60)
    print("CiteSpace 突现词检测辅助工具")
    print("="*60)

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # 检查是否有数据文件
    burst_data_file = os.path.join(OUTPUT_DIR, "burst_data.txt")

    if not os.path.exists(burst_data_file):
        print(f"\n未找到突现词数据文件: {burst_data_file}")
        print("正在创建数据录入模板...")
        create_burst_template()

        print("\n下一步操作:")
        print("1. 在 CiteSpace 中完成 Burst Detection 分析")
        print("2. 导出或复制突现词数据")
        print("3. 将数据粘贴到 burst_data_template.txt 中")
        print("4. 重命名为 burst_data.txt")
        print("5. 重新运行本脚本")
        return

    # 解析数据
    with open(burst_data_file, 'r', encoding='utf-8') as f:
        text = f.read()

    bursts = parse_burst_text(text)

    if bursts:
        # 生成报告
        generate_burst_report(bursts)

        # 保存表格
        output_file = os.path.join(OUTPUT_DIR, "burst_keywords.csv")
        save_burst_table(bursts, output_file)

        # 单独保存当前活跃突现词
        active_bursts = [b for b in bursts if b.Status == "Active"]
        if active_bursts:
            active_file = os.path.join(OUTPUT_DIR, "burst_active_keywords.csv")
            save_burst_table(active_bursts, active_file)
            print(f"当前活跃突现词已保存: {active_file}")
    else:
        print("未能解析到突现词数据，请检查数据格式")

    print("\n" + "="*60)

if __name__ == "__main__":
    main()
