#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CMCC Coffee 订单管理系统启动脚本
"""

import subprocess
import sys
import os

def main():
    """启动主程序"""
    print("=" * 50)
    print("🚀 CMCC Coffee 订单管理系统")
    print("=" * 50)
    
    # 检查Python版本
    if sys.version_info < (3, 7):
        print("❌ 错误: 需要Python 3.7或更高版本")
        sys.exit(1)
    
    # 检查依赖
    try:
        import flask
        import pandas
        import openpyxl
        print("✅ 依赖检查通过")
    except ImportError as e:
        print(f"❌ 缺少依赖: {e}")
        print("请运行: pip install -r requirements.txt")
        sys.exit(1)
    
    # 检查Excel文件
    if not os.path.exists('orders'):
        os.makedirs('orders')
        print("📁 创建orders文件夹")
    
    excel_files = [f for f in os.listdir('orders') if f.endswith('.xlsx')]
    if not excel_files:
        print("⚠️  警告: orders文件夹中没有Excel文件")
        print("请运行: python generate_simple_test_data.py 生成测试数据")
    else:
        print(f"📊 找到 {len(excel_files)} 个Excel文件")
    
    print("\n🎯 启动系统...")
    print("=" * 50)
    
    # 启动Flask应用
    try:
        # 获取当前脚本所在目录
        script_dir = os.path.dirname(os.path.abspath(__file__))
        main_path = os.path.join(script_dir, 'main.py')
        subprocess.run([sys.executable, main_path], check=True)
    except KeyboardInterrupt:
        print("\n👋 系统已停止")
    except Exception as e:
        print(f"❌ 启动失败: {e}")

if __name__ == '__main__':
    main() 