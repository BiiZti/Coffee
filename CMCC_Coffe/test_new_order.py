#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
模拟新增咖啡订单测试
模拟咖啡订单程序向Excel文件添加新订单
"""

import pandas as pd
import glob
import os
import time
from datetime import datetime
from openpyxl import load_workbook
import random

def simulate_new_coffee_order():
    """模拟新增咖啡订单"""
    
    # 查找最新的Excel文件
    EXCEL_FOLDER = 'orders'
    EXCEL_PATTERN = '*.xlsx'
    
    excel_files = glob.glob(os.path.join(EXCEL_FOLDER, EXCEL_PATTERN))
    if not excel_files:
        print("❌ 未找到Excel文件")
        return
    
    latest_file = max(excel_files, key=os.path.getctime)
    print(f"📁 操作文件: {latest_file}")
    
    try:
        # 读取现有数据
        df = pd.read_excel(latest_file, engine='openpyxl')
        print(f"📊 当前数据行数: {len(df)}")
        
        # 生成新订单数据
        new_order = generate_new_order_data()
        
        # 添加新订单到DataFrame
        new_row = pd.DataFrame([new_order])
        df = pd.concat([df, new_row], ignore_index=True)
        
        print(f"➕ 添加新订单: {new_order['订单编号']}")
        print(f"📋 订单详情:")
        print(f"   姓名: {new_order['姓名']}")
        print(f"   手机号码: {new_order['手机号码']}")
        print(f"   公司: {new_order['公司']}")
        print(f"   部门: {new_order['部门']}")
        print(f"   订单金额: ¥{new_order['订单金额']}")
        print(f"   物流方式: {new_order['物流方式']}")
        print(f"   取货时间: {new_order['取货时间']}")
        print(f"   取餐码: {new_order['取餐码']}")
        print(f"   订单状态: {new_order['订单状态']}")
        
        # 保存到Excel文件
        df.to_excel(latest_file, index=False, engine='openpyxl')
        print(f"✅ 新订单已保存到Excel文件")
        print(f"📊 更新后数据行数: {len(df)}")
        
        return new_order['订单编号']
        
    except Exception as e:
        print(f"❌ 添加新订单失败: {e}")
        return None

def generate_new_order_data():
    """生成新订单数据"""
    
    # 生成订单编号 (格式: W1 + 年月日 + 时分秒 + 4位随机数)
    now = datetime.now()
    order_number = f"W1{now.strftime('%Y%m%d%H%M%S')}{random.randint(1000, 9999)}"
    
    # 随机选择客户信息
    customers = [
        {'name': '张三', 'phone': '13800138001', 'company': '技术部', 'department': '开发组'},
        {'name': '李四', 'phone': '13800138002', 'company': '市场部', 'department': '销售组'},
        {'name': '王五', 'phone': '13800138003', 'company': '人事部', 'department': '招聘组'},
        {'name': '赵六', 'phone': '13800138004', 'company': '财务部', 'department': '会计组'},
        {'name': '钱七', 'phone': '13800138005', 'company': '运营部', 'department': '客服组'}
    ]
    
    customer = random.choice(customers)
    
    # 随机选择咖啡
    coffees = [
        '美式咖啡',
        '拿铁咖啡', 
        '卡布奇诺',
        '摩卡咖啡',
        '焦糖玛奇朵',
        '香草拿铁',
        '榛果拿铁',
        '白咖啡'
    ]
    
    coffee = random.choice(coffees)
    
    # 生成订单数据
    order_data = {
        '订单编号': order_number,
        '姓名': customer['name'],
        '手机号码': customer['phone'],
        '公司': customer['company'],
        '部门': customer['department'],
        '订单金额': round(random.uniform(15, 35), 2),
        '物流方式': random.choice(['自提', '配送']),
        '取货时间': f"{now.strftime('%Y-%m-%d')} {now.hour}:{now.minute}",
        '预定时间': f"{now.strftime('%Y-%m-%d')} {now.hour}:{now.minute}",
        '取餐码': f"{random.randint(10000, 99999)}",
        '包装费': 0,
        '配送费': 0,
        '订单次数': 0,
        '实际支付次数': 0,
        '实际支付金额': 0,
        '订单状态': '备货中',
        '菜品': coffee,
        '订单时间': now.strftime('%Y-%m-%d %H:%M:%S')
    }
    
    return order_data

def test_multiple_orders(count=3):
    """测试添加多个订单"""
    print(f"🚀 开始模拟添加 {count} 个新咖啡订单...")
    print("=" * 50)
    
    for i in range(count):
        print(f"\n📦 添加第 {i+1} 个订单:")
        order_number = simulate_new_coffee_order()
        
        if order_number:
            print(f"✅ 第 {i+1} 个订单添加成功: {order_number}")
        else:
            print(f"❌ 第 {i+1} 个订单添加失败")
        
        # 等待一段时间再添加下一个
        if i < count - 1:
            print("⏳ 等待3秒后添加下一个订单...")
            time.sleep(3)
    
    print("\n" + "=" * 50)
    print("🎉 所有测试订单添加完成！")

if __name__ == "__main__":
    # 测试添加3个新订单
    test_multiple_orders(3) 