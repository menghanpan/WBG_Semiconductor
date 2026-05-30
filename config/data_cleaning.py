#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Web of Science 文献数据清洗脚本
用途：对 WoS 导出的全记录文本进行去重、同义词合并、机构标准化、作者消歧
输入：合并后的 WoS 全记录 .txt 文件（Full Record and Cited References）
输出：CiteSpace 可直接导入的 .txt 文件
日期：2026-05-30
"""

import re
import os
from collections import defaultdict, Counter

# ==================== 配置区域 ====================

INPUT_FILE = "wos_raw_merged.txt"      # 输入：合并后的原始 WoS 数据
OUTPUT_FILE = "wos_cleaned_for_citespace.txt"  # 输出：清洗后的 CiteSpace 数据
REPORT_FILE = "cleaning_report.txt"    # 清洗报告

# 同义词映射表
SYNONYM_MAP = {
    # 材料名称
    "silicon carbide": "SiC",
    "Silicon Carbide": "SiC",
    "SILICON CARBIDE": "SiC",
    "gallium nitride": "GaN",
    "Gallium Nitride": "GaN",
    "GALLIUM NITRIDE": "GaN",
    "wide band gap": "WBG",
    "Wide Band Gap": "WBG",
    "wide bandgap": "WBG",
    "Wide Bandgap": "WBG",
    "third generation semiconductor": "WBG",
    "Third Generation Semiconductor": "WBG",
    # 器件名称
    "metal oxide semiconductor field effect transistor": "MOSFET",
    "Metal Oxide Semiconductor Field Effect Transistor": "MOSFET",
    "high electron mobility transistor": "HEMT",
    "High Electron Mobility Transistor": "HEMT",
    "schottky barrier diode": "SBD",
    "Schottky Barrier Diode": "SBD",
}

# 机构标准化映射表
INSTITUTION_MAP = {
    # 中国科学院各院所统一
    "Chinese Acad Sci": "Chinese Academy of Sciences",
    "Chinese Academy of Sciences": "Chinese Academy of Sciences",
    "CAS": "Chinese Academy of Sciences",
    "中科院": "Chinese Academy of Sciences",
    # 清华大学
    "Tsinghua Univ": "Tsinghua University",
    "Tsinghua University": "Tsinghua University",
    "清华大学": "Tsinghua University",
    # 西安交通大学
    "Xi An Jiao Tong Univ": "Xi'an Jiaotong University",
    "Xi'an Jiaotong Univ": "Xi'an Jiaotong University",
    "Xi'an Jiaotong University": "Xi'an Jiaotong University",
    "Xian Jiaotong University": "Xi'an Jiaotong University",
    # 电子科技大学
    "Univ Elect Sci & Technol China": "University of Electronic Science and Technology of China",
    "University of Electronic Science and Technology of China": "University of Electronic Science and Technology of China",
    "UESTC": "University of Electronic Science and Technology of China",
    # 浙江大学
    "Zhejiang Univ": "Zhejiang University",
    "Zhejiang University": "Zhejiang University",
    # 英飞凌
    "Infineon Technol": "Infineon Technologies",
    "Infineon Technologies AG": "Infineon Technologies",
    "Infineon": "Infineon Technologies",
    # 安森美
    "ON Semiconductor": "onsemi",
    "ON Semi": "onsemi",
    "onsemi": "onsemi",
    # 意法半导体
    "STMicroelectronics": "STMicroelectronics",
    "ST Microelectronics": "STMicroelectronics",
    # Wolfspeed / Cree
    "Cree Inc": "Wolfspeed",
    "Cree": "Wolfspeed",
    "Wolfspeed Inc": "Wolfspeed",
    "Wolfspeed": "Wolfspeed",
}

# 作者名消歧规则（处理同名不同人、拼写变体）
AUTHOR_ALIAS = {
    # 格式: "变体形式": "标准形式"
    # "J. Zhang": "J. Zhang",
    # "J Zhang": "J. Zhang",
}

# ==================== 核心函数 ====================

def parse_wos_records(filepath):
    """
    解析 WoS 全记录文本文件，按记录拆分
    WoS 每条记录以 "PT " 开头，以 "ER\n" 结束
    """
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 按记录分隔符拆分
    records = []
    raw_records = re.split(r'(?=\nPT\s)', content)

    for raw in raw_records:
        raw = raw.strip()
        if raw.startswith('PT ') and 'ER' in raw:
            records.append(raw)

    return records


def extract_field(record, field_tag):
    """
    从单条记录中提取指定字段
    WoS 字段格式: "XX " 开头，后续行以 "   " 开头表示续行
    """
    pattern = rf'^{re.escape(field_tag)}\s(.*?)\n(?=[A-Z]{{2}}\s|ER)'
    match = re.search(pattern, record, re.MULTILINE | re.DOTALL)
    if match:
        # 处理续行（去除续行前缀空格）
        value = match.group(1)
        value = re.sub(r'\n\s+', ' ', value)
        return value.strip()
    return None


def extract_doi(record):
    """提取 DOI 字段"""
    doi = extract_field(record, 'DI ')
    if doi:
        # 清理 DOI 格式
        doi = doi.strip().lower()
        # 去除可能的 URL 前缀
        doi = re.sub(r'^https?://(dx\.)?doi\.org/', '', doi)
        return doi
    return None


def extract_title(record):
    """提取标题"""
    return extract_field(record, 'TI ')


def extract_authors(record):
    """提取作者列表（AU 字段）"""
    au_text = extract_field(record, 'AU ')
    if au_text:
        # 作者以分号或换行分隔
        authors = [a.strip() for a in re.split(r'[;\n]', au_text) if a.strip()]
        return authors
    return []


def extract_affiliations(record):
    """提取机构地址（C1 字段）"""
    c1_text = extract_field(record, 'C1 ')
    if c1_text:
        # 机构地址通常以 [作者名] 地址 格式出现
        # 提取机构名称部分
        affiliations = []
        lines = c1_text.split(';')
        for line in lines:
            # 去除作者名前缀，如 "[Zhang, J] "
            line = re.sub(r'\[.*?\]\s*', '', line).strip()
            if line:
                affiliations.append(line)
        return affiliations
    return []


def extract_keywords(record):
    """提取作者关键词（DE 字段）和 Keywords Plus（ID 字段）"""
    keywords = []

    de = extract_field(record, 'DE ')
    if de:
        keywords.extend([k.strip() for k in de.split(';') if k.strip()])

    id_field = extract_field(record, 'ID ')
    if id_field:
        keywords.extend([k.strip() for k in id_field.split(';') if k.strip()])

    return keywords


def extract_abstract(record):
    """提取摘要"""
    return extract_field(record, 'AB ')


def extract_year(record):
    """提取出版年份"""
    year = extract_field(record, 'PY ')
    if year:
        return year.strip()
    # 备选：从 PD（出版日期）或 EA（早期访问日期）提取
    pd = extract_field(record, 'PD ')
    if pd:
        match = re.search(r'\b(20\d{2})\b', pd)
        if match:
            return match.group(1)
    return None


def extract_document_type(record):
    """提取文献类型"""
    return extract_field(record, 'DT ')


def extract_references(record):
    """提取参考文献列表（CR 字段）"""
    cr_text = extract_field(record, 'CR ')
    if cr_text:
        refs = [r.strip() for r in cr_text.split(';') if r.strip()]
        return refs
    return []


def extract_cited_count(record):
    """提取被引频次"""
    tc = extract_field(record, 'TC ')
    if tc:
        match = re.search(r'\d+', tc)
        if match:
            return int(match.group())
    return 0


def extract_funding(record):
    """提取基金信息"""
    fu = extract_field(record, 'FU ')
    if fu:
        funds = [f.strip() for f in fu.split(';') if f.strip()]
        return funds
    return []


def apply_synonym_replacement(text, synonym_map):
    """应用同义词替换"""
    if not text:
        return text
    for old, new in synonym_map.items():
        # 使用单词边界匹配，避免部分替换
        pattern = rf'\b{re.escape(old)}\b'
        text = re.sub(pattern, new, text, flags=re.IGNORECASE)
    return text


def standardize_institution(institution_text, institution_map):
    """标准化机构名称"""
    if not institution_text:
        return institution_text

    # 先尝试完全匹配
    if institution_text in institution_map:
        return institution_map[institution_text]

    # 尝试部分匹配（提取主要机构名）
    for old, new in institution_map.items():
        if old.lower() in institution_text.lower():
            return new

    return institution_text


def disambiguate_author(author_name, author_alias):
    """作者名消歧"""
    if author_name in author_alias:
        return author_alias[author_name]

    # 标准化格式：确保首字母后有空格
    # 如 "ZhangJ" -> "Zhang J"
    standardized = re.sub(r'([A-Z][a-z]+)([A-Z])', r'\1 \2', author_name)

    if standardized in author_alias:
        return author_alias[standardized]

    return standardized


def clean_record(record, synonym_map, institution_map, author_alias):
    """
    对单条记录进行清洗
    返回清洗后的记录文本
    """
    # 1. 同义词替换（标题、摘要、关键词）
    # 替换标题
    ti = extract_field(record, 'TI ')
    if ti:
        new_ti = apply_synonym_replacement(ti, synonym_map)
        if new_ti != ti:
            record = record.replace(f'TI {ti}', f'TI {new_ti}', 1)

    # 替换摘要
    ab = extract_field(record, 'AB ')
    if ab:
        new_ab = apply_synonym_replacement(ab, synonym_map)
        if new_ab != ab:
            record = record.replace(f'AB {ab}', f'AB {new_ab}', 1)

    # 替换关键词
    de = extract_field(record, 'DE ')
    if de:
        new_de = apply_synonym_replacement(de, synonym_map)
        if new_de != de:
            record = record.replace(f'DE {de}', f'DE {new_de}', 1)

    id_field = extract_field(record, 'ID ')
    if id_field:
        new_id = apply_synonym_replacement(id_field, synonym_map)
        if new_id != id_field:
            record = record.replace(f'ID {id_field}', f'ID {new_id}', 1)

    # 2. 机构标准化（C1 字段）
    c1 = extract_field(record, 'C1 ')
    if c1:
        # 解析机构地址，替换机构名部分
        new_c1 = c1
        for old, new in institution_map.items():
            # 使用不区分大小写的替换
            pattern = re.compile(re.escape(old), re.IGNORECASE)
            new_c1 = pattern.sub(new, new_c1)
        if new_c1 != c1:
            record = record.replace(f'C1 {c1}', f'C1 {new_c1}', 1)

    # 3. 作者名消歧（AU 字段）
    au = extract_field(record, 'AU ')
    if au:
        authors = [a.strip() for a in au.split(';') if a.strip()]
        new_authors = [disambiguate_author(a, author_alias) for a in authors]
        new_au = '; '.join(new_authors)
        if new_au != au:
            record = record.replace(f'AU {au}', f'AU {new_au}', 1)

    # 4. 清理多余空白
    record = re.sub(r'\n\s*\n', '\n', record)

    return record


def deduplicate_by_doi(records):
    """
    按 DOI 去重
    保留第一条出现的记录
    """
    seen_dois = set()
    unique_records = []
    duplicate_count = 0
    no_doi_records = []

    for record in records:
        doi = extract_doi(record)

        if doi:
            if doi not in seen_dois:
                seen_dois.add(doi)
                unique_records.append(record)
            else:
                duplicate_count += 1
        else:
            # 没有 DOI 的记录，尝试用标题+年份去重
            title = extract_title(record)
            year = extract_year(record)
            fallback_key = f"{title}_{year}" if title and year else None

            if fallback_key and fallback_key not in seen_dois:
                seen_dois.add(fallback_key)
                unique_records.append(record)
            elif not fallback_key:
                no_doi_records.append(record)
            else:
                duplicate_count += 1

    return unique_records, duplicate_count, no_doi_records


def generate_report(original_count, unique_count, duplicate_count, 
                    no_doi_count, synonym_stats, institution_stats):
    """生成清洗报告"""
    report = []
    report.append("=" * 60)
    report.append("Web of Science 数据清洗报告")
    report.append("=" * 60)
    report.append(f"")
    report.append("【数据规模】")
    report.append(f"  原始记录数: {original_count}")
    report.append(f"  去重后记录数: {unique_count}")
    report.append(f"  重复记录数: {duplicate_count}")
    report.append(f"  无 DOI 记录数: {no_doi_count}")
    report.append(f"  去重率: {duplicate_count/original_count*100:.2f}%")
    report.append(f"")
    report.append("【同义词替换统计】")
    for term, count in synonym_stats.most_common():
        report.append(f"  {term}: {count} 次")
    report.append(f"")
    report.append("【机构标准化统计】")
    for inst, count in institution_stats.most_common():
        report.append(f"  {inst}: {count} 次")
    report.append(f"")
    report.append("=" * 60)

    return "\n".join(report)


def save_citespace_format(records, output_path):
    """
    保存为 CiteSpace 可识别的格式
    确保每条记录以 PT 开头，ER 结尾，文件以 EF 结尾
    """
    with open(output_path, 'w', encoding='utf-8') as f:
        for record in records:
            f.write(record + "\n")
        f.write("EF\n")
    print(f"已保存 {len(records)} 条记录到: {output_path}")


# ==================== 主程序 ====================

def main():
    print("=" * 60)
    print("Web of Science 数据清洗工具")
    print("=" * 60)
    print(f"输入文件: {INPUT_FILE}")
    print(f"输出文件: {OUTPUT_FILE}")
    print()

    # 1. 读取原始数据
    print("[1/5] 读取原始数据...")
    if not os.path.exists(INPUT_FILE):
        print(f"错误: 找不到输入文件 {INPUT_FILE}")
        print("请将合并后的 WoS 数据命名为 'wos_raw_merged.txt' 放在同目录下")
        return

    records = parse_wos_records(INPUT_FILE)
    original_count = len(records)
    print(f"      读取到 {original_count} 条记录")

    # 2. 按 DOI 去重
    print("[2/5] 按 DOI 去重...")
    unique_records, duplicate_count, no_doi_records = deduplicate_by_doi(records)
    no_doi_count = len(no_doi_records)
    print(f"      去重后: {len(unique_records)} 条")
    print(f"      重复记录: {duplicate_count} 条")
    print(f"      无 DOI 记录: {no_doi_count} 条")

    # 3. 数据清洗
    print("[3/5] 数据清洗（同义词替换、机构标准化、作者消歧）...")
    synonym_stats = Counter()
    institution_stats = Counter()
    cleaned_records = []

    for i, record in enumerate(unique_records):
        # 统计同义词替换前
        original_text = extract_field(record, 'TI ') or ""
        original_text += extract_field(record, 'AB ') or ""
        original_text += extract_field(record, 'DE ') or ""

        # 清洗记录
        cleaned = clean_record(record, SYNONYM_MAP, INSTITUTION_MAP, AUTHOR_ALIAS)

        # 统计同义词替换次数
        new_text = extract_field(cleaned, 'TI ') or ""
        new_text += extract_field(cleaned, 'AB ') or ""
        new_text += extract_field(cleaned, 'DE ') or ""

        for old, new in SYNONYM_MAP.items():
            count = original_text.lower().count(old.lower()) - new_text.lower().count(old.lower())
            if count > 0:
                synonym_stats[new] += count

        # 统计机构标准化
        original_c1 = extract_field(record, 'C1 ') or ""
        for old, new in INSTITUTION_MAP.items():
            if old.lower() in original_c1.lower():
                institution_stats[new] += 1

        cleaned_records.append(cleaned)

        if (i + 1) % 500 == 0:
            print(f"      已处理 {i + 1}/{len(unique_records)} 条...")

    print(f"      清洗完成")

    # 4. 保存清洗后的数据
    print("[4/5] 保存清洗后的数据...")
    save_citespace_format(cleaned_records, OUTPUT_FILE)

    # 5. 生成报告
    print("[5/5] 生成清洗报告...")
    report = generate_report(
        original_count, 
        len(unique_records), 
        duplicate_count,
        no_doi_count,
        synonym_stats,
        institution_stats
    )

    with open(REPORT_FILE, 'w', encoding='utf-8') as f:
        f.write(report)
    print(f"      报告已保存到: {REPORT_FILE}")

    print()
    print("=" * 60)
    print("清洗完成!")
    print(f"最终输出: {OUTPUT_FILE} ({len(cleaned_records)} 条记录)")
    print("=" * 60)


if __name__ == "__main__":
    main()
