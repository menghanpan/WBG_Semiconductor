# 文献研究概要：2020-2025年宽禁带半导体功率器件的发展与挑战
自2020年以来，由于全球对能源转换效率、系统小型化及高功率密度的迫切需求，以碳化硅 (SiC) 和 氮化镓 (GaN) 为代表的第三代（宽禁带）半导体研究进入了爆发期。与传统硅 (Si) 基器件相比，这些材料具有更高的击穿电场、更高的热导率和更快的饱和电子漂移速度。本检索范围涵盖了从底层物理结构（晶体管、二极管）到应用前端的关键技术演进。
# 项目成员与职责

组长：张娜   整体安排和相关数据获取与规划   | data/raw/src/config |

组员：魏瑜琤  撰写并完善项目报告，做报告分析。 | reports/paper |

组员：邹星云   处理相关代码 | src/data  |

组员：潘梦涵   图谱构建与计量分析，完成数据分析并输出结果报告。  | data/src/outputs/docs/   |

# 检索式
v0.2
TS=( “third generation semiconductor” OR “wide-bandgap semiconductor” OR “silicon carbide” OR SiC OR “gallium nitride” OR GaN )
AND TS=(“MOSFET” OR “HEMT” OR “SBD” OR “transistor” OR “diode”)
AND PY=2020-2025
AND LA=English
AND DT=("Article" OR "Review" OR "Proceedings Paper")


# 规范化目录结构re

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

# 数据规模

## 1. 数据来源
- **数据库**：Web of Science Core Collection
- **检索日期**：2026年X月X日（请填写实际日期）
- **导出格式**：Plain Text (.txt)，Full Record and Cited References

## 2. 检索策略

| 项目 | 内容 |
|:---|:---|
| 检索式 | `TS=("third generation semiconductor" OR "wide band gap semiconductor" OR "silicon carbide" OR SiC OR "gallium nitride" OR GaN)` |
| 时间范围 | 2020–2026 |
| 语言 | English |
| 文献类型 | Article, Review, Proceedings Paper |
| 检索命中量 | 4,369 篇 |

## 3. 数据筛选流程

## 4. 数据导出字段（Full Record）

| 字段类别 | 具体字段 | 用途 |
| 基础信息 | Title, Author, Publication Year, Source Title, Volume, Issue, Pages, DOI | 文献标识、期刊分析 |
| 作者信息 | Author, Author Identifiers, Affiliation, Reprint Address, E-mail Address | 作者合作分析、机构分析 |
| 内容信息 | Abstract, Author Keywords, Keywords Plus | 关键词共现分析、主题提取 |
| 引文信息 | References, Cited Reference Count, Times Cited, 180 Day Usage Count, Since 2013 Usage Count | 共被引分析、引文分析 |
| 分类信息 | Research Area, Web of Science Categories | 学科分布分析 |
| 基金信息 | Funding Orgs, Funding Text | 基金资助分析 |

> 注：导出时选择 **Full Record and Cited References**，确保包含参考文献列表，以支持文献共被引分析。

## 5. 最终分析数据集特征

| 指标 | 数值 |
|:---|:---|
| 时间跨度 | 2020–2026 |
| 文献总量 | 2,014 篇 |
| 文献类型 | Article, Review |
| 语言 | English |
| 数据格式 | CiteSpace 可识别的 WoS 纯文本格式 (.txt) |

# 处理流程

```
数据获取 (Web of Science)
    ↓
数据清洗 (Python 脚本: wos_data_cleaning.py)
    ├── DOI 去重: 4,369 → 3,000 篇
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

## 详细说明

| 步骤 | 工具/软件 | 输入 | 输出 | 文档 |
|:---|:---|:---|:---|:---|
| 数据清洗 | Python 3.x | `wos_raw_merged.txt` | `wos_cleaned_for_citespace.txt` | [processing_workflow.md](docs/processing_workflow.md) |
| 参数设置 | CiteSpace 6.4.R2 (64-bit, Windows) | 清洗后数据 | 分析项目文件 | [parameter_settings.md](docs/parameter_settings.md) |
| 结果解读 | — | 可视化图谱 | 文字说明 (≥200字/图) | [interpretation_guide.md](docs/interpretation_guide.md) |

## 分析维度与研究问题对应

| 输出 | 分析维度 | 研究问题 | 解读要求 |
|:---|:---|:---|:---|
| **图1** | 文献共被引网络 / 关键词聚类 | 知识基础是什么？ | ≥200字，含聚类结构、关键节点、时间特征 |
| **图2** | 时间线图 / 突现图 | 趋势如何演化？ | ≥200字，含演化阶段、突现词、聚类持续时间 |
| **图3** | 作者合作网络 / 机构地图 | 谁在推动这个领域？ | ≥200字，含核心作者、网络结构、机构分布 |
| **表1** | Top 10 里程碑论文 | 领域奠基性文献 | ≥200字，含四项指标解读、主题分布、关键文献分析 |
