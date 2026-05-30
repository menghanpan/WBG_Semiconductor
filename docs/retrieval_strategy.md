# 检索策略详细说明

> 本文档详细记录文献检索的数据库选择、检索式构建、检索执行过程及结果，确保研究数据来源透明、可复现。

---

## 1. 数据库选择

| 项目 | 内容 |
|:---|:---|
| **数据库** | Web of Science Core Collection |
| **子库** | SCI-EXPANDED, SSCI, A&HCI, CPCI-S, CPCI-SSH, ESCI |
| **访问方式** | 学校图书馆VPN |
| **检索日期** | 2026年3月26日 |
| **检索平台** | Web of Science 网页版 |

### 选择理由

Web of Science Core Collection 是文献计量学研究的**首选数据库**，原因如下：

1. **数据完整性**：提供完整的引文信息（参考文献列表），支持共被引分析
2. **字段标准化**：作者、机构、关键词等字段格式统一，便于后续清洗
3. **学科覆盖**：SCI-EXPANDED 覆盖工程技术领域，与本研究主题（宽禁带半导体功率器件）高度匹配
4. **CiteSpace 兼容**：原生支持 WoS 纯文本格式导入，无需额外转换

---

## 2. 检索式构建

### 2.1 检索主题

宽禁带半导体功率器件（Wide Band Gap Semiconductor Power Devices）

### 2.2 检索词选择逻辑

| 检索词 | 变体形式 | 选择理由 |
|:---|:---|:---|
| **third generation semiconductor** | 无 | 中文语境下"第三代半导体"的英文对应表述 |
| **wide band gap semiconductor** | wide bandgap semiconductor | 领域标准术语，描述带隙宽度 > 2.3 eV 的半导体材料 |
| **silicon carbide** | SiC | 碳化硅，第三代半导体核心材料之一，功率器件主流材料 |
| **SiC** | silicon carbide | 材料缩写形式，文献中高频出现 |
| **gallium nitride** | GaN | 氮化镓，第三代半导体核心材料之一，高频/功率器件主流材料 |
| **GaN** | gallium nitride | 材料缩写形式，文献中高频出现 |

> **未纳入检索词说明**：
> - 未纳入 "diamond"、"Ga₂O₃" 等材料：这些材料目前研究规模较小，纳入后会引入大量噪声
> - 未纳入具体器件术语（如 MOSFET、HEMT、SBD）：这些器件也可能基于 Si/Ge 等传统材料，会引入无关文献
> - 采用**材料层级**检索而非**器件层级**检索，确保查全率与查准率的平衡

### 2.3 检索式

```
TS=("third generation semiconductor" OR "wide band gap semiconductor" OR "silicon carbide" OR SiC OR "gallium nitride" OR GaN)
AND PY=2020-2026
AND LA=English
AND DT=("Article" OR "Review" OR "Proceedings Paper")
```

### 2.4 检索式解析

| 字段 | 含义 | 设置值 | 作用 |
|:---|:---|:---|:---|
| **TS** | Topic（主题） | 见上 | 在标题、摘要、关键词中检索 |
| **PY** | Publication Year（出版年） | 2020–2026 | 限定时间范围 |
| **LA** | Language（语言） | English | 限定英文文献，确保分析一致性 |
| **DT** | Document Type（文献类型） | Article, Review, Proceedings Paper | 限定学术性文献，排除会议摘要、编辑材料等 |

---

## 3. 检索执行过程

### 3.1 检索步骤

1. 登录 Web of Science 网页版
2. 选择 **Core Collection** 数据库
3. 进入 **Advanced Search**（高级检索）界面
4. 输入上述检索式
5. 点击 **Search** 执行检索
6. 记录检索结果数量及检索历史编号

### 3.2 检索结果

| 指标 | 数值 |
|:---|:---|
| 检索命中量 | **4,369 篇** |
| 检索历史编号 | #X（Web of Science 自动生成） |

---

## 4. 数据导出

### 4.1 导出设置

| 项目 | 设置 |
|:---|:---|
| **导出格式** | Plain Text (.txt) |
| **记录内容** | Full Record and Cited References |
| **排序方式** | Publication Date（出版日期，升序） |
| **文件编码** | UTF-8 |

### 4.2 导出字段（Full Record）

Web of Science Full Record 包含以下字段：

