#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
测试完整的运营流程
待接单 → 准备中 → 已完成
"""

import requests
import time
import json

def test_workflow():
    """测试完整的运营流程"""
    base_url = "http://localhost:5000"
    
    print("=" * 60)
    print("🧪 测试完整运营流程")
    print("=" * 60)
    
    # 1. 获取所有订单
    print("\n📋 1. 获取所有订单...")
    try:
        response = requests.get(f"{base_url}/api/orders/all")
        if response.status_code == 200:
            data = response.json()
            if data['code'] == 1:
                orders = data['data']
                print(f"✅ 成功获取 {len(orders)} 个订单")
                
                # 显示所有订单状态
                print("\n📊 当前订单状态:")
                for order in orders:
                    status_map = {2: "待接单", 3: "准备中", 5: "已完成", 6: "已取消"}
                    status_name = status_map.get(order['status'], f"状态{order['status']}")
                    print(f"  订单{order['id']}: {order['number']} - {status_name}")
                
                # 2. 找到待接单的订单
                pending_orders = [order for order in orders if order['status'] == 2]
                if pending_orders:
                    test_order = pending_orders[0]
                    print(f"\n🎯 选择测试订单: {test_order['number']} (ID: {test_order['id']})")
                    
                    # 3. 接单操作（待接单 → 准备中）
                    print(f"\n🔄 2. 执行接单操作 (订单{test_order['id']})...")
                    response = requests.post(f"{base_url}/api/order/{test_order['id']}/confirm")
                    if response.status_code == 200:
                        data = response.json()
                        if data['code'] == 1:
                            print("✅ 接单成功！订单状态已更新为：准备中")
                            
                            # 4. 等待一秒，然后获取更新后的订单
                            time.sleep(1)
                            response = requests.get(f"{base_url}/api/orders/all")
                            if response.status_code == 200:
                                data = response.json()
                                if data['code'] == 1:
                                    updated_orders = data['data']
                                    updated_order = next((o for o in updated_orders if o['id'] == test_order['id']), None)
                                    if updated_order and updated_order['status'] == 3:
                                        print("✅ 确认订单状态已更新为准备中")
                                        
                                        # 5. 完成订单操作（准备中 → 已完成）
                                        print(f"\n🔄 3. 执行完成订单操作 (订单{test_order['id']})...")
                                        response = requests.post(f"{base_url}/api/order/{test_order['id']}/complete")
                                        if response.status_code == 200:
                                            data = response.json()
                                            if data['code'] == 1:
                                                print("✅ 完成订单成功！订单状态已更新为：已完成")
                                                
                                                # 6. 最终验证
                                                time.sleep(1)
                                                response = requests.get(f"{base_url}/api/orders/all")
                                                if response.status_code == 200:
                                                    data = response.json()
                                                    if data['code'] == 1:
                                                        final_orders = data['data']
                                                        final_order = next((o for o in final_orders if o['id'] == test_order['id']), None)
                                                        if final_order and final_order['status'] == 5:
                                                            print("✅ 确认订单状态已更新为已完成")
                                                            print("\n🎉 完整运营流程测试成功！")
                                                            print("   待接单 → 准备中 → 已完成")
                                                        else:
                                                            print(f"❌ 最终状态验证失败，当前状态: {final_order['status'] if final_order else 'None'}")
                                                    else:
                                                        print(f"❌ 获取最终订单数据失败: {data['msg']}")
                                                else:
                                                    print(f"❌ 获取最终订单数据请求失败: {response.status_code}")
                                            else:
                                                print(f"❌ 完成订单失败: {data['msg']}")
                                        else:
                                            print(f"❌ 完成订单请求失败: {response.status_code}")
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

if __name__ == "__main__":
    test_workflow() 