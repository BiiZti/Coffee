#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试Excel文件读取功能
"""

import pandas as pd
import os
import glob

def test_excel_reading():
    """测试Excel文件读取"""
    
    # 查找所有Excel文件
    excel_files = glob.glob(os.path.join('orders', '*.xlsx'))
    
    print("=" * 60)
    print("🔍 Excel文件读取测试")
    print("=" * 60)
    
    for file_path in excel_files:
        print(f"\n📁 测试文件: {file_path}")
        print("-" * 40)
        
        try:
            # 尝试读取Excel文件
            df = pd.read_excel(file_path, engine='openpyxl')
            
            print(f"✅ 读取成功!")
            print(f"📊 数据行数: {len(df)}")
            print(f"📋 列名: {list(df.columns)}")
            
            # 显示前几行数据
            print("\n📋 前3行数据:")
            print(df.head(3).to_string())
            
            # 检查是否有中文字符
            print(f"\n🔤 字符编码检查:")
            for col in df.columns:
                sample_value = str(df[col].iloc[0]) if len(df) > 0 else ""
                print(f"   {col}: {sample_value}")
            
        except Exception as e:
            print(f"❌ 读取失败: {e}")
            import traceback
            traceback.print_exc()
    
    print("\n" + "=" * 60)
    print("🎯 测试完成")
    print("=" * 60)

if __name__ == '__main__':
    test_excel_reading() 