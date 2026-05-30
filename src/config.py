#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
配置管理模块
用途：集中管理所有路径、参数和常量，方便统一修改
"""

import os

# ==================== 路径配置 ====================

# 项目根目录（相对于 src/ 目录）
PROJECT_ROOT = ".."

# 数据目录
DATA_DIR = os.path.join(PROJECT_ROOT, "data")
RAW_DATA_DIR = os.path.join(DATA_DIR, "raw")
PROCESSED_DATA_DIR = os.path.join(DATA_DIR, "processed")

# 结果目录
RESULTS_DIR = os.path.join(PROJECT_ROOT, "results")
STATISTICS_DIR = os.path.join(RESULTS_DIR, "statistics")
NETWORKS_DIR = os.path.join(RESULTS_DIR, "networks")
INTERPRETATION_DIR = os.path.join(RESULTS_DIR, "interpretation")
CITESPACE_EXPORT_DIR = os.path.join(RESULTS_DIR, "citespace_export")

# 文档目录
DOCS_DIR = os.path.join(PROJECT_ROOT, "docs")

# ==================== 文件名配置 ====================

# 原始数据文件
RAW_MERGED_FILE = os.path.join(PROCESSED_DATA_DIR, "wos_raw_merged.txt")
CLEANED_FILE = os.path.join(PROCESSED_DATA_DIR, "wos_cleaned_for_citespace.txt")

# 清洗报告
CLEANING_REPORT = os.path.join(PROCESSED_DATA_DIR, "cleaning_report.txt")

# 统计输出文件
YEARLY_STATS_FILE = os.path.join(STATISTICS_DIR, "yearly_publications.csv")
KEYWORD_STATS_FILE = os.path.join(STATISTICS_DIR, "top_keywords.csv")
AUTHOR_STATS_FILE = os.path.join(STATISTICS_DIR, "top_authors.csv")
INSTITUTION_STATS_FILE = os.path.join(STATISTICS_DIR, "top_institutions.csv")
NETWORK_METRICS_FILE = os.path.join(STATISTICS_DIR, "network_metrics_template.csv")
BURST_KEYWORDS_FILE = os.path.join(STATISTICS_DIR, "burst_keywords.csv")
BURST_ACTIVE_FILE = os.path.join(STATISTICS_DIR, "burst_active_keywords.csv")
CENTRALITY_FILE = os.path.join(STATISTICS_DIR, "node_centrality_analysis.csv")
TIMELINE_FILE = os.path.join(STATISTICS_DIR, "timeline_analysis.csv")
MILESTONE_FILE = os.path.join(STATISTICS_DIR, "top10_milestone_candidates.csv")

# 解读文件
INTERPRETATION_DRAFT = os.path.join(INTERPRETATION_DIR, "interpretation_draft.md")

# ==================== 分析参数配置 ====================

# CiteSpace 参数
CITESPACE_VERSION = "6.4.R2"
TIME_SLICE_FROM = "2020 JAN"
TIME_SLICE_TO = "2026 DEC"
YEARS_PER_SLICE = 1
SELECTION_CRITERIA = "g-index"
G_INDEX_VALUE = 25
PRUNING_METHOD = "Pathfinder + Pruning sliced networks"

# 统计参数
TOP_N_KEYWORDS = 50
TOP_N_AUTHORS = 20
TOP_N_INSTITUTIONS = 20
TOP_N_MILESTONE = 10

# 突现检测参数
BURST_MIN_DURATION = 2
BURST_GAMMA = 1.0

# ==================== 同义词映射 ====================

SYNONYM_MAP = {
    "silicon carbide": "SiC",
    "Silicon Carbide": "SiC",
    "gallium nitride": "GaN",
    "Gallium Nitride": "GaN",
    "wide band gap": "WBG",
    "Wide Band Gap": "WBG",
    "wide bandgap": "WBG",
    "third generation semiconductor": "WBG",
    "metal oxide semiconductor field effect transistor": "MOSFET",
    "high electron mobility transistor": "HEMT",
    "schottky barrier diode": "SBD",
}

# ==================== 机构标准化映射 ====================

INSTITUTION_MAP = {
    "Chinese Acad Sci": "Chinese Academy of Sciences",
    "CAS": "Chinese Academy of Sciences",
    "Tsinghua Univ": "Tsinghua University",
    "Xi An Jiao Tong Univ": "Xi'an Jiaotong University",
    "Univ Elect Sci & Technol China": "University of Electronic Science and Technology of China",
    "UESTC": "University of Electronic Science and Technology of China",
    "Zhejiang Univ": "Zhejiang University",
    "Infineon Technol": "Infineon Technologies",
    "ON Semiconductor": "onsemi",
    "Cree Inc": "Wolfspeed",
    "Cree": "Wolfspeed",
}

# ==================== 工具函数 ====================

def ensure_directories():
    """确保所有必要的目录存在"""
    dirs = [
        RAW_DATA_DIR,
        PROCESSED_DATA_DIR,
        STATISTICS_DIR,
        NETWORKS_DIR,
        INTERPRETATION_DIR,
        CITESPACE_EXPORT_DIR,
        DOCS_DIR,
    ]

    for d in dirs:
        os.makedirs(d, exist_ok=True)

    print("所有目录已创建/确认")

def print_config():
    """打印当前配置"""
    print("=" * 60)
    print("项目配置信息")
    print("=" * 60)
    print(f"\nCiteSpace 版本: {CITESPACE_VERSION}")
    print(f"时间切片: {TIME_SLICE_FROM} - {TIME_SLICE_TO}")
    print(f"每切片年数: {YEARS_PER_SLICE}")
    print(f"筛选策略: {SELECTION_CRITERIA} = {G_INDEX_VALUE}")
    print(f"修剪方法: {PRUNING_METHOD}")
    print(f"\n数据路径:")
    print(f"  原始数据: {RAW_DATA_DIR}")
    print(f"  处理后数据: {PROCESSED_DATA_DIR}")
    print(f"  统计结果: {STATISTICS_DIR}")
    print(f"  网络图谱: {NETWORKS_DIR}")
    print(f"  CiteSpace导出: {CITESPACE_EXPORT_DIR}")
    print("=" * 60)

if __name__ == "__main__":
    ensure_directories()
    print_config()
