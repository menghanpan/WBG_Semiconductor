# src/ 目录说明

本目录包含用于 CiteSpace 文献计量分析的 Python 辅助脚本，补充 CiteSpace 原生功能的不足，提供数据预处理、批量统计和结果后处理能力。

---

## 文件清单

### 核心脚本

| 脚本 | 用途 | 输入 | 输出 |
|:---|:---|:---|:---|
| `config.py` | 配置管理模块 | - | 路径/参数常量 |
| `merge_files.py` | 合并多个 WoS 导出文件 | `data/raw/savedrecs_*.txt` | `data/processed/wos_raw_merged.txt` |
| `data_validation.py` | 数据完整性验证 | `data/processed/wos_cleaned_for_citespace.txt` | 验证报告 |
| `yearly_stats.py` | 年度发文量统计 | 清洗后数据 | `results/statistics/yearly_publications.csv` |
| `keyword_stats.py` | 高频关键词统计 | 清洗后数据 | `results/statistics/top_keywords.csv` |
| `author_institution_stats.py` | 核心作者与机构统计 | 清洗后数据 | `top_authors.csv` + `top_institutions.csv` |
| `network_metrics.py` | 网络质量指标记录模板 | 手动填入 | `results/statistics/network_metrics_template.csv` |
| `burst_detection.py` | 突现词数据解析 | `results/statistics/burst_data.txt` | `results/statistics/burst_keywords.csv` |
| `timeline_extractor.py` | 时间线数据提取 | CiteSpace 导出数据 | `results/statistics/timeline_analysis.csv` |
| `centrality_calc.py` | 节点中心性计算 | CiteSpace 网络数据 | `results/statistics/node_centrality_analysis.csv` |
| `citespace_postprocess.py` | CiteSpace 结果后处理 | CiteSpace 导出节点/连线 | 标准化统计表格 |
| `interpretation_generator.py` | 解读文字辅助生成 | 各统计结果 CSV | `results/interpretation/interpretation_draft.md` |
| `run_all.py` | 批量运行所有脚本 | - | 全部统计结果 |

---

## 快速开始

### 完整流程

```bash
cd src

# 第一步：合并数据（如已合并可跳过）
python merge_files.py

# 第二步：运行完整分析流程
python run_all.py

# 第三步：在 CiteSpace 中分析后，处理导出数据
python citespace_postprocess.py
python centrality_calc.py
python timeline_extractor.py

# 第四步：生成解读初稿
python interpretation_generator.py
```

### 单独运行

```bash
cd src

# 仅运行数据验证
python data_validation.py

# 仅运行年度统计
python yearly_stats.py

# 仅运行关键词统计
python keyword_stats.py
```

---

## 依赖要求

- Python 3.7+
- 仅使用标准库，无需额外安装

---

## 与 CiteSpace 的分工

| 任务 | CiteSpace | Python 脚本 |
|:---|:---|:---|
| 网络构建与可视化 | ✅ | ❌ |
| 聚类分析 | ✅ | ❌ |
| 突现检测 | ✅ | ❌ |
| 多文件合并 | ❌ | ✅ |
| 数据完整性验证 | ❌ | ✅ |
| 高频关键词排序 | ⚠️ 需导出后处理 | ✅ 直接输出表格 |
| 作者/机构发文量 | ⚠️ 需导出后处理 | ✅ 直接输出表格 |
| 网络指标汇总 | ⚠️ 分散在各界面 | ✅ 标准化表格 |
| 突现词整理 | ⚠️ 需手动复制 | ✅ 结构化解析 |
| 中心性计算 | ⚠️ 需导出后处理 | ✅ 多种指标 |
| 时间线分析 | ⚠️ 需导出后处理 | ✅ 演化阶段划分 |
| 解读文字生成 | ❌ | ✅ 辅助初稿 |
| 批量重复操作 | ❌ | ✅ |

---

## 配置修改

如需修改路径或参数，编辑 `config.py`：

```python
# 修改 Top N 数量
TOP_N_KEYWORDS = 50      # 改为需要的数量
TOP_N_AUTHORS = 20

# 修改 CiteSpace 参数
G_INDEX_VALUE = 25       # 修改 g-index 值

# 添加同义词映射
SYNONYM_MAP = {
    "新词": "标准词",
    # ...
}
```

---

## 注意事项

1. **路径配置**：所有脚本使用相对路径，以 `src/` 为基准
2. **编码问题**：WoS 数据为 UTF-8，如遇乱码请检查编码
3. **数据更新**：重新运行脚本即可更新统计结果
4. **手动填入**：`network_metrics_template.csv` 需手动填入 CiteSpace 指标
5. **可选步骤**：带 `optional` 标记的步骤失败不影响主流程
