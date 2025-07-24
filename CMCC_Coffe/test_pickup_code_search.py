#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
取餐码查询功能测试
"""

import requests
import time

def test_pickup_code_search():
    """测试取餐码查询功能"""
    
    base_url = "http://localhost:5000"
    
    print("🔍 取餐码查询功能测试...")
    print("=" * 50)
    
    # 等待应用启动
    print("⏳ 等待应用启动...")
    time.sleep(3)
    
    try:
        # 1. 先获取所有订单，查看有哪些取餐码
        print("\n📋 获取所有订单...")
        response = requests.get(f"{base_url}/api/orders/all")
        if response.status_code == 200:
            data = response.json()
            orders = data.get('data', [])
            print(f"✅ 当前共有 {len(orders)} 个订单")
            
            # 提取所有取餐码
            pickup_codes = []
            for order in orders:
                remark = order.get('remark', '')
                if '取餐码:' in remark:
                    pickup_code = remark.split('取餐码:')[1].strip()
                    pickup_codes.append(pickup_code)
                    print(f"   订单{order['id']}: {order['number']} - 取餐码: {pickup_code}")
            
            if not pickup_codes:
                print("❌ 没有找到取餐码")
                return False
            
            # 2. 测试取餐码查询
            test_pickup_code = pickup_codes[0]  # 使用第一个取餐码进行测试
            print(f"\n🔍 测试查询取餐码: {test_pickup_code}")
            
            response = requests.get(f"{base_url}/api/search/pickup-code/{test_pickup_code}")
            if response.status_code == 200:
                data = response.json()
                if data['code'] == 1:
                    orders = data.get('data', [])
                    print(f"✅ 查询成功！找到 {len(orders)} 个匹配的订单")
                    
                    for order in orders:
                        print(f"   - 订单{order['id']}: {order['number']} ({order['status']})")
                        print(f"     姓名: {order['userName']}, 手机: {order['phone']}")
                        print(f"     备注: {order['remark']}")
                    
                    return True
                else:
                    print(f"❌ 查询失败: {data['msg']}")
                    return False
            else:
                print(f"❌ 查询请求失败: {response.status_code}")
                return False
                
        else:
            print(f"❌ 获取订单列表失败: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ 测试过程中出错: {e}")
        return False

def test_phone_search():
    """测试手机号查询功能"""
    
    base_url = "http://localhost:5000"
    
    print("\n" + "=" * 50)
    print("📱 手机号查询功能测试...")
    print("=" * 50)
    
    try:
        # 1. 先获取所有订单，查看有哪些手机号
        print("\n📋 获取所有订单...")
        response = requests.get(f"{base_url}/api/orders/all")
        if response.status_code == 200:
            data = response.json()
            orders = data.get('data', [])
            
            # 提取所有手机号
            phone_numbers = []
            for order in orders:
                phone = order.get('phone', '')
                if phone and phone != '未知':
                    phone_numbers.append(phone)
                    print(f"   订单{order['id']}: {order['number']} - 手机: {phone}")
            
            if not phone_numbers:
                print("❌ 没有找到有效的手机号")
                return False
            
            # 2. 测试手机号查询
            test_phone = phone_numbers[0]  # 使用第一个手机号进行测试
            print(f"\n📱 测试查询手机号: {test_phone}")
            
            response = requests.get(f"{base_url}/api/search/phone/{test_phone}")
            if response.status_code == 200:
                data = response.json()
                if data['code'] == 1:
                    orders = data.get('data', [])
                    print(f"✅ 查询成功！找到 {len(orders)} 个匹配的订单")
                    
                    for order in orders:
                        print(f"   - 订单{order['id']}: {order['number']} ({order['status']})")
                        print(f"     姓名: {order['userName']}, 手机: {order['phone']}")
                    
                    return True
                else:
                    print(f"❌ 查询失败: {data['msg']}")
                    return False
            else:
                print(f"❌ 查询请求失败: {response.status_code}")
                return False
                
        else:
            print(f"❌ 获取订单列表失败: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ 测试过程中出错: {e}")
        return False

def test_invalid_search():
    """测试无效查询"""
    
    base_url = "http://localhost:5000"
    
    print("\n" + "=" * 50)
    print("❌ 无效查询测试...")
    print("=" * 50)
    
    try:
        # 测试不存在的取餐码
        print("\n🔍 测试不存在的取餐码: 99999")
        response = requests.get(f"{base_url}/api/search/pickup-code/99999")
        if response.status_code == 200:
            data = response.json()
            if data['code'] == 0:
                print(f"✅ 正确处理无效查询: {data['msg']}")
            else:
                print(f"❌ 无效查询处理异常: {data}")
                return False
        else:
            print(f"❌ 无效查询请求失败: {response.status_code}")
            return False
        
        # 测试不存在的手机号
        print("\n📱 测试不存在的手机号: 99999999999")
        response = requests.get(f"{base_url}/api/search/phone/99999999999")
        if response.status_code == 200:
            data = response.json()
            if data['code'] == 0:
                print(f"✅ 正确处理无效查询: {data['msg']}")
            else:
                print(f"❌ 无效查询处理异常: {data}")
                return False
        else:
            print(f"❌ 无效查询请求失败: {response.status_code}")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ 测试过程中出错: {e}")
        return False

def main():
    """主测试函数"""
    
    print("🎯 取餐码查询功能测试开始...")
    print("=" * 50)
    
    # 测试取餐码查询
    pickup_success = test_pickup_code_search()
    
    # 测试手机号查询
    phone_success = test_phone_search()
    
    # 测试无效查询
    invalid_success = test_invalid_search()
    
    # 总结测试结果
    print("\n" + "=" * 50)
    print("📊 测试结果总结:")
    print("=" * 50)
    print(f"   取餐码查询测试: {'✅ 通过' if pickup_success else '❌ 失败'}")
    print(f"   手机号查询测试: {'✅ 通过' if phone_success else '❌ 失败'}")
    print(f"   无效查询测试: {'✅ 通过' if invalid_success else '❌ 失败'}")
    
    passed_tests = sum([pickup_success, phone_success, invalid_success])
    total_tests = 3
    
    if passed_tests == total_tests:
        print(f"\n🎉 所有测试通过！({passed_tests}/{total_tests})")
        print("✅ 取餐码查询功能完全正常！")
    else:
        print(f"\n⚠️  部分测试失败！({passed_tests}/{total_tests})")
        print("❌ 取餐码查询功能存在问题，需要检查")

if __name__ == "__main__":
    main() 