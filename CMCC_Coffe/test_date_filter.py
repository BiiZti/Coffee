#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
测试单日期筛选功能
"""

import requests
import json
from datetime import datetime, date

def test_date_filter():
    """测试单日期筛选功能"""
    base_url = "http://localhost:5000"
    
    print("=" * 60)
    print("🧪 测试单日期筛选功能")
    print("=" * 60)
    
    try:
        # 1. 获取所有订单
        print("\n📋 1. 获取所有订单...")
        response = requests.get(f"{base_url}/api/orders/all")
        if response.status_code == 200:
            data = response.json()
            if data['code'] == 1:
                orders = data['data']
                print(f"✅ 成功获取 {len(orders)} 个订单")
                
                # 2. 显示所有订单的日期分布
                print("\n📅 2. 订单日期分布:")
                date_counts = {}
                for order in orders:
                    try:
                        order_date = datetime.fromisoformat(order['orderTime'].replace('Z', '+00:00')).date()
                        date_str = order_date.isoformat()
                        date_counts[date_str] = date_counts.get(date_str, 0) + 1
                    except Exception as e:
                        print(f"   解析订单{order['id']}时间出错: {e}")
                
                for date_str, count in sorted(date_counts.items()):
                    print(f"   {date_str}: {count} 个订单")
                
                # 3. 测试日期筛选
                if date_counts:
                    # 选择第一个有订单的日期进行测试
                    test_date = list(date_counts.keys())[0]
                    print(f"\n🎯 3. 测试筛选日期: {test_date}")
                    
                    # 模拟前端筛选逻辑
                    filtered_orders = []
                    for order in orders:
                        try:
                            order_date = datetime.fromisoformat(order['orderTime'].replace('Z', '+00:00')).date()
                            if order_date.isoformat() == test_date:
                                filtered_orders.append(order)
                        except Exception as e:
                            continue
                    
                    print(f"✅ 筛选结果: {len(filtered_orders)} 个订单")
                    
                    # 显示筛选结果
                    print("\n📋 筛选结果详情:")
                    for i, order in enumerate(filtered_orders, 1):
                        status_map = {2: "待接单", 3: "准备中", 5: "已完成", 6: "已取消"}
                        status_name = status_map.get(order['status'], f"状态{order['status']}")
                        order_time = datetime.fromisoformat(order['orderTime'].replace('Z', '+00:00')).strftime('%H:%M:%S')
                        print(f"  {i}. {order['number']} - {status_name} - {order['userName']} - {order_time}")
                    
                    # 4. 验证筛选逻辑
                    print(f"\n✅ 4. 筛选验证:")
                    print(f"   预期订单数: {date_counts[test_date]}")
                    print(f"   实际筛选数: {len(filtered_orders)}")
                    
                    if len(filtered_orders) == date_counts[test_date]:
                        print("   ✅ 筛选结果正确")
                    else:
                        print("   ❌ 筛选结果不正确")
                    
                    # 5. 测试无结果的情况
                    print(f"\n🎯 5. 测试无结果筛选...")
                    future_date = "2099-12-31"  # 一个未来的日期
                    future_filtered = []
                    for order in orders:
                        try:
                            order_date = datetime.fromisoformat(order['orderTime'].replace('Z', '+00:00')).date()
                            if order_date.isoformat() == future_date:
                                future_filtered.append(order)
                        except Exception as e:
                            continue
                    
                    print(f"   筛选未来日期 {future_date}: {len(future_filtered)} 个订单")
                    if len(future_filtered) == 0:
                        print("   ✅ 无结果筛选正确")
                    else:
                        print("   ❌ 无结果筛选有问题")
                
                else:
                    print("❌ 没有找到有效的订单日期")
                
            else:
                print(f"❌ 获取订单失败: {data['msg']}")
        else:
            print(f"❌ 请求失败: {response.status_code}")
            
    except Exception as e:
        print(f"❌ 测试过程中出错: {e}")
    
    print("=" * 60)
    print("💡 使用说明:")
    print("1. 在界面中选择一个日期")
    print("2. 点击'查询'按钮")
    print("3. 系统会显示该日期的所有订单")
    print("4. 点击'清除'按钮可以重置筛选条件")
    print("=" * 60)

if __name__ == "__main__":
    test_date_filter() 