#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成简单的测试订单数据
"""

import pandas as pd
import os
from datetime import datetime, timedelta
import random

def generate_simple_test_data():
    """生成简单的测试数据，所有订单都是待接单状态"""
    
    # 确保orders文件夹存在
    orders_folder = "orders"
    if not os.path.exists(orders_folder):
        os.makedirs(orders_folder)
        print(f"创建文件夹: {orders_folder}")
    
    # 生成测试数据
    test_data = []
    
    # 菜品列表
    dishes_list = [
        "美式咖啡", "拿铁咖啡", "卡布奇诺", "摩卡咖啡", "焦糖玛奇朵",
        "红茶", "绿茶", "奶茶", "柠檬水", "橙汁",
        "三明治", "蛋糕", "面包", "饼干", "水果沙拉"
    ]
    
    # 生成5个待接单订单
    for i in range(1, 6):
        # 随机生成下单时间（最近1小时内）
        order_time = datetime.now() - timedelta(minutes=random.randint(0, 60))
        
        # 随机选择1-3个菜品
        num_dishes = random.randint(1, 3)
        selected_dishes = random.sample(dishes_list, num_dishes)
        dishes_str = ",".join(selected_dishes)
        
        # 计算总金额（每个菜品10-30元）
        total_amount = sum(random.randint(10, 30) for _ in range(num_dishes))
        
        order = {
            '订单号': f'ORDER{str(i).zfill(3)}',
            '状态': 2,  # 所有订单都是待接单状态
            '用户名': f'用户{i}',
            '手机号': f'138{str(random.randint(10000000, 99999999))}',
            '地址': f'北京市朝阳区第{i}街道{i}号',
            '金额': total_amount,
            '备注': random.choice(['', '少糖', '多冰', '不要奶泡', '快点送', '热饮', '冷饮', '加奶', '不加糖', '少冰', '常温']),
            '下单时间': order_time.strftime('%Y-%m-%d %H:%M:%S'),
            '菜品': dishes_str
        }
        test_data.append(order)
    
    # 创建DataFrame
    df = pd.DataFrame(test_data)
    
    # 保存到Excel文件
    output_file = os.path.join(orders_folder, "simple_test_orders.xlsx")
    df.to_excel(output_file, index=False, engine='openpyxl')
    
    print(f"✅ 成功生成测试数据文件: {output_file}")
    print(f"📊 生成了 {len(test_data)} 个待接单订单")
    print("\n📋 订单详情:")
    for i, order in enumerate(test_data, 1):
        print(f"  订单{i}: {order['订单号']} - {order['用户名']} - ¥{order['金额']} - {order['菜品']}")
    
    return output_file

if __name__ == "__main__":
    generate_simple_test_data() 