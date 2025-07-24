#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
测试冲突检测机制
模拟用户操作与咖啡订单程序更新的冲突场景
"""

import requests
import time
import json
from test_new_order import simulate_new_coffee_order

def test_conflict_detection():
    """测试冲突检测机制"""
    
    base_url = "http://localhost:5000"
    
    print("🧪 开始测试冲突检测机制...")
    print("=" * 60)
    
    # 1. 获取初始订单列表
    print("📋 步骤1: 获取初始订单列表")
    try:
        response = requests.get(f"{base_url}/api/orders/all")
        if response.status_code == 200:
            data = response.json()
            initial_orders = data.get('data', [])
            print(f"✅ 初始订单数量: {len(initial_orders)}")
        else:
            print(f"❌ 获取订单列表失败: {response.status_code}")
            return
    except Exception as e:
        print(f"❌ 连接服务器失败: {e}")
        return
    
    # 2. 模拟用户操作 - 完成第一个订单
    if initial_orders:
        first_order = initial_orders[0]
        order_id = first_order['id']
        print(f"\n👤 步骤2: 模拟用户操作 - 完成订单 {order_id}")
        
        try:
            response = requests.post(f"{base_url}/api/order/{order_id}/complete")
            if response.status_code == 200:
                result = response.json()
                print(f"✅ 用户操作结果: {result['msg']}")
            else:
                print(f"❌ 用户操作失败: {response.status_code}")
        except Exception as e:
            print(f"❌ 用户操作异常: {e}")
    
    # 3. 模拟咖啡订单程序添加新订单
    print(f"\n☕ 步骤3: 模拟咖啡订单程序添加新订单")
    print("⏳ 等待2秒后开始添加...")
    time.sleep(2)
    
    new_order_number = simulate_new_coffee_order()
    if new_order_number:
        print(f"✅ 咖啡订单程序添加成功: {new_order_number}")
    else:
        print("❌ 咖啡订单程序添加失败")
    
    # 4. 立即尝试用户操作 - 测试冲突检测
    print(f"\n⚡ 步骤4: 立即尝试用户操作 - 测试冲突检测")
    print("⏳ 等待1秒后尝试用户操作...")
    time.sleep(1)
    
    if initial_orders:
        second_order = initial_orders[1] if len(initial_orders) > 1 else initial_orders[0]
        order_id = second_order['id']
        
        try:
            response = requests.post(f"{base_url}/api/order/{order_id}/complete")
            if response.status_code == 200:
                result = response.json()
                print(f"📊 冲突检测结果: {result['msg']}")
                
                if "系统繁忙" in result['msg']:
                    print("✅ 冲突检测机制正常工作！")
                else:
                    print("⚠️  冲突检测可能未触发")
            else:
                print(f"❌ 冲突检测测试失败: {response.status_code}")
        except Exception as e:
            print(f"❌ 冲突检测测试异常: {e}")
    
    # 5. 检查系统状态
    print(f"\n📊 步骤5: 检查系统状态")
    try:
        response = requests.get(f"{base_url}/api/system-status")
        if response.status_code == 200:
            data = response.json()
            status = data.get('data', {})
            print(f"📈 系统状态:")
            print(f"   Excel更新状态: {status.get('is_excel_updating', 'N/A')}")
            print(f"   前端操作数量: {status.get('frontend_operations_count', 'N/A')}")
            print(f"   当前订单数量: {status.get('orders_count', 'N/A')}")
        else:
            print(f"❌ 获取系统状态失败: {response.status_code}")
    except Exception as e:
        print(f"❌ 获取系统状态异常: {e}")
    
    # 6. 等待一段时间后再次尝试用户操作
    print(f"\n⏰ 步骤6: 等待5秒后再次尝试用户操作")
    time.sleep(5)
    
    if initial_orders:
        third_order = initial_orders[2] if len(initial_orders) > 2 else initial_orders[0]
        order_id = third_order['id']
        
        try:
            response = requests.post(f"{base_url}/api/order/{order_id}/complete")
            if response.status_code == 200:
                result = response.json()
                print(f"📊 延迟操作结果: {result['msg']}")
                
                if "成功" in result['msg']:
                    print("✅ 系统恢复正常，用户操作成功！")
                else:
                    print("⚠️  系统可能仍在繁忙状态")
            else:
                print(f"❌ 延迟操作失败: {response.status_code}")
        except Exception as e:
            print(f"❌ 延迟操作异常: {e}")
    
    print("\n" + "=" * 60)
    print("🎉 冲突检测测试完成！")

def test_multiple_conflicts():
    """测试多次冲突场景"""
    print("🔄 开始测试多次冲突场景...")
    print("=" * 60)
    
    for i in range(3):
        print(f"\n🔄 第 {i+1} 轮冲突测试:")
        
        # 模拟咖啡订单程序添加新订单
        print("☕ 咖啡订单程序添加新订单...")
        new_order_number = simulate_new_coffee_order()
        
        if new_order_number:
            print(f"✅ 添加成功: {new_order_number}")
            
            # 立即尝试用户操作
            print("👤 立即尝试用户操作...")
            time.sleep(1)
            
            # 这里可以添加实际的用户操作测试
            print("⏳ 等待3秒...")
            time.sleep(3)
        else:
            print("❌ 添加失败")
        
        print(f"✅ 第 {i+1} 轮测试完成")
    
    print("\n" + "=" * 60)
    print("🎉 多次冲突测试完成！")

if __name__ == "__main__":
    # 运行冲突检测测试
    test_conflict_detection()
    
    print("\n" + "=" * 60)
    
    # 运行多次冲突测试
    test_multiple_conflicts() 