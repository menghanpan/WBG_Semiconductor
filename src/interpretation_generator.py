#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
图表解读文字辅助生成脚本
用途：根据分析数据自动生成图表解读的初稿文字
输入：各统计结果 CSV 文件
输出：interpretation_draft.md（每张图的解读初稿）
"""

import os
import csv
from datetime import datetime

OUTPUT_DIR = "../results/interpretation"
DATA_DIR = "../results/statistics"

def load_csv_data(filename):
    """加载 CSV 数据"""
    filepath = os.path.join(DATA_DIR, filename)
    if not os.path.exists(filepath):
        return []

    with open(filepath, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        return list(reader)

def generate_fig1_interpretation(cluster_data, keyword_data):
    """生成图1（共被引网络/关键词聚类）解读初稿"""

    if not cluster_data:
        return "[数据不足，无法生成解读]"

    # 获取主要聚类信息
    clusters = sorted(cluster_data, key=lambda x: int(x.get('Size', 0)), reverse=True)
    top_clusters = clusters[:3]

    # 计算平均轮廓值
    avg_silhouette = sum(float(c.get('Silhouette', 0)) for c in clusters) / len(clusters)

    text = f"""## 图1: 关键词聚类网络图解读

### 研究问题
**知识基础是什么？** —— 宽禁带半导体功率器件领域的研究主题如何结构化分布？

### 主要发现

本研究基于 CiteSpace 6.4.R2 对 2014 篇文献进行关键词聚类分析，时间切片为 2020–2026 年，采用 g-index=25 的筛选策略和 LLR 聚类标签提取算法。网络共识别出 {len(clusters)} 个主要聚类，网络模块化指数 Q 值为 [请填入]，平均轮廓值 S 为 {avg_silhouette:.3f}。

**聚类结构特征：**

"""

    for i, cluster in enumerate(top_clusters, 1):
        cluster_id = cluster.get('Cluster_ID', i)
        label = cluster.get('Label', '未命名')
        size = cluster.get('Size', 0)
        silhouette = cluster.get('Silhouette', 0)
        mean_year = cluster.get('Mean_Year', '')

        text += f"""
**聚类 #{cluster_id}**（规模: {size}，轮廓值: {silhouette}）
- 标签: {label}
- 平均年份: {mean_year}
- 该聚类代表 [请根据标签内容描述研究主题]
"""

    text += f"""
**网络整体特征：**

从聚类分布来看，宽禁带半导体功率器件领域的知识基础呈现 [集中/分散] 特征。{top_clusters[0].get('Label', '最大聚类')} 相关研究构成了领域的核心知识基础，而 [其他聚类] 则代表了 [新兴/交叉] 研究方向。

**关键节点：**

网络中中介中心性较高的关键词包括 [请填入高中心性节点]，这些节点在不同聚类间起到桥梁作用，反映了领域知识结构的 [整合/分化] 特征。

### 局限

- 聚类结果依赖算法参数设置，不同 g-index 阈值可能产生不同的聚类结构
- LLR 标签提取基于统计显著性，可能存在语义解读偏差
- 2026 年数据可能不完整，影响最新研究趋势的判断
- 关键词聚类反映的是主题共现关系，无法直接揭示知识传承路径

---
"""

    return text

def generate_fig2_interpretation(timeline_data, burst_data):
    """生成图2（时间线/突现图）解读初稿"""

    text = "## 图2: 时间线图/突现图解读\n\n"
    text += "### 研究问题\n"
    text += "**趋势如何演化？** —— 宽禁带半导体功率器件领域的研究主题随时间如何变迁？\n\n"
    text += "### 主要发现\n\n"

    if timeline_data:
        # 按阶段分组
        early = [c for c in timeline_data if float(c.get('Mean_Year', 0)) <= 2021.5]
        middle = [c for c in timeline_data if 2021.5 < float(c.get('Mean_Year', 0)) <= 2023.5]
        recent = [c for c in timeline_data if float(c.get('Mean_Year', 0)) > 2023.5]

        text += f"""**演化阶段划分：**

