#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CiteSpace 结果后处理脚本
用途：解析 CiteSpace 导出的网络数据（.csv / .xls），生成标准化统计表格
输入：CiteSpace 导出的节点/连线数据
输出：标准化的统计表格（Top 节点、网络指标汇总等）
"""

import os
import csv
import pandas as pd
from collections import defaultdict

# 配置路径
CITESPACE_OUTPUT_DIR = "../results/citespace_export"  # CiteSpace 导出数据目录
OUTPUT_DIR = "../results/statistics"

def parse_citespace_nodes(filepath):
    """
    解析 CiteSpace 导出的节点数据
    CiteSpace 导出格式通常为 CSV，包含：
    Id, Label, Weight, Color, ...
    """
    nodes = []
    with open(filepath, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            nodes.append(row)
    return nodes

def parse_citespace_edges(filepath):
    """
    解析 CiteSpace 导出的连线数据
    """
    edges = []
    with open(filepath, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            edges.append(row)
    return edges

def extract_top_nodes(nodes, key='Weight', top_n=10):
    """提取 Top N 节点"""
    # 按指定字段排序
    sorted_nodes = sorted(nodes, key=lambda x: float(x.get(key, 0)), reverse=True)
    return sorted_nodes[:top_n]

def generate_network_summary(nodes, edges):
    """生成网络指标汇总"""
    summary = {
        '节点总数': len(nodes),
        '连线总数': len(edges),
        '网络密度': len(edges) / (len(nodes) * (len(nodes) - 1)) if len(nodes) > 1 else 0,
    }
    return summary

def process_keyword_clusters(cluster_file):
    """
    处理关键词聚类结果
    输入：CiteSpace 聚类汇总表（从 Cluster Explorer 导出）
    """
    clusters = []
    with open(cluster_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            clusters.append({
                'Cluster_ID': row.get('Cluster ID', ''),
                'Size': row.get('Size', ''),
                'Silhouette': row.get('Silhouette', ''),
                'Mean_Year': row.get('Mean Year', ''),
                'Top_Terms': row.get('Top Terms (by LLR)', ''),
                'Label': row.get('Label (LLR)', '')
            })
    return clusters

def process_cocitation_nodes(node_file, top_n=10):
    """
    处理共被引网络节点，提取高中心性/高被引文献
    用于生成 Top 10 里程碑论文候选列表
    """
    nodes = parse_citespace_nodes(node_file)

    # 提取关键指标
    processed = []
    for node in nodes:
        processed.append({
            'Id': node.get('Id', ''),
            'Label': node.get('Label', ''),
            'Frequency': node.get('Weight', ''),  # 被引频次
            'Centrality': node.get('Centrality', ''),  # 中介中心性
            'Sigma': node.get('Sigma', ''),  # Sigma 值
            'Burst': node.get('Burst', ''),  # 突现强度
            'Year': node.get('Year', '')
        })

    # 按被引频次排序
    top_by_citation = sorted(processed, 
                              key=lambda x: float(x['Frequency'] or 0), 
                              reverse=True)[:top_n]

    # 按中心性排序
    top_by_centrality = sorted(processed, 
                               key=lambda x: float(x['Centrality'] or 0), 
                               reverse=True)[:top_n]

    return top_by_citation, top_by_centrality

def generate_milestone_table(cocitation_nodes, burst_nodes, output_file):
    """
    生成 Top 10 里程碑论文候选列表
    综合被引量、突现强度、中介中心性、Sigma 值
    """
    # 合并指标
    paper_dict = defaultdict(lambda: {
        'Label': '',
        'Citations': 0,
        'Burst_Strength': 0,
        'Betweenness_Centrality': 0,
        'Sigma': 0,
        'Year': ''
    })

    # 从共被引节点提取被引量和中心性
    for node in cocitation_nodes:
        label = node.get('Label', '')
        paper_dict[label]['Label'] = label
        paper_dict[label]['Citations'] = float(node.get('Frequency', 0))
        paper_dict[label]['Betweenness_Centrality'] = float(node.get('Centrality', 0))
        paper_dict[label]['Sigma'] = float(node.get('Sigma', 0))
        paper_dict[label]['Year'] = node.get('Year', '')

    # 从突现节点提取突现强度
    for node in burst_nodes:
        label = node.get('Label', '')
        paper_dict[label]['Burst_Strength'] = float(node.get('Burst', 0))

    # 计算综合得分并排序
    papers = []
    for label, metrics in paper_dict.items():
        # 综合得分 = 被引量归一化 + 突现强度归一化 + 中心性归一化 + Sigma
        # 这里使用简单加权，可根据需要调整
        score = (metrics['Citations'] * 0.3 + 
                 metrics['Burst_Strength'] * 100 * 0.3 + 
                 metrics['Betweenness_Centrality'] * 100 * 0.2 + 
                 metrics['Sigma'] * 0.2)

        papers.append({
            'Label': label,
            'Citations': metrics['Citations'],
            'Burst_Strength': metrics['Burst_Strength'],
            'Betweenness_Centrality': metrics['Betweenness_Centrality'],
            'Sigma': metrics['Sigma'],
            'Year': metrics['Year'],
            'Composite_Score': score
        })

    # 按综合得分排序
    papers.sort(key=lambda x: x['Composite_Score'], reverse=True)

    # 保存 Top 10
    top_10 = papers[:10]
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=[
            'Rank', 'Label', 'Year', 'Citations', 
            'Burst_Strength', 'Betweenness_Centrality', 'Sigma', 'Composite_Score'
        ])
        writer.writeheader()
        for rank, paper in enumerate(top_10, 1):
            paper['Rank'] = rank
            writer.writerow(paper)

    return top_10

def main():
    print("=" * 60)
    print("CiteSpace 结果后处理")
    print("=" * 60)

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # 示例：处理关键词聚类结果
    cluster_file = os.path.join(CITESPACE_OUTPUT_DIR, "clusters_summary.csv")
    if os.path.exists(cluster_file):
        clusters = process_keyword_clusters(cluster_file)
        print(f"读取到 {len(clusters)} 个聚类")

        output = os.path.join(OUTPUT_DIR, "cluster_summary_processed.csv")
        with open(output, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=[
                'Cluster_ID', 'Size', 'Silhouette', 'Mean_Year', 'Top_Terms', 'Label'
            ])
            writer.writeheader()
            writer.writerows(clusters)
        print(f"聚类汇总已保存: {output}")

    # 示例：处理共被引节点生成里程碑论文表
    cocitation_file = os.path.join(CITESPACE_OUTPUT_DIR, "cocitation_nodes.csv")
    burst_file = os.path.join(CITESPACE_OUTPUT_DIR, "burst_nodes.csv")

    if os.path.exists(cocitation_file):
        top_citation, top_centrality = process_cocitation_nodes(cocitation_file, top_n=20)
        print(f"\n高被引文献 Top 5:")
        for i, node in enumerate(top_citation[:5], 1):
            print(f"  {i}. {node['Label'][:60]}... (被引: {node['Frequency']})")

        if os.path.exists(burst_file):
            milestone_output = os.path.join(OUTPUT_DIR, "top10_milestone_candidates.csv")
            # 这里需要实际数据才能运行
            print(f"\n里程碑论文候选表将保存至: {milestone_output}")

    print("=" * 60)

if __name__ == "__main__":
    main()
