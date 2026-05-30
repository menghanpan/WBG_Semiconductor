#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
时间线图数据提取脚本
用途：从 CiteSpace 时间线视图导出的数据中提取关键信息
输入：CiteSpace Timeline View 导出的聚类数据
输出：各聚类的时间分布表和演化趋势分析
"""

import os
import csv
from collections import defaultdict

OUTPUT_DIR = "../results/statistics"

def parse_timeline_data(cluster_file):
    """
    解析 CiteSpace 时间线数据
    格式：Cluster ID, Size, Silhouette, Mean Year, Top Terms, Timeline Data
    """
    clusters = []

    with open(cluster_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            cluster = {
                'Cluster_ID': row.get('Cluster ID', ''),
                'Size': int(row.get('Size', 0)),
                'Silhouette': float(row.get('Silhouette', 0)),
                'Mean_Year': float(row.get('Mean Year', 0)),
                'Top_Terms': row.get('Top Terms (by LLR)', ''),
                'Label': row.get('Label (LLR)', ''),
                'Timeline': row.get('Timeline', '')
            }
            clusters.append(cluster)

    return clusters

def analyze_cluster_evolution(clusters):
    """分析聚类演化趋势"""
    # 按平均年份排序
    sorted_clusters = sorted(clusters, key=lambda x: x['Mean_Year'])

    # 划分阶段
    stages = {
        '早期 (2020-2021)': [],
        '发展期 (2022-2023)': [],
        '近期 (2024-2026)': []
    }

    for cluster in sorted_clusters:
        year = cluster['Mean_Year']
        if year <= 2021.5:
            stages['早期 (2020-2021)'].append(cluster)
        elif year <= 2023.5:
            stages['发展期 (2022-2023)'].append(cluster)
        else:
            stages['近期 (2024-2026)'].append(cluster)

    return stages

def generate_evolution_report(clusters, stages):
    """生成演化分析报告"""
    print("\n" + "=" * 70)
    print("关键词聚类时间演化分析")
    print("=" * 70)

    # 整体概况
    print(f"\n【聚类概况】")
    print(f"  聚类总数: {len(clusters)}")
    print(f"  平均轮廓值: {sum(c['Silhouette'] for c in clusters) / len(clusters):.3f}")
    print(f"  平均年份范围: {min(c['Mean_Year'] for c in clusters):.1f} - {max(c['Mean_Year'] for c in clusters):.1f}")

    # 各阶段分析
    print(f"\n【分阶段分析】")
    for stage_name, stage_clusters in stages.items():
        if stage_clusters:
            print(f"\n  {stage_name}: {len(stage_clusters)} 个聚类")
            for c in stage_clusters:
                print(f"    • #{c['Cluster_ID']}: {c['Label'][:40]}...")
                print(f"      规模: {c['Size']}, 轮廓值: {c['Silhouette']:.3f}, 平均年份: {c['Mean_Year']:.1f}")

    # 聚类质量评估
    print(f"\n【聚类质量评估】")
    high_quality = [c for c in clusters if c['Silhouette'] >= 0.7]
    medium_quality = [c for c in clusters if 0.5 <= c['Silhouette'] < 0.7]
    low_quality = [c for c in clusters if c['Silhouette'] < 0.5]

    print(f"  高质量聚类 (S≥0.7): {len(high_quality)} 个")
    print(f"  中等质量聚类 (0.5≤S<0.7): {len(medium_quality)} 个")
    print(f"  低质量聚类 (S<0.5): {len(low_quality)} 个")

    # 主题演化路径
    print(f"\n【主题演化路径】")
    sorted_by_year = sorted(clusters, key=lambda x: x['Mean_Year'])
    print("  按时间顺序的主要研究主题:")
    for i, c in enumerate(sorted_by_year, 1):
        print(f"    {i}. {c['Mean_Year']:.0f}: {c['Label'][:50]}")

def save_timeline_csv(clusters, output_file):
    """保存时间线数据"""
    fieldnames = [
        'Cluster_ID', 'Label', 'Size', 'Silhouette',
        'Mean_Year', 'Stage', 'Top_Terms'
    ]

    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()

        for c in clusters:
            # 确定阶段
            year = c['Mean_Year']
            if year <= 2021.5:
                stage = '早期'
            elif year <= 2023.5:
                stage = '发展期'
            else:
                stage = '近期'

            writer.writerow({
                'Cluster_ID': c['Cluster_ID'],
                'Label': c['Label'],
                'Size': c['Size'],
                'Silhouette': c['Silhouette'],
                'Mean_Year': c['Mean_Year'],
                'Stage': stage,
                'Top_Terms': c['Top_Terms']
            })

    print(f"\n时间线数据已保存: {output_file}")

def main():
    print("=" * 70)
    print("CiteSpace 时间线数据提取工具")
    print("=" * 70)

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    cluster_file = "../results/citespace_export/timeline_clusters.csv"

    if not os.path.exists(cluster_file):
        print(f"\n错误: 找不到时间线数据文件 {cluster_file}")
        print("请先从 CiteSpace 导出时间线数据:")
        print("  1. 在 Timeline View 中")
        print("  2. 点击 Cluster Explorer")
        print("  3. 导出聚类汇总表为 CSV")
        return

    # 解析数据
    print("\n正在解析时间线数据...")
    clusters = parse_timeline_data(cluster_file)
    print(f"读取到 {len(clusters)} 个聚类")

    # 分析演化
    stages = analyze_cluster_evolution(clusters)

    # 生成报告
    generate_evolution_report(clusters, stages)

    # 保存数据
    output_file = os.path.join(OUTPUT_DIR, "timeline_analysis.csv")
    save_timeline_csv(clusters, output_file)

    print("\n" + "=" * 70)

if __name__ == "__main__":
    main()
