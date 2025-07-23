#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
测试订单排序功能
"""

import requests
import json
from datetime import datetime

def test_order_sorting():
    """测试订单排序功能"""
    base_url = "http://localhost:5000"
    
    print("=" * 60)
    print("🧪 测试订单排序功能")
    print("=" * 60)
    
    try:
        # 获取所有订单
        response = requests.get(f"{base_url}/api/orders/all")
        if response.status_code == 200:
            data = response.json()
            if data['code'] == 1:
                orders = data['data']
                print(f"✅ 成功获取 {len(orders)} 个订单")
                
                # 显示排序前的订单
                print("\n📋 排序前的订单状态:")
                for i, order in enumerate(orders, 1):
                    status_map = {2: "待接单", 3: "准备中", 5: "已完成", 6: "已取消"}
                    status_name = status_map.get(order['status'], f"状态{order['status']}")
                    order_time = datetime.fromisoformat(order['orderTime'].replace('Z', '+00:00')).strftime('%H:%M:%S')
                    print(f"  {i}. {order['number']} - {status_name} - {order_time}")
                
                # 模拟前端排序逻辑
                print("\n🔄 应用智能排序...")
                
                # 定义状态优先级：待接单(2) > 准备中(3) > 已完成(5) > 已取消(6)
                status_priority = {2: 1, 3: 2, 5: 3, 6: 4}
                
                def sort_orders(orders):
                    return sorted(orders, key=lambda x: (
                        status_priority.get(x['status'], 5),  # 按状态优先级排序
                        -datetime.fromisoformat(x['orderTime'].replace('Z', '+00:00')).timestamp()  # 同状态下按时间倒序
                    ))
                
                sorted_orders = sort_orders(orders)
                
                # 显示排序后的订单
                print("\n📋 排序后的订单状态:")
                for i, order in enumerate(sorted_orders, 1):
                    status_map = {2: "待接单", 3: "准备中", 5: "已完成", 6: "已取消"}
                    status_name = status_map.get(order['status'], f"状态{order['status']}")
                    order_time = datetime.fromisoformat(order['orderTime'].replace('Z', '+00:00')).strftime('%H:%M:%S')
                    print(f"  {i}. {order['number']} - {status_name} - {order_time}")
                
                # 验证排序结果
                print("\n✅ 排序验证:")
                
                # 检查是否待接单和准备中在前面
                priority_orders = [o for o in sorted_orders if o['status'] in [2, 3]]
                non_priority_orders = [o for o in sorted_orders if o['status'] in [5, 6]]
                
                print(f"  优先级订单（待接单+准备中）: {len(priority_orders)} 个")
                print(f"  非优先级订单（已完成+已取消）: {len(non_priority_orders)} 个")
                
                if len(priority_orders) > 0 and len(non_priority_orders) > 0:
                    # 检查优先级订单是否都在前面
                    first_non_priority_index = next(i for i, o in enumerate(sorted_orders) if o['status'] in [5, 6])
                    priority_in_front = all(o['status'] in [2, 3] for o in sorted_orders[:first_non_priority_index])
                    
                    if priority_in_front:
                        print("  ✅ 优先级订单正确显示在前面")
                    else:
                        print("  ❌ 优先级订单排序有问题")
                
                # 检查同状态内是否按时间倒序
                status_groups = {}
                for order in sorted_orders:
                    status = order['status']
                    if status not in status_groups:
                        status_groups[status] = []
                    status_groups[status].append(order)
                
                print("\n📊 各状态内时间排序验证:")
                for status, group_orders in status_groups.items():
                    if len(group_orders) > 1:
                        status_name = {2: "待接单", 3: "准备中", 5: "已完成", 6: "已取消"}[status]
                        times = [datetime.fromisoformat(o['orderTime'].replace('Z', '+00:00')) for o in group_orders]
                        is_descending = all(times[i] >= times[i+1] for i in range(len(times)-1))
                        print(f"  {status_name}: {'✅ 时间倒序' if is_descending else '❌ 时间排序有问题'}")
                
            else:
                print(f"❌ 获取订单失败: {data['msg']}")
        else:
            print(f"❌ 请求失败: {response.status_code}")
            
    except Exception as e:
        print(f"❌ 测试过程中出错: {e}")
    
    print("=" * 60)

if __name__ == "__main__":
    test_order_sorting() 