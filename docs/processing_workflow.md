# 数据处理流程

> 本文档详细记录从原始数据到最终分析结果的完整处理流程，确保研究可复现。

---

## 流程概览

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│  1. 数据获取     │────▶│  2. 数据清洗     │────▶│  3. 格式转换     │
│  (Web of Science)│     │  (Python脚本)    │     │  (CiteSpace导入) │
└─────────────────┘     └─────────────────┘     └─────────────────┘
                                                        │
                                                        ▼
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│  6. 结果解读     │◀────│  5. 可视化输出   │◀────│  4. 参数设置     │
│  (图表分析)      │     │  (CiteSpace)     │     │  (CiteSpace)     │
└─────────────────┘     └─────────────────┘     └─────────────────┘
```

---

## 1. 数据获取

### 1.1 数据库与检索策略

| 项目 | 内容 |
|:---|:---|
| 数据库 | Web of Science Core Collection |
| 检索日期 | 2026年3月26日 |
| 检索式 | `TS=("third generation semiconductor" OR "wide band gap semiconductor" OR "silicon carbide" OR SiC OR "gallium nitride" OR GaN)` |
| 时间范围 | 2020–2026 |
| 语言 | English |
| 文献类型 | Article, Review, Proceedings Paper |

### 1.2 原始数据规模

| 指标 | 数值 |
|:---|:---|
| 检索命中量 | 4,369 篇 |
| 导出格式 | Plain Text (.txt), Full Record and Cited References |
| 导出字段 | 完整记录（含标题、作者、机构、摘要、关键词、参考文献、被引频次等） |

### 1.3 数据合并

由于 Web of Science 单次导出限制，检索结果分多次下载后合并为单一文件 `download_total.txt`。

---

## 2. 数据清洗

### 2.1 清洗工具

- **语言**: Python 3.x
- **脚本**: `wos_data_cleaning.py`（见 `/scripts/` 目录）
- **依赖**: 仅使用 Python 标准库（`re`, `os`, `collections`）

### 2.2 清洗步骤

#### Step 1: 解析记录
- 将合并后的 WoS 文本按记录分隔符拆分为独立条目
- 每条记录以 `PT `（Publication Type）开头，以 `ER`（End of Record）结尾

#### Step 2: DOI 去重
- **策略**: 以 DOI 为唯一标识符去重，保留首次出现的记录
- **兜底方案**: 无 DOI 的记录使用 "标题 + 出版年" 组合键去重
- **结果**: 4,369 篇 → 3,000 篇（去重 1,369 篇，去重率 31.33%）

#### Step 3: 同义词合并
- **目标**: 统一术语表述，避免同一概念被识别为不同节点
- **处理字段**: 标题（TI）、摘要（AB）、作者关键词（DE）、Keywords Plus（ID）
- **示例映射**:

| 原始表述 | 标准化后 |
|:---|:---|
| silicon carbide / Silicon Carbide | SiC |
| gallium nitride / Gallium Nitride | GaN |
| wide band gap / wide bandgap | WBG |
| third generation semiconductor | WBG |

#### Step 4: 机构名称标准化
- **目标**: 合并同一机构的不同写法
- **处理字段**: 机构地址（C1）
- **示例映射**:

| 原始表述 | 标准化后 |
|:---|:---|
| Chinese Acad Sci / CAS | Chinese Academy of Sciences |
| Tsinghua Univ | Tsinghua University |
| Cree Inc / Cree | Wolfspeed |

#### Step 5: 作者名消歧
- **目标**: 统一作者姓名格式，减少同名异写
- **处理字段**: 作者（AU）
- **策略**: 标准化大小写和空格格式，建立别名映射表

### 2.3 清洗输出

| 文件 | 说明 |
|:---|:---|
| `wos_cleaned_for_citespace.txt` | 清洗后的 CiteSpace 可识别格式 |
| `cleaning_report.txt` | 清洗统计报告（去重数量、同义词替换次数等） |

---

## 3. 数据格式转换

### 3.1 CiteSpace 输入格式要求

CiteSpace 6.4.R2 支持直接导入 Web of Science 纯文本格式（Plain Text），无需额外转换。

### 3.2 导入步骤

1. 打开 CiteSpace 6.4.R2
2. 选择 **Data** → **Import/Export** → **WoS** 
3. 选择清洗后的数据文件 `wos_cleaned_for_citespace.txt`
4. 确认数据成功导入（检查记录数是否为 3,000）

### 3.3 数据筛选（在 CiteSpace 中完成）

在 CiteSpace 中进一步筛选文献类型，仅保留 **Article** 和 **Review**：
- 原始清洗数据: 3,000 篇
- 筛选后用于分析: **2,014 篇**

---

## 4. 参数设置

详见 [parameter_settings.md](parameter_settings.md)

---

## 5. 可视化输出

基于 2,014 篇文献，生成以下分析图谱：

| 图谱编号 | 图谱类型 | 研究问题 | 对应文件 |
|:---|:---|:---|:---|
| 图1 | 文献共被引网络图 / 关键词聚类图 | 知识基础是什么？ | `results/networks/cocitation_network.png` |
| 图2 | 时间线图 / 突现图 | 趋势如何演化？ | `results/networks/timeline_view.png` |
| 图3 | 作者合作网络图 / 机构合作地图 | 谁在推动这个领域？ | `results/networks/author_collaboration.png` |
| 表1 | Top 10 里程碑论文列表 | 领域奠基性文献 | `results/statistics/top10_milestone.csv` |

---

## 6. 结果解读

详见 [interpretation_guide.md](interpretation_guide.md)

---

## 可复现性声明

| 项目 | 版本/信息 |
|:---|:---|
| 数据库 | Web of Science Core Collection |
| 检索日期 | 2026年3月26日 |
| 清洗脚本 | `wos_data_cleaning.py` |
| 分析软件 | CiteSpace 6.4.R2 (64-bit) |
| 操作系统 | Windows |
| 分析日期 | 2026年5月30日 |

> **注意**: 由于 Web of Science 数据库持续更新，不同日期检索结果可能存在细微差异。
