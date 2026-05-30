#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CiteSpace 网络质量指标提取脚本
用途：从 CiteSpace 生成的报告文件或日志中提取网络质量指标
输入：CiteSpace 报告文本 / 手动记录的数据
输出：network_metrics.csv（用于论文/报告中的指标汇总表）
"""

import os
import csv
import re
from datetime import datetime

OUTPUT_DIR = "../results/statistics"

def extract_from_report(report_text):
    """
    从 CiteSpace 生成的报告文本中提取指标
    报告文本可通过 CiteSpace: Report -> Generate -> Network Summary 获取
    """
    metrics = {}

    # Modularity Q
    q_match = re.search(r'Modularity Q\s*=\s*([\d.]+)', report_text)
    if q_match:
        metrics['Modularity_Q'] = float(q_match.group(1))

    # Weighted Mean Silhouette S
    s_match = re.search(r'Weighted Mean Silhouette S\s*=\s*([\d.]+)', report_text)
    if s_match:
        metrics['Mean_Silhouette_S'] = float(s_match.group(1))

    # Mean Cited Year
    year_match = re.search(r'Mean Cited Year\s*=\s*([\d.]+)', report_text)
    if year_match:
        metrics['Mean_Cited_Year'] = float(year_match.group(1))

    # Network Density
    density_match = re.search(r'Density\s*=\s*([\d.]+)', report_text)
    if density_match:
        metrics['Network_Density'] = float(density_match.group(1))

    # Number of Nodes
    nodes_match = re.search(r'Nodes\s*=\s*(\d+)', report_text)
    if nodes_match:
        metrics['Nodes'] = int(nodes_match.group(1))

    # Number of Links
    links_match = re.search(r'Links\s*=\s*(\d+)', report_text)
    if links_match:
        metrics['Links'] = int(links_match.group(1))

    # Number of Clusters
    clusters_match = re.search(r'Clusters\s*=\s*(\d+)', report_text)
    if clusters_match:
        metrics['Clusters'] = int(clusters_match.group(1))

    return metrics

def create_metrics_template():
    """
    生成网络质量指标记录模板
    由于 CiteSpace 不直接导出结构化指标，需手动填入
    """
    template = {
        'Analysis_Type': '',           # 如: Keyword_Clustering / Cocitation / Author_Collaboration
        'Node_Type': '',             # 如: Keyword / Cited Reference / Author
        'Time_Slice': '2020-2026',
        'Years_Per_Slice': 1,
        'Selection_Criteria': 'g-index=25',
        'Pruning': 'Pathfinder + Pruning sliced networks',

        # 以下需从 CiteSpace 界面或报告中获取
        'Modularity_Q': '',          # 模块化指数 Q > 0.3 表示聚类显著
        'Mean_Silhouette_S': '',     # 平均轮廓值 S > 0.5 聚类合理
        'Mean_Cited_Year': '',       # 平均被引年份
        'Network_Density': '',       # 网络密度
        'Nodes': '',                 # 节点数
        'Links': '',                 # 连线数
        'Clusters': '',              # 聚类数

        # 记录信息
        'Record_Date': datetime.now().strftime('%Y-%m-%d'),
        'Notes': ''
    }
    return template

def save_metrics_table(analyses, output_file):
    """
    保存多个分析的网络指标汇总表

    analyses: list of dict, 每个 dict 是一个分析的网络指标
    """
    if not analyses:
        print("警告: 没有数据可保存")
        return

    fieldnames = [
        'Analysis_Type', 'Node_Type', 'Time_Slice', 'Years_Per_Slice',
        'Selection_Criteria', 'Pruning',
        'Modularity_Q', 'Mean_Silhouette_S', 'Mean_Cited_Year',
        'Network_Density', 'Nodes', 'Links', 'Clusters',
        'Record_Date', 'Notes'
    ]

    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for analysis in analyses:
            # 确保所有字段存在
            row = {k: analysis.get(k, '') for k in fieldnames}
            writer.writerow(row)

    print(f"网络指标汇总表已保存: {output_file}")

def print_metrics_interpretation():
    """打印指标解读说明"""
    print("\n" + "="*60)
    print("CiteSpace 网络质量指标解读")
    print("="*60)

    interpretations = [
        ("Modularity Q", 
         "模块化指数", 
         "Q > 0.3: 聚类结构显著 | Q > 0.5: 聚类结构清晰 | Q > 0.7: 聚类结构非常清晰"),
        ("Mean Silhouette S", 
         "平均轮廓值", 
         "S > 0.5: 聚类合理可信 | S > 0.7: 聚类结果高度可信"),
        ("Mean Cited Year", 
         "平均被引年份", 
         "反映研究前沿性，越接近当前年份说明研究越前沿"),
        ("Network Density", 
         "网络密度", 
         "0-1之间，值越大网络连接越紧密，但过高可能意味着主题过于集中"),
        ("Nodes", 
         "节点数", 
         "网络中的节点总数，反映分析规模"),
        ("Links", 
         "连线数", 
         "节点间的连接总数"),
        ("Clusters", 
         "聚类数", 
         "自动识别的聚类数量"),
    ]

    for metric, name, interpretation in interpretations:
        print(f"\n【{metric}】- {name}")
        print(f"  解读: {interpretation}")

    print("\n" + "="*60)

def main():
    print("="*60)
    print("CiteSpace 网络质量指标提取工具")
    print("="*60)

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # 打印指标解读
    print_metrics_interpretation()

    # 生成模板
    print("\n生成网络指标记录模板...")
    template = create_metrics_template()

    # 示例：为三种分析类型生成空模板
    analyses = []
    analysis_types = [
        ('Keyword_Clustering', 'Keyword', '关键词聚类分析'),
        ('Cocitation_Network', 'Cited Reference', '文献共被引网络'),
        ('Author_Collaboration', 'Author', '作者合作网络'),
    ]

    for analysis_type, node_type, note in analysis_types:
        t = template.copy()
        t['Analysis_Type'] = analysis_type
        t['Node_Type'] = node_type
        t['Notes'] = note
        analyses.append(t)

    # 保存模板
    output_file = os.path.join(OUTPUT_DIR, "network_metrics_template.csv")
    save_metrics_table(analyses, output_file)

    print("\n使用说明:")
    print("1. 在 CiteSpace 中完成分析后，记录界面左下角显示的网络指标")
    print("2. 将指标数值填入 network_metrics_template.csv 对应列")
    print("3. 该表格可直接用于论文中的方法学描述部分")

    print("\n" + "="*60)

if __name__ == "__main__":
    main()
