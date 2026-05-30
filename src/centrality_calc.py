
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
共被引网络节点中心性计算脚本
用途：从 CiteSpace 导出的共被引网络数据计算节点中心性指标
输入：CiteSpace 导出的节点和连线 CSV 文件
输出：节点中心性排名表（含中介中心性、接近中心性、特征向量中心性）
"""

import os
import csv
from collections import defaultdict

OUTPUT_DIR = "../results/statistics"

def build_graph(nodes_file, edges_file):
    """
    从 CiteSpace 导出的数据构建图结构
    """
    # 读取节点
    nodes = {}
    with open(nodes_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            node_id = row.get('Id', '')
            if node_id:
                nodes[node_id] = {
                    'label': row.get('Label', ''),
                    'weight': float(row.get('Weight', 0)),
                    'year': row.get('Year', '')
                }

    # 读取边并构建邻接表
    adjacency = defaultdict(list)
    edge_weights = {}

    with open(edges_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            source = row.get('Source', '')
            target = row.get('Target', '')
            weight = float(row.get('Weight', 1))

            if source in nodes and target in nodes:
                adjacency[source].append((target, weight))
                adjacency[target].append((source, weight))
                edge_weights[(source, target)] = weight
                edge_weights[(target, source)] = weight

    return nodes, adjacency, edge_weights

def calculate_degree_centrality(nodes, adjacency):
    """计算度中心性"""
    centrality = {}
    for node_id in nodes:
        centrality[node_id] = len(adjacency[node_id])
    return centrality

def calculate_betweenness_centrality(nodes, adjacency):
    """
    计算中介中心性（Brandes算法简化版）
    """
    betweenness = {node: 0.0 for node in nodes}

    for source in nodes:
        # BFS
        shortest_paths = defaultdict(list)
        shortest_paths[source] = [[]]
        visited = {source: 0}
        queue = [source]

        while queue:
            current = queue.pop(0)
            for neighbor, _ in adjacency[current]:
                if neighbor not in visited:
                    visited[neighbor] = visited[current] + 1
                    queue.append(neighbor)
                    shortest_paths[neighbor] = [path + [neighbor] for path in shortest_paths[current]]
                elif visited[neighbor] == visited[current] + 1:
                    shortest_paths[neighbor].extend([path + [neighbor] for path in shortest_paths[current]])

        # 计算依赖
        dependency = defaultdict(float)
        nodes_by_distance = sorted(visited.keys(), key=lambda x: visited[x], reverse=True)

        for node in nodes_by_distance:
            if node != source:
                path_count = len(shortest_paths[node])
                for path in shortest_paths[node]:
                    for intermediate in path[1:-1]:
                        if path_count > 0:
                            dependency[intermediate] += 1.0 / path_count

        for node in dependency:
            betweenness[node] += dependency[node]

    # 归一化
    n = len(nodes)
    if n > 2:
        for node in betweenness:
            betweenness[node] /= ((n - 1) * (n - 2) / 2)

    return betweenness

def calculate_closeness_centrality(nodes, adjacency):
    """计算接近中心性"""
    closeness = {}

    for source in nodes:
        distances = {source: 0}
        queue = [source]
        visited = {source}

        while queue:
            current = queue.pop(0)
            for neighbor, _ in adjacency[current]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    distances[neighbor] = distances[current] + 1
                    queue.append(neighbor)

        if len(distances) > 1:
            avg_distance = sum(distances.values()) / (len(distances) - 1)
            closeness[source] = 1.0 / avg_distance if avg_distance > 0 else 0
        else:
            closeness[source] = 0

    return closeness

def generate_centrality_report(nodes, adjacency):
    """生成中心性分析报告"""
    print("计算度中心性...")
    degree_cent = calculate_degree_centrality(nodes, adjacency)

    print("计算中介中心性...")
    betweenness_cent = calculate_betweenness_centrality(nodes, adjacency)

    print("计算接近中心性...")
    closeness_cent = calculate_closeness_centrality(nodes, adjacency)

    # 整合结果
    results = []
    for node_id in nodes:
        results.append({
            'Id': node_id,
            'Label': nodes[node_id]['label'],
            'Year': nodes[node_id]['year'],
            'Weight': nodes[node_id]['weight'],
            'Degree_Centrality': degree_cent.get(node_id, 0),
            'Betweenness_Centrality': betweenness_cent.get(node_id, 0),
            'Closeness_Centrality': closeness_cent.get(node_id, 0)
        })

    # 按中介中心性排序
    results.sort(key=lambda x: x['Betweenness_Centrality'], reverse=True)

    return results

def save_centrality_csv(results, output_file):
    """保存中心性结果"""
    fieldnames = [
        'Rank', 'Id', 'Label', 'Year', 'Weight',
        'Degree_Centrality', 'Betweenness_Centrality', 'Closeness_Centrality'
    ]

    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for rank, result in enumerate(results, 1):
            result['Rank'] = rank
            writer.writerow(result)

    print(f"中心性分析结果已保存: {output_file}")

def main():
    print("=" * 60)
    print("共被引网络节点中心性计算")
    print("=" * 60)

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # 文件路径
    nodes_file = "../results/citespace_export/cocitation_nodes.csv"
    edges_file = "../results/citespace_export/cocitation_edges.csv"

    if not os.path.exists(nodes_file) or not os.path.exists(edges_file):
        print("错误: 找不到 CiteSpace 导出的网络数据文件")
        print("请先从 CiteSpace 导出节点和连线数据:")
        print("  1. 在 CiteSpace 可视化界面中")
        print("  2. 点击 File -> Export -> Network")
        print("  3. 分别导出 Nodes 和 Edges 为 CSV 格式")
        return

    # 构建图
    print("\n正在构建网络图...")
    nodes, adjacency, edge_weights = build_graph(nodes_file, edges_file)
    print(f"节点数: {len(nodes)}")
    print(f"边数: {len(edge_weights) // 2}")  # 无向图，边数减半

    # 计算中心性
    print("\n正在计算中心性指标...")
    results = generate_centrality_report(nodes, adjacency)

    # 显示 Top 10
    print("\n中介中心性 Top 10:")
    print("-" * 80)
    print(f"{'排名':<6}{'文献':<50}{'中介中心性':<12}")
    print("-" * 80)
    for r in results[:10]:
        label = r['Label'][:45] + "..." if len(r['Label']) > 48 else r['Label']
        print(f"{r['Rank']:<6}{label:<50}{r['Betweenness_Centrality']:<12.4f}")

    # 保存结果
    output_file = os.path.join(OUTPUT_DIR, "node_centrality_analysis.csv")
    save_centrality_csv(results, output_file)

    print("\n" + "=" * 60)
    print("中心性指标说明:")
    print("  • Degree Centrality: 连接数，反映节点活跃度")
    print("  • Betweenness Centrality: 中介程度，反映桥梁作用")
    print("  • Closeness Centrality: 接近程度，反映信息传播效率")
    print("=" * 60)

if __name__ == "__main__":
    main()
