#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
快速测试数据读取功能
"""

import pandas as pd
import os
import glob

def quick_test():
    """快速测试"""
    
    print("=" * 50)
    print("🚀 快速测试Excel数据读取")
    print("=" * 50)
    
    # 查找Excel文件
    excel_files = glob.glob(os.path.join('orders', '*.xlsx'))
    
    if not excel_files:
        print("❌ 未找到Excel文件")
        return
    
    # 读取最新的文件
    latest_file = max(excel_files, key=os.path.getctime)
    print(f"📁 读取文件: {latest_file}")
    
    try:
        # 读取数据
        df = pd.read_excel(latest_file, engine='openpyxl')
        print(f"✅ 读取成功! 数据行数: {len(df)}")
        
        # 显示数据概览
        print(f"\n📊 数据概览:")
        print(f"   列名: {list(df.columns)}")
        print(f"   行数: {len(df)}")
        
        # 显示前几行
        print(f"\n📋 前3行数据:")
        for i, row in df.head(3).iterrows():
            print(f"   第{i+1}行: {row['订单号']} - {row['用户名']} - ¥{row['金额']} - 状态{row['状态']}")
        
        # 状态统计
        print(f"\n📈 状态分布:")
        status_counts = df['状态'].value_counts()
        for status, count in status_counts.items():
            status_name = {2: '待接单', 5: '已完成', 6: '已取消'}[status]
            print(f"   {status_name}({status}): {count} 个")
        
        print(f"\n💰 总金额: ¥{df['金额'].sum():.2f}")
        print("\n✅ 测试完成，数据读取正常!")
        
    except Exception as e:
        print(f"❌ 读取失败: {e}")

if __name__ == '__main__':
    quick_test() 