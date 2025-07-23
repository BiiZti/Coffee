#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
测试前端操作保护机制
"""

import requests
import json
import time
from datetime import datetime

def test_frontend_protection():
    """测试前端操作保护机制"""
    base_url = "http://localhost:5000"
    
    print("=" * 60)
    print("🧪 测试前端操作保护机制")
    print("=" * 60)
    
    try:
        # 1. 获取当前订单状态
        print("\n📋 1. 获取当前订单状态...")
        response = requests.get(f"{base_url}/api/orders/all")
        if response.status_code == 200:
            data = response.json()
            if data['code'] == 1:
                orders = data['data']
                print(f"✅ 成功获取 {len(orders)} 个订单")
                
                # 找到待接单的订单
                pending_orders = [order for order in orders if order['status'] == 2]
                if pending_orders:
                    test_order = pending_orders[0]
                    print(f"\n🎯 选择测试订单: {test_order['number']} (ID: {test_order['id']})")
                    print(f"   当前状态: {test_order['status']} (待接单)")
                    
                    # 2. 执行前端操作（接单）
                    print(f"\n🔄 2. 执行前端操作 - 接单...")
                    response = requests.post(f"{base_url}/api/order/{test_order['id']}/confirm")
                    if response.status_code == 200:
                        data = response.json()
                        if data['code'] == 1:
                            print("✅ 接单成功！")
                            
                            # 3. 验证状态是否改变
                            time.sleep(1)
                            response = requests.get(f"{base_url}/api/orders/all")
                            if response.status_code == 200:
                                data = response.json()
                                if data['code'] == 1:
                                    updated_orders = data['data']
                                    updated_order = next((o for o in updated_orders if o['id'] == test_order['id']), None)
                                    if updated_order and updated_order['status'] == 3:
                                        print("✅ 确认订单状态已更新为准备中")
                                        
                                        # 4. 查看前端操作记录
                                        print(f"\n📊 3. 查看前端操作记录...")
                                        response = requests.get(f"{base_url}/api/frontend-operations")
                                        if response.status_code == 200:
                                            data = response.json()
                                            if data['code'] == 1:
                                                operations = data['data']
                                                print(f"   前端操作记录数量: {operations['operations_count']}")
                                                if operations['operations_count'] > 0:
                                                    print("   操作详情:")
                                                    for order_id, info in operations['operations'].items():
                                                        print(f"     订单{order_id}: {info['time_ago']}前")
                                                    print("✅ 前端操作记录已创建")
                                                else:
                                                    print("❌ 没有找到前端操作记录")
                                            else:
                                                print(f"❌ 获取前端操作记录失败: {data['msg']}")
                                        else:
                                            print(f"❌ 获取前端操作记录请求失败: {response.status_code}")
                                        
                                        # 5. 模拟Excel数据更新（这里我们手动修改Excel文件来测试）
                                        print(f"\n🔄 4. 模拟Excel数据更新...")
                                        print("   注意：这里需要手动修改Excel文件中的订单状态来测试保护机制")
                                        print("   当前订单状态应该保持为'准备中'，即使Excel中改回'待接单'")
                                        
                                        # 6. 等待下一次Excel读取（1分钟后）
                                        print(f"\n⏰ 5. 等待Excel数据刷新...")
                                        print("   系统每分钟会自动读取Excel文件")
                                        print("   如果Excel中的状态与前端状态冲突，系统会保持前端状态")
                                        
                                    else:
                                        print(f"❌ 接单后状态验证失败，当前状态: {updated_order['status'] if updated_order else 'None'}")
                                else:
                                    print(f"❌ 获取更新后订单数据失败: {data['msg']}")
                            else:
                                print(f"❌ 获取更新后订单数据请求失败: {response.status_code}")
                        else:
                            print(f"❌ 接单失败: {data['msg']}")
                    else:
                        print(f"❌ 接单请求失败: {response.status_code}")
                else:
                    print("❌ 没有找到待接单的订单")
            else:
                print(f"❌ 获取订单失败: {data['msg']}")
        else:
            print(f"❌ 获取订单请求失败: {response.status_code}")
            
    except Exception as e:
        print(f"❌ 测试过程中出错: {e}")
    
    print("=" * 60)
    print("💡 测试说明:")
    print("1. 前端操作会记录时间戳")
    print("2. Excel数据更新时会检查冲突")
    print("3. 如果Excel状态与前端状态不同，保持前端状态")
    print("4. 状态同步后，清除前端操作记录")
    print("=" * 60)

if __name__ == "__main__":
    test_frontend_protection() 