#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
测试商品信息显示
"""

import requests
import json

def test_dishes_display():
    """测试商品信息显示"""
    base_url = "http://localhost:5000"
    
    print("=" * 60)
    print("🧪 测试商品信息显示")
    print("=" * 60)
    
    try:
        # 获取所有订单
        response = requests.get(f"{base_url}/api/orders/all")
        if response.status_code == 200:
            data = response.json()
            if data['code'] == 1:
                orders = data['data']
                print(f"✅ 成功获取 {len(orders)} 个订单")
                
                print("\n📋 订单商品信息详情:")
                for i, order in enumerate(orders, 1):
                    print(f"\n订单{i}: {order['number']}")
                    print(f"  状态: {order['status']}")
                    print(f"  用户名: {order['userName']}")
                    print(f"  金额: ¥{order['amount']}")
                    
                    # 显示商品信息
                    if order.get('dishes') and len(order['dishes']) > 0:
                        dishes_names = [dish['name'] for dish in order['dishes']]
                        print(f"  商品: {', '.join(dishes_names)}")
                    else:
                        print(f"  商品: 无商品信息")
                    
                    # 显示备注
                    if order.get('remark') and order['remark'].strip():
                        print(f"  备注: {order['remark']}")
                    else:
                        print(f"  备注: 无")
                    
                    print("-" * 40)
                
                # 统计有商品信息的订单
                orders_with_dishes = [o for o in orders if o.get('dishes') and len(o['dishes']) > 0]
                print(f"\n📊 统计信息:")
                print(f"  总订单数: {len(orders)}")
                print(f"  有商品信息的订单: {len(orders_with_dishes)}")
                print(f"  无商品信息的订单: {len(orders) - len(orders_with_dishes)}")
                
            else:
                print(f"❌ 获取订单失败: {data['msg']}")
        else:
            print(f"❌ 请求失败: {response.status_code}")
            
    except Exception as e:
        print(f"❌ 测试过程中出错: {e}")
    
    print("=" * 60)

if __name__ == "__main__":
    test_dishes_display() 