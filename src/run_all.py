#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
批量运行所有数据分析脚本（增强版）
用途：一键执行完整的数据处理流程
"""

import sys
import os
import subprocess
import time

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config import ensure_directories, print_config

# 脚本执行顺序（按依赖关系排列）
PIPELINE = [
    {
        'name': '数据验证',
        'script': 'data_validation.py',
        'description': '检查输入数据完整性和质量',
        'optional': False
    },
    {
        'name': '年度发文量统计',
        'script': 'yearly_stats.py',
        'description': '统计各年度发文量趋势',
        'optional': False
    },
    {
        'name': '高频关键词统计',
        'script': 'keyword_stats.py',
        'description': '提取 Top 50 高频关键词',
        'optional': False
    },
    {
        'name': '核心作者与机构统计',
        'script': 'author_institution_stats.py',
        'description': '统计核心作者和机构发文量',
        'optional': False
    },
    {
        'name': '网络指标模板生成',
        'script': 'network_metrics.py',
        'description': '生成网络质量指标记录模板',
        'optional': True
    },
    {
        'name': '突现词模板生成',
        'script': 'burst_detection.py',
        'description': '生成突现词数据录入模板',
        'optional': True
    },
    {
        'name': '解读初稿生成',
        'script': 'interpretation_generator.py',
        'description': '基于数据生成图表解读初稿',
        'optional': True
    }
]

def run_script(script_name, script_dir):
    """运行单个脚本"""
    script_path = os.path.join(script_dir, script_name)

    if not os.path.exists(script_path):
        print(f"  ⚠ 脚本不存在: {script_name}")
        return False

    try:
        result = subprocess.run(
            [sys.executable, script_path],
            capture_output=False,
            text=True,
            check=True
        )
        return True
    except subprocess.CalledProcessError as e:
        print(f"  ✗ 运行失败 (返回码: {e.returncode})")
        return False
    except Exception as e:
        print(f"  ✗ 运行错误: {e}")
        return False

def main():
    print("=" * 70)
    print("CiteSpace 文献计量分析 - 完整数据处理流程")
    print("=" * 70)

    # 显示配置
    print_config()

    # 确保目录存在
    print("\n正在初始化目录结构...")
    ensure_directories()

    # 确定脚本目录
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # 执行流程
    print(f"\n开始执行数据处理流程...")
    print("=" * 70)

    results = []
    start_time = time.time()

    for i, step in enumerate(PIPELINE, 1):
        print(f"\n[{i}/{len(PIPELINE)}] {step['name']}")
        print(f"  说明: {step['description']}")
        print(f"  脚本: {step['script']}")

        step_start = time.time()
        success = run_script(step['script'], script_dir)
        step_time = time.time() - step_start

        status = "✓ 成功" if success else "✗ 失败"
        if step['optional'] and not success:
            status = "⚠ 跳过（可选步骤）"

        print(f"  状态: {status} ({step_time:.1f}s)")

        results.append({
            'name': step['name'],
            'success': success,
            'optional': step['optional'],
            'time': step_time
        })

    # 汇总报告
    total_time = time.time() - start_time

    print(f"\n{'=' * 70}")
    print("执行汇总")
    print(f"{'=' * 70}")

    success_count = sum(1 for r in results if r['success'])
    required_count = sum(1 for r in results if not r['optional'])
    required_success = sum(1 for r in results if r['success'] and not r['optional'])

    print(f"\n总步骤: {len(results)}")
    print(f"成功: {success_count}/{len(results)}")
    print(f"必需步骤成功: {required_success}/{required_count}")
    print(f"总耗时: {total_time:.1f} 秒")

    # 失败项
    failed = [r for r in results if not r['success'] and not r['optional']]
    if failed:
        print(f"\n失败的必需步骤:")
        for f in failed:
            print(f"  ✗ {f['name']}")

    # 输出文件清单
    print(f"\n生成的文件:")
    output_files = [
        "results/statistics/yearly_publications.csv",
        "results/statistics/top_keywords.csv",
        "results/statistics/top_authors.csv",
        "results/statistics/top_institutions.csv",
        "results/statistics/network_metrics_template.csv",
        "results/interpretation/interpretation_draft.md",
    ]

    for f in output_files:
        full_path = os.path.join(os.path.dirname(script_dir), f)
        exists = os.path.exists(full_path)
        status = "✓" if exists else "✗"
        print(f"  {status} {f}")

    print(f"\n{'=' * 70}")
    print("下一步操作:")
    print("  1. 在 CiteSpace 中导入清洗后的数据进行分析")
    print("  2. 将 CiteSpace 导出的网络数据放入 results/citespace_export/")
    print("  3. 运行 citespace_postprocess.py 和 centrality_calc.py 处理结果")
    print("  4. 填写 network_metrics_template.csv 中的网络指标")
    print("  5. 根据 interpretation_draft.md 完善图表解读")
    print(f"{'=' * 70}")

if __name__ == "__main__":
    main()
