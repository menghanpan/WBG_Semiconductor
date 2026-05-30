
# CiteSpace 参数设置

> 本文档记录 CiteSpace 6.4.R2 (64-bit) 的完整参数配置，确保分析结果可复现。

---

## 软件环境

| 项目 | 信息 |
|:---|:---|
| 软件名称 | CiteSpace |
| 版本号 | 6.4.R2 (64-bit) |
| 运行环境 | Windows |
| 数据路径 | `data/citespace/` |
| 项目名 | WBG_Semiconductor_2020-2026 |

---

## 全局参数设置

### 时间切片（Time Slicing）

| 参数 | 设置值 | 说明 |
|:---|:---|:---|
| From | 2020 JAN | 分析起始时间 |
| To | 2026 DEC | 分析终止时间 |
| Years Per Slice | 1 | 每个时间切片为 1 年 |
| 切片数量 | 7 | 2020, 2021, 2022, 2023, 2024, 2025, 2026 |

> **设置理由**: 本研究时间跨度为 7 年（2020–2026），以 1 年为切片单位可捕捉年度演化特征，同时保证每个切片内样本量充足。

---

## 节点类型与阈值设置

### 通用设置

| 参数 | 设置值 | 说明 |
|:---|:---|:---|
| Selection Criteria | g-index | 筛选算法 |
| g-index | 25 | 每个时间切片选取 g-index 排名前 25 的节点 |
| Top N / Top N% | 未使用 | 采用 g-index 替代 |

> **g-index 说明**: g-index 是 h-index 的改进版，综合考虑论文数量和引用质量。设置 g=25 可在控制网络规模的同时保留高影响力节点，避免网络过于稀疏或密集。

---

## 各分析维度参数

### 维度 1: 文献共被引分析（Document Co-citation）

| 参数 | 设置值 |
|:---|:---|
| Node Types | Cited Reference |
| Selection Criteria | g-index = 25 |
| Pruning | Pathfinder + Pruning sliced networks |
| 可视化 | Cluster View（聚类视图） |

**聚类标签来源**: Keywords / Terms

---

### 维度 2: 关键词聚类分析（Keyword Clustering）

| 参数 | 设置值 |
|:---|:---|
| Node Types | Keyword |
| Selection Criteria | g-index = 25 |
| Pruning | Pathfinder + Pruning sliced networks |
| 聚类算法 | LLR（Log-Likelihood Ratio） |

**聚类标签提取算法**: LLR（默认）+ MI（Mutual Information）辅助验证

---

### 维度 3: 时间线分析（Timeline View）

| 参数 | 设置值 |
|:---|:---|
| Node Types | Cited Reference / Keyword |
| Selection Criteria | g-index = 25 |
| 视图类型 | Timeline View |
| 聚类排序 | 按聚类规模或 Silhouette 值排序 |

---

### 维度 4: 突现检测（Burst Detection）

| 参数 | 设置值 |
|:---|:---|
| Node Types | Keyword / Cited Reference |
| Minimum Duration | 2 年 |
| γ (Gamma) | 1.0（默认） |

> **突现词说明**: 突现强度（Burst Strength）反映关键词/文献在特定时间段内被引频次的急剧增长，标识研究前沿和热点转移。

---

### 维度 5: 作者合作网络（Author Collaboration）

| 参数 | 设置值 |
|:---|:---|
| Node Types | Author |
| Selection Criteria | g-index = 25 |
| Pruning | Pathfinder |
| 网络类型 | Co-authorship Network |

---


## 网络修剪（Pruning）策略

| 参数 | 设置 | 说明 |
|:---|:---|:---|
| Pruning | Pathfinder + Pruning sliced networks | 保留网络骨架结构，去除冗余连接 |
| 网络简化 | 启用 | 提升可视化清晰度 |

> **Pathfinder 算法**: 基于最短路径原则修剪网络，保留最具代表性的连接关系，使网络结构更清晰、聚类更明确。

---

## 可视化参数

| 参数 | 设置值 |
|:---|:---|
| 节点大小 | 按频次/中心性比例缩放 |
| 节点颜色 | 按时间切片或聚类着色 |
| 连线粗细 | 按共现/共被引强度 |
| 标签显示 | 显示高频/高中心性节点标签 |
| 背景 | 白色 |

---

## 网络质量指标

分析完成后需记录以下指标，用于评估网络可靠性：

| 指标 | 说明 | 可接受范围 |
|:---|:---|:---|
| Modularity Q | 网络模块化程度 | Q > 0.3 表示聚类结构显著 |
| Weighted Mean Silhouette S | 聚类平均轮廓值 | S > 0.5 表示聚类合理 |
| Mean Cited Year | 平均被引年份 | 反映研究前沿性 |

---


