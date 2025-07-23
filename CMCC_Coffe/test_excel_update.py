#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试Excel更新功能
"""

import sys
import os

# 添加当前目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# 导入app.py中的函数
from app import update_excel_order_status, read_excel_orders, orders_db

def test_excel_update():
    """测试Excel更新功能"""
    print("=" * 50)
    print("🧪 测试Excel更新功能")
    print("=" * 50)
    
    # 先读取Excel数据
    read_excel_orders()
    
    # 重新导入orders_db获取最新值
    from app import orders_db
    print(f"📊 当前订单数量: {len(orders_db)}")
    
    if orders_db:
        print("\n📋 更新前的订单状态:")
        for order in orders_db:
            print(f"  订单{order['id']}: {order['number']} - 状态{order['status']}")
        
        # 测试更新第一个订单的状态
        test_order_id = 1
        new_status = 3  # 准备中
        
        print(f"\n🔄 测试更新订单{test_order_id}状态为{new_status}...")
        
        # 更新Excel文件
        success = update_excel_order_status(test_order_id, new_status)
        
        if success:
            print("✅ Excel文件更新成功！")
            
            # 重新读取数据验证
            read_excel_orders()
            from app import orders_db
            print("\n📋 更新后的订单状态:")
            for order in orders_db:
                print(f"  订单{order['id']}: {order['number']} - 状态{order['status']}")
        else:
            print("❌ Excel文件更新失败！")
    else:
        print("❌ 没有订单数据可测试")
    
    print("=" * 50)

if __name__ == '__main__':
    test_excel_update() 