#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CMCC Coffee 订单管理系统 - 根目录启动脚本
"""

import subprocess
import sys
import os

def main():
    """启动主程序"""
    print("=" * 60)
    print("🚀 CMCC Coffee 订单管理系统")
    print("=" * 60)
    
    # 获取项目目录
    project_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'CMCC_Coffe')
    
    if not os.path.exists(project_dir):
        print(f"❌ 错误: 找不到项目目录 {project_dir}")
        sys.exit(1)
    
    print(f"📁 项目目录: {project_dir}")
    print("🎯 启动系统...")
    print("=" * 60)
    
    # 切换到项目目录并启动
    try:
        # 使用subprocess在项目目录中运行start.py
        start_script = os.path.join(project_dir, 'start.py')
        subprocess.run([sys.executable, start_script], check=True)
    except KeyboardInterrupt:
        print("\n👋 系统已停止")
    except Exception as e:
        print(f"❌ 启动失败: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main() 