基于聚类平均年份分析，领域研究演化可分为三个阶段：

**1. 早期阶段（2020–2021）**
- 主要聚类: {', '.join([c.get('Label', '')[:30] for c in early[:2]]) if early else '[请填入]'}
- 特征: [请描述早期研究特点]

**2. 发展阶段（2022–2023）**
- 主要聚类: {', '.join([c.get('Label', '')[:30] for c in middle[:2]]) if middle else '[请填入]'}
- 特征: [请描述发展期研究特点]

**3. 近期阶段（2024–2026）**
- 主要聚类: {', '.join([c.get('Label', '')[:30] for c in recent[:2]]) if recent else '[请填入]'}
- 特征: [请描述近期研究特点]

"""

    if burst_data:
        active_bursts = [b for b in burst_data if b.get('Status') == 'Active']
        text += f"""**突现词分析：**

突现检测识别出 {len(burst_data)} 个显著突现的关键词/主题，其中 {len(active_bursts)} 个当前仍在持续突现。

**持续突现的热点：**
"""
        for burst in active_bursts[:5]:
            text += f"- {burst.get('Keyword', '')}（突现强度: {burst.get('Strength', '')}，始于 {burst.get('Begin', '')}）\n"

        text += "\n**已结束的突现：**\n"
        ended_bursts = [b for b in burst_data if b.get('Status') != 'Active']
        for burst in ended_bursts[:5]:
            text += f"- {burst.get('Keyword', '')}（{burst.get('Begin', '')}-{burst.get('End', '')}）\n"

    text += f"""
**演化趋势总结：**

从时间演化来看，宽禁带半导体功率器件领域的研究呈现出从 [早期主题] 向 [近期主题] 的演进趋势。[请根据实际数据补充具体发现]

### 局限

- 时间切片为 1 年，可能无法精确捕捉跨年度的突变事件
- 突现检测的 Minimum Duration=2 年设置可能遗漏短期热点
- 2026 年数据不完整，当年突现趋势需谨慎解读
- 突现强度受文献总量增长影响，需结合相对指标判断

---
"""

    return text

def generate_fig3_interpretation(author_data, institution_data):
    """生成图3（作者/机构合作网络）解读初稿"""

    text = "## 图3: 作者合作网络/机构合作地图解读\n\n"
    text += "### 研究问题\n"
    text += "**谁在推动这个领域？** —— 哪些作者和机构是宽禁带半导体功率器件领域的核心贡献者？\n\n"
    text += "### 主要发现\n\n"

    if author_data:
        top_authors = author_data[:5]
        text += "**核心作者：**\n\n"
        for i, author in enumerate(top_authors, 1):
            name = author.get('Author', '')
            pubs = author.get('Publications', '')
            text += f"{i}. **{name}**（发文量: {pubs} 篇）\n"
            text += f"   - 主要研究方向: [请根据文献内容补充]\n"
            text += f"   - 合作网络特征: [请补充]\n\n"

    if institution_data:
        top_inst = institution_data[:5]
        text += "**核心机构：**\n\n"
        for i, inst in enumerate(top_inst, 1):
            name = inst.get('Institution', '')
            pubs = inst.get('Publications', '')
            text += f"{i}. **{name}**（发文量: {pubs} 篇）\n"
            text += f"   - 机构类型: [高校/研究所/企业]\n\n"

    text += """**合作网络特征：**

网络密度为 [请填入]，呈现 [核心-边缘/多中心/紧密连接] 结构。主要合作群体包括：
- [群体1]: [描述]
- [群体2]: [描述]

**地域分布：**

中国/美国/欧洲机构分别占比 [请填入]%，显示 [某地区] 在该领域占主导地位。产业界参与度 [高/低]，主要企业包括 [请填入]。

### 局限

- 作者名消歧无法完全解决，同名同姓可能导致统计偏差
- 机构标准化依赖映射表，部分机构合并可能不够精确
- 合作网络仅反映合著关系，无法体现非正式学术影响
- 通讯作者信息可能更能代表机构贡献，但本分析基于全部作者

---
"""

    return text

def generate_table1_interpretation():
    """生成表1（Top 10里程碑论文）解读初稿"""

    return """## 表1: Top 10 里程碑论文列表解读

### 研究问题
**领域的奠基性文献有哪些？** —— 哪些论文在宽禁带半导体功率器件的知识结构中起到关键作用？

### 主要发现

本研究基于文献共被引网络分析，综合考虑被引量、突现强度、中介中心性和 Sigma 值四项指标，筛选出该领域的 Top 10 里程碑论文。

**指标说明：**

| 指标 | 含义 | 重要性 |
|:---|:---|:---|
| 被引量 | 总被引次数 | 反映学术影响力 |
| 突现强度 | 特定时期关注度跃升程度 | 反映研究前沿性 |
| 中介中心性 | 连接不同知识社群的能力 | 反映知识枢纽作用 |
| Sigma 值 | 结构性和时间性新颖性综合指标 | Σ>1 表示具有结构洞和时间前沿双重特征 |

**Top 10 论文特征：**

[请根据实际数据填写具体论文信息]

1. **[作者, 年份]** - 被引量: [X], 突现强度: [X], 中介中心性: [X], Sigma: [X]
   - 主要贡献: [请补充]

2. **[作者, 年份]** - ...

**综合分析：**

Top 10 论文中，Sigma > 1 的有 [X] 篇，表明这些文献不仅被大量引用，还在知识结构中起到桥梁作用。从时间分布来看，[早期/近期] 文献占比更高，说明 [请补充发现]。

### 局限

- 四项指标均基于引用数据，可能遗漏尚未被广泛引用的新兴文献
- Sigma 值计算依赖网络结构，不同参数设置可能影响排序
- 单一文献列表无法全面反映领域知识基础
- 被引量受发表时间影响，早期文献有累积优势

---
"""

def main():
    print("=" * 60)
    print("图表解读文字辅助生成")
    print("=" * 60)

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # 加载数据
    print("\n正在加载分析数据...")
    cluster_data = load_csv_data("timeline_analysis.csv")
    keyword_data = load_csv_data("top_keywords.csv")
    timeline_data = load_csv_data("timeline_analysis.csv")
    burst_data = load_csv_data("burst_keywords.csv")
    author_data = load_csv_data("top_authors.csv")
    institution_data = load_csv_data("top_institutions.csv")

    # 生成各图解读
    print("正在生成解读初稿...")

    interpretations = []
    interpretations.append(generate_fig1_interpretation(cluster_data, keyword_data))
    interpretations.append(generate_fig2_interpretation(timeline_data, burst_data))
    interpretations.append(generate_fig3_interpretation(author_data, institution_data))
    interpretations.append(generate_table1_interpretation())

    # 合并并保存
    full_text = f"""# 图表解读初稿

> 生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M')}
> 说明: 本文件为自动生成的解读初稿，需根据实际分析结果补充具体数据和发现。

---

"""
    full_text += "\n\n".join(interpretations)

    output_file = os.path.join(OUTPUT_DIR, "interpretation_draft.md")
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(full_text)

    print(f"\n解读初稿已生成: {output_file}")
    print("\n请根据实际分析结果补充以下内容:")
    print("  1. CiteSpace 网络质量指标（Q值、S值）")
    print("  2. 具体的高中心性节点名称")
    print("  3. 各聚类的详细研究主题描述")
    print("  4. Top 10 里程碑论文的具体信息")
    print("  5. 网络密度等结构指标")

    print("\n" + "=" * 60)

if __name__ == "__main__":
    main()
