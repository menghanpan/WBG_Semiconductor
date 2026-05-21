# 文献研究概要：2020-2025年宽禁带半导体功率器件的发展与挑战
自2020年以来，由于全球对能源转换效率、系统小型化及高功率密度的迫切需求，以碳化硅 (SiC) 和 氮化镓 (GaN) 为代表的第三代（宽禁带）半导体研究进入了爆发期。与传统硅 (Si) 基器件相比，这些材料具有更高的击穿电场、更高的热导率和更快的饱和电子漂移速度。本检索范围涵盖了从底层物理结构（晶体管、二极管）到应用前端的关键技术演进。
# 项目成员与职责

组长：张娜   整体安排和相关数据获取与规划   | data/raw/ |

组员：魏瑜琤  撰写并完善项目报告，做报告分析。 | reports/paper |

组员：邹星云   处理相关代码 | config/data/processed/  |

组员：潘梦涵   图谱构建与计量分析，完成数据分析并输出结果报告。  | outputs/docs/    |

# 检索式
v0.2
TS=( “third generation semiconductor” OR “wide-bandgap semiconductor” OR “silicon carbide” OR SiC OR “gallium nitride” OR GaN )
AND TS=(“MOSFET” OR “HEMT” OR “SBD” OR “transistor” OR “diode”)
AND PY=2020-2025
AND LA=English
AND DT=("Article" OR "Review" OR "Proceedings Paper")


# 规范化目录结构re

项目文件分类为“原始数据”、“处理逻辑与分析产出”。具体目录说明如下zheng：

- **config/**：存放项目配置文件如查询参数。
- **data/raw/**：原始数据及其导入系统的结构。
- **data/processed/**：经过处理的数据集。
- **src/**：Python脚本来处理和分析数据。
- **outputs/**：分析结果，包括报告和可视化图表。
- **reports/**：最终项目报告。
- **paper/**：学术论文草稿及其相关参考资料。
- **README.md/**：项目说明文档。

# 项目核心里程碑 (Milestones)

# M1阶段：数据与检索方案验证（第4周末前）
- **阶段目标**：完成从数据获取到初步清洗和验证。
- **核心步骤**：
  - 验证配置文件准确性。
  - 定期检查数据质量报告。

# M2阶段：计量分析与图谱产出（第10周末前）
- **阶段目标**：构建完整的文献计量网络图谱。
- **核心步骤**：
  - 完成图谱分析，并输出详细结果。

# M3阶段：终稿与项目归档（第15周末前）
- **阶段目标**：编制详细的项目报告和学术论文。
- **核心步骤**：
  - 完成论文撰写与代码库的整理。
