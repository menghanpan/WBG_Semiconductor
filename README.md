# 文献研究概要：2020-2025年宽禁带半导体功率器件的发展与挑战
自2020年以来，由于全球对能源转换效率、系统小型化及高功率密度的迫切需求，以碳化硅 (SiC) 和 氮化镓 (GaN) 为代表的第三代（宽禁带）半导体研究进入了爆发期。与传统硅 (Si) 基器件相比，这些材料具有更高的击穿电场、更高的热导率和更快的饱和电子漂移速度。本检索范围涵盖了从底层物理结构（晶体管、二极管）到应用前端的关键技术演进。
# 项目成员与职责

组长：张娜   整体安排和相关数据获取与检索式撰写   | data/raw/src/config |

组员：魏瑜琤  撰写并完善项目报告，产出报告分析并准备答辩 | reports/paper |

组员：邹星云   处理相关运行环境代码 | src/data  |

组员：潘梦涵   数据清洗去重，图谱构建与计量分析，完成数据分析并输出结果报告  | data/src/outputs/docs/ |

# 检索式
v0.2
TS=( “third generation semiconductor” OR “wide-bandgap semiconductor” OR “silicon carbide” OR SiC OR “gallium nitride” OR GaN )
AND TS=(“MOSFET” OR “HEMT” OR “SBD” OR “transistor” OR “diode”)
AND PY=2020-2025
AND LA=English
AND DT=("Article" OR "Review" OR "Proceedings Paper")


# 规范化目录结构

项目文件分类为“原始数据”、“处理逻辑与分析产出”。具体目录说明如下：