| 字段标签 | 字段名 | 本研究用途 |
|:---|:---|:---|
| PT | Publication Type | 筛选 Article / Review |
| AU | Author | 作者合作分析 |
| AF | Author Full Name | 作者消歧辅助 |
| TI | Title | 文本分析、同义词替换 |
| SO | Source Title | 期刊分析 |
| LA | Language | 确认语言筛选 |
| DT | Document Type | 筛选文献类型 |
| DE | Author Keywords | 关键词共现分析 |
| ID | Keywords Plus | 补充关键词分析 |
| AB | Abstract | 主题分析 |
| C1 | Author Address | 机构合作分析 |
| RP | Reprint Address | 通讯作者信息 |
| EM | E-mail Address | 辅助机构识别 |
| CR | Cited References | 共被引分析 |
| NR | Cited Reference Count | 引文分析 |
| TC | Times Cited | 影响力分析 |
| Z9 | Total Times Cited | 总被引频次 |
| PU | Publisher | 出版商信息 |
| PI | Publisher City | 出版地 |
| PA | Publisher Address | 出版地址 |
| SN | ISSN | 期刊识别 |
| EI | eISSN | 电子期刊识别 |
| BN | ISBN | 图书识别 |
| J9 | 29-Character Source Abbreviation | 期刊缩写 |
| JI | ISO Source Abbreviation | ISO 期刊缩写 |
| PD | Publication Date | 出版日期 |
| PY | Publication Year | 时间趋势分析 |
| VL | Volume | 卷号 |
| IS | Issue | 期号 |
| PN | Part Number | 部分号 |
| SU | Supplement | 增刊 |
| SI | Special Issue | 特刊 |
| MA | Meeting Abstract | 会议摘要 |
| BP | Beginning Page | 起始页 |
| EP | Ending Page | 结束页 |
| AR | Article Number | 文章编号 |
| DI | DOI | 去重标识符 |
| D2 | Book DOI | 图书 DOI |
| EA | Early Access Date | 早期访问日期 |
| PG | Page Count | 页数 |
| WC | Web of Science Categories | 学科分类 |
| SC | Research Areas | 研究领域 |
| GA | Document Delivery Number | 文献传递号 |
| UT | Unique Article Identifier | 唯一标识符 |
| PM | PubMed ID | PubMed 编号 |
| OA | Open Access Indicator | 开放获取标识 |
| HC | ESI Highly Cited Paper | 高被引论文标识 |
| HP | ESI Hot Paper | 热点论文标识 |
| DA | Date this report was generated | 报告生成日期 |
| ER | End of Record | 记录结束标记 |
| EF | End of File | 文件结束标记 |

### 4.3 导出过程

由于 Web of Science 单次导出限制（最多 500 条记录），4,369 篇文献分 **9 次** 导出：

| 批次 | 记录范围 | 文件名 |
|:---|:---|:---|
| 1 | 1–500 | savedrecs_1.txt |
| 2 | 501–1000 | savedrecs_2.txt |
| 3 | 1001–1500 | savedrecs_3.txt |
| 4 | 1501–2000 | savedrecs_4.txt |
| 5 | 2001–2500 | savedrecs_5.txt |
| 6 | 2501–3000 | savedrecs_6.txt |
| 7 | 3001–3500 | savedrecs_7.txt |
| 8 | 3501–4000 | savedrecs_8.txt |
| 9 | 4001–4369 | savedrecs_9.txt |

### 4.4 数据合并

使用文本编辑器或命令行工具将 9 个文件合并为单一文件：

```bash
# Windows CMD
copy /b savedrecs_1.txt + savedrecs_2.txt + ... + savedrecs_9.txt wos_raw_merged.txt

# 或 PowerShell
Get-Content savedrecs_*.txt | Set-Content wos_raw_merged.txt
```

合并后文件：`wos_raw_merged.txt`

---

## 5. 检索策略评估

### 5.1 查全率评估

| 评估方式 | 结果 |
|:---|:---|
| 与已知核心文献比对 | 领域经典文献（如 [关键文献1]、[关键文献2]）均被命中 |
| 与综述文献参考文献比对 | 随机抽取 5 篇综述的参考文献，命中率为 XX% |

### 5.2 查准率评估

| 评估方式 | 结果 |
|:---|:---|
| 随机抽样检查 | 抽取前 100 条记录人工判读，相关度为 XX% |
| 关键词分布检查 | 高频关键词均为领域核心术语（SiC、GaN、power device 等） |

---

## 6. 可复现性声明

| 项目 | 信息 |
|:---|:---|
| 数据库 | Web of Science Core Collection |
| 检索日期 | 2026年X月X日 |
| 检索式 | 见第 2.3 节 |
| 检索结果 | 4,369 篇 |
| 导出格式 | Plain Text, Full Record and Cited References |
| 合并文件 | wos_raw_merged.txt |

> **声明**：Web of Science 数据库每日更新，不同日期检索结果可能存在细微差异。本研究检索日期为 2026年3月26日，后续研究者如需完全复现，建议在同一日期或相近时间段执行检索。
