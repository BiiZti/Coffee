#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
生成混合状态的测试数据，用于测试排序功能
"""

import pandas as pd
import os
from datetime import datetime, timedelta
import random

def generate_mixed_test_data():
    """生成混合状态的测试数据"""
    
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
    
    # 备注列表
    remarks_list = [
        "", "少糖", "多冰", "不要奶泡", "快点送", "热饮", "冷饮", 
        "加奶", "不加糖", "少冰", "常温", "加冰", "去冰"
    ]
    
    # 生成10个不同状态的订单
    for i in range(1, 11):
        # 随机生成下单时间（最近2小时内）
        order_time = datetime.now() - timedelta(minutes=random.randint(0, 120))
        
        # 随机选择1-3个菜品
        num_dishes = random.randint(1, 3)
        selected_dishes = random.sample(dishes_list, num_dishes)
        dishes_str = ",".join(selected_dishes)
        
        # 计算总金额（每个菜品10-30元）
        total_amount = sum(random.randint(10, 30) for _ in range(num_dishes))
        
        # 分配不同状态：待接单(2)、准备中(3)、已完成(5)、已取消(6)
        if i <= 3:
            status = 2  # 待接单
        elif i <= 5:
            status = 3  # 准备中
        elif i <= 8:
            status = 5  # 已完成
        else:
            status = 6  # 已取消
        
        order = {
            '订单号': f'ORDER{str(i).zfill(3)}',
            '状态': status,
            '用户名': f'用户{i}',
            '手机号': f'138{str(random.randint(10000000, 99999999))}',
            '地址': f'北京市朝阳区第{i}街道{i}号',
            '金额': total_amount,
            '备注': random.choice(remarks_list),
            '下单时间': order_time.strftime('%Y-%m-%d %H:%M:%S'),
            '菜品': dishes_str
        }
        test_data.append(order)
    
    # 创建DataFrame
    df = pd.DataFrame(test_data)
    
    # 保存到Excel文件
    output_file = os.path.join(orders_folder, "mixed_test_orders.xlsx")
    df.to_excel(output_file, index=False, engine='openpyxl')
    
    print(f"✅ 成功生成混合状态测试数据文件: {output_file}")
    print(f"📊 生成了 {len(test_data)} 个订单")
    
    # 统计各状态数量
    status_counts = df['状态'].value_counts().sort_index()
    status_names = {2: '待接单', 3: '准备中', 5: '已完成', 6: '已取消'}
    
    print("\n📋 订单状态分布:")
    for status, count in status_counts.items():
        status_name = status_names.get(status, f'状态{status}')
        print(f"  {status_name}: {count} 个")
    
    print("\n📋 订单详情:")
    for i, order in enumerate(test_data, 1):
        status_name = status_names.get(order['状态'], f'状态{order["状态"]}')
        print(f"  订单{i}: {order['订单号']} - {status_name} - {order['用户名']} - ¥{order['金额']} - {order['菜品']}")
    
    return output_file

if __name__ == "__main__":
    generate_mixed_test_data() 