- **config/**：存放项目配置文件如查询参数。
- **data/raw/**：原始数据及其导入系统的结构。
- **data/processed/**：经过处理的数据集。
- **src/**：Python脚本来处理和分析数据。
- **outputs/**：分析结果，包括报告和可视化图表。
- **docs/**：存放有说明性，解释性的文字。
- **reports/**：最终项目报告。
- **paper/**：学术论文草稿及其相关参考资料。
- **README.md/**：项目说明文档。

# 项目核心里程碑 (Milestones)

## M1阶段：数据与检索方案验证（第4周末前）
- **阶段目标**：完成从数据获取到初步清洗和验证。
- **核心步骤**：
  - 验证配置文件准确性。
  - 定期检查数据质量报告。

## M2阶段：计量分析与图谱产出（第10周末前）
- **阶段目标**：构建完整的文献计量网络图谱。
- **核心步骤**：
  - 完成图谱分析，并输出详细结果。


## M3阶段：终稿与项目归档（第15周末前）
- **阶段目标**：编制详细的项目报告和学术论文。
- **核心步骤**：
  - 完成论文撰写与代码库的整理。

# 数据处理

## 1. 数据来源
- **数据库**：Web of Science Core Collection
- **检索日期**：2026年5月27日（请填写实际日期）
- **导出格式**：Plain Text (.txt)，Full Record and Cited References

## 2. 检索策略

| 项目 | 内容 |
|:---|:---|
| 检索式 | TS=( “third generation semiconductor” OR “wide-bandgap semiconductor” OR “silicon carbide” OR SiC OR “gallium nitride” OR GaN )
          AND TS=(“MOSFET” OR “HEMT” OR “SBD” OR “transistor” OR “diode”)
| 时间范围 | 2020–2025 |
| 语言 | English |
| 文献类型 | Article, Review, Proceedings Paper |
| 检索命中量 | 3000 篇 |

## 3. 数据导出字段（Full Record）

| 字段类别 | 具体字段 | 用途 |
| 基础信息 | Title, Author, Publication Year, Source Title, Volume, Issue, Pages, DOI | 文献标识、期刊分析 |
| 作者信息 | Author, Author Identifiers, Affiliation, Reprint Address, E-mail Address | 作者合作分析、机构分析 |
| 内容信息 | Abstract, Author Keywords, Keywords Plus | 关键词共现分析、主题提取 |
| 引文信息 | References, Cited Reference Count, Times Cited, 180 Day Usage Count, Since 2013 Usage Count | 共被引分析、引文分析 |
| 分类信息 | Research Area, Web of Science Categories | 学科分布分析 |
| 基金信息 | Funding Orgs, Funding Text | 基金资助分析 |

> 注：导出时选择 **Full Record and Cited References**，确保包含参考文献列表，以支持文献共被引分析。

## 4. 最终分析数据集特征

| 指标 | 数值 |
|:---|:---|
| 时间跨度 | 2020–2025 |
| 文献总量 | 2,014 篇 |
| 文献类型 | Article, Review |
| 语言 | English |
| 数据格式 | CiteSpace 可识别的 WoS 纯文本格式 (.txt) |

## 5. 处理流程

```
数据获取 (Web of Science)
    ↓
数据清洗 (Python 脚本: wos_data_cleaning.py)
    ├── DOI 去重: 3000 → 2994 篇
    ├── 同义词合并
    ├── 机构名称标准化
    └── 作者名消歧
    ↓
数据导入 (CiteSpace 6.4.R2)
    ├── 格式: WoS Plain Text (.txt)
    └── 筛选: Article + Review → 2,014 篇
    ↓
参数设置
    ├── 时间切片: 2020 JAN – 2026 DEC
    ├── 时间段: 1 年
    └── 筛选方式: g-index = 25
    ↓
可视化分析
    ├── 图1: 文献共被引网络图 / 关键词聚类图
    ├── 图2: 时间线图 / 突现图
    ├── 图3: 作者合作网络图 / 机构合作地图
    └── 表1: Top 10 里程碑论文列表
```

### 详细说明

| 步骤 | 工具/软件 | 输入 | 输出 | 文档 |
|:---|:---|:---|:---|:---|
| 数据清洗 | Python 3.x | `wos_raw_merged.txt` | `wos_cleaned_for_citespace.txt` | [processing_workflow.md](docs/processing_workflow.md) |
| 参数设置 | CiteSpace 6.4.R2 (64-bit, Windows) | 清洗后数据 | 分析项目文件 | [parameter_settings.md](docs/parameter_settings.md) |
| 结果解读 | — | 可视化图谱 | 文字说明 (≥200字/图) | [interpretation_guide.md](docs/interpretation_guide.md) |

## 6. 数据分析

### 分析维度与研究问题对应

| 输出 | 分析维度 | 研究问题 | 解读要求 |
|:---|:---|:---|:---|
| **图1** | 文献共被引网络 / 关键词聚类 | 知识基础是什么？ | ≥200字，含聚类结构、关键节点、时间特征 |
| **图2** | 时间线图 / 突现图 | 趋势如何演化？ | ≥200字，含演化阶段、突现词、聚类持续时间 |
| **图3** | 作者合作网络 / 机构地图 | 谁在推动这个领域？ | ≥200字，含核心作者、网络结构、机构分布 |
| **表1** | Top 10 里程碑论文 | 领域奠基性文献 | ≥200字，含四项指标解读、主题分布、关键文献分析 |

### 宽禁带半导体功率器件领域文献计量分析
【总数据分析】 [宽禁带半导体功率器件领域文献计量分析报告.md](outputs/宽禁带半导体功率器件领域文献计量分析报告.md)

基于 Web of Science 数据库（2020–2026年，共277篇文献），使用 CiteSpace v.6.4.R2 进行知识图谱分析。本报告涵盖四大维度：知识基础、趋势演化、核心团队与里程碑论文。

## 图1：文献共被引网络 / 关键词聚类
 [文献共被引图](outputs/fig1_cocitation_cluster.png)
 [关键词聚类图](outputs/fig1_keywords_clusters_network.png)

**研究问题**：领域的知识基础是什么？

**核心发现**：

- 领域围绕 SiC、GaN、Ga2O3 三大材料体系展开，SiC MOSFET 与 GaN HEMT 是最主要研究对象。
- 识别出 5 个主要知识群：器件物理与建模、材料与工艺、封装与可靠性、电路与应用、新型器件结构。
- 6 篇高被引核心文献构成知识基石：Amano H (2018)、Chen KJ (2017)、She X (2017)、Lei Zhang (2019)、Meneghini M (2021)、Kozak JP (2023)。
- 网络密度 0.0232，最大连通分量占 90%，领域处于发展期但知识体系相对统一。

## 图2：时间线图 / 突现图
[关键词突现检测图](outputs/fig2_burst_detection.png)
[关键词时间线变化趋势图]( outputs/fig2_timeline.png)

**研究问题**：研究趋势如何演化？

**核心发现**：

- **三阶段演化**：2020–2021 奠基期 → 2022–2023 成长期 → 2024–2026 深化期。
- SiC MOSFET 稳步上升，GaN HEMT 在 2022 年后增速放缓，SiC 在高压大功率应用中的优势逐渐凸显。
- **三大新兴趋势**：
  - `trench gate`（沟槽栅）：自 2021 年起快速增长
  - `superjunction`（超结）移植 GaN：2023 年后显著增加
  - `reliability`（可靠性）：2024–2025 年热度快速攀升
- 衰退主题：`planar gate`（平面栅）被沟槽栅替代；`material growth` 进入成熟稳定期。

## 图3：作者合作网络 / 机构地图
.[作者合作网络图]( outputs/fig3_author_network.png)

**研究问题**：谁在推动这个领域？

**核心团队（8 个）**：

| 团队 | 机构 | 核心人物 | 研究方向 |
|------|------|----------|----------|
| 1 | 中国香港科技大学 | Chen, KJ | GaN HEMT、集成器件 |
| 2 | 电子科技大学 | Luo, XR、Wei, J | SiC MOSFET |
| 3 | 浙江大学 | Sheng, K | 功率模块、系统集成 |
| 4 | 东芝/三菱 | Kono, H、Ohashi, T | 产业化器件 |
| 5 | 湖南大学 | Wang, J | 器件可靠性物理 |
| 6 | 中国台湾大学 | Lee, KY | 器件建模与表征 |
| 7 | 韩国西江大学 | Kim, K | 新型器件结构 |
| 8 | 重庆大学 | Hu, SD | 集成 SBD、MCD |

**网络结构**：呈"多中心、强合作"格局，中、美、韩三国团队形成紧密合作网络，欧洲团队相对独立。

## 表1：Top 10 里程碑论文
.[T10 milestone候选论文列表](outputs/table1_top10_milestone.csv)

**指标说明**：

- **被引量（本地）**：关键词在数据集中的加权共现频次
- **中介中心性**：第一作者在合作网络中的桥梁作用
- **突现强度**：关键词在发表年份的相对热度增长率
- **Sigma 值**：`(centrality + 1) ^ burstness`，值越大越具知识转折点意义

**Top 10 论文概览**：

| 排名 | 主题方向 | 代表作者 | 年份 |
|------|----------|----------|------|
| 1, 10 | 器件建模与仿真 | Li, X；Broeck, CH | 2025 |
| 2, 4, 8, 9 | 新型器件结构 | Wang, J；Liu, JC；Zhang, M；Zhang, YH | 2020–2022 |
| 3, 5, 7 | 可靠性物理 | Song, XT；Chen, X；Dai, Y | 2025 |

**关键发现**：

- 高 Sigma 值论文（论文 2、3、7）兼具结构重要性与时间突发性，代表知识转折点。
- 2025 年论文占 4 篇以上，领域正处于快速创新期。
- 论文 4（Liu, JC, 2022）被引量 2268 居首；论文 2（Wang, J, 2021）Sigma 值 1.2927 最高。

---

**数据来源**：Web of Science | **分析工具**：CiteSpace v.6.4.R2 | **网络规模**：N=277, E=886
