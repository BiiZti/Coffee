from flask import Flask, render_template, jsonify, request
import json
import time
import threading
from datetime import datetime, timedelta
import os
import random
import pandas as pd
import glob
from openpyxl import load_workbook

app = Flask(__name__)

# 订单数据存储
orders_db = []
order_counter = 1
# 记录前端操作的时间戳，防止被Excel数据覆盖
frontend_operations = {}  # {order_id: last_operation_time}

# 订单状态常量
TO_BE_CONFIRMED = 2  # 待接单
PREPARING = 3        # 准备中
COMPLETED = 5        # 已完成
CANCELLED = 6        # 已取消

# Excel文件路径配置
EXCEL_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), "orders")  # Excel文件存放文件夹
EXCEL_PATTERN = "*.xlsx"  # Excel文件匹配模式

def ensure_orders_folder():
    """确保orders文件夹存在"""
    if not os.path.exists(EXCEL_FOLDER):
        os.makedirs(EXCEL_FOLDER)
        print(f"创建文件夹: {EXCEL_FOLDER}")

def read_excel_orders():
    """从Excel文件读取订单数据"""
    global orders_db
    
    try:
        # 确保文件夹存在
        ensure_orders_folder()
        
        # 查找所有Excel文件
        excel_files = glob.glob(os.path.join(EXCEL_FOLDER, EXCEL_PATTERN))
        
        if not excel_files:
            print("未找到Excel文件，使用空订单列表")
            orders_db = []
            return
        
        # 读取最新的Excel文件
        latest_file = max(excel_files, key=os.path.getctime)
        print(f"读取Excel文件: {latest_file}")
        
        # 读取Excel数据
        df = pd.read_excel(latest_file, engine='openpyxl')
        print(f"成功读取Excel文件，数据行数: {len(df)}")
        
        # 清空现有订单数据
        orders_db = []
        
        # 处理每一行数据
        for index, row in df.iterrows():
            try:
                order_id = index + 1
                
                # 检查是否有前端操作记录
                has_frontend_operation = order_id in frontend_operations
                
                # 根据Excel列名映射数据
                order = {
                    'id': order_id,
                    'number': str(row.get('订单号', f'ORDER{order_id}')),
                    'status': int(row.get('状态', 2)),  # 默认待接单
                    'userName': str(row.get('用户名', '未知')),
                    'phone': str(row.get('手机号', '未知')),
                    'address': str(row.get('地址', '未知')),
                    'amount': float(row.get('金额', 0)),
                    'remark': str(row.get('备注', '')),
                    'orderTime': str(row.get('下单时间', datetime.now().isoformat())),
                    'dishes': []  # 可以从Excel中读取菜品信息
                }
                
                # 处理菜品信息（如果有的话）
                if '菜品' in row and pd.notna(row['菜品']):
                    dishes_str = str(row['菜品'])
                    if dishes_str and dishes_str != 'nan':
                        order['dishes'] = [{'name': dish.strip(), 'price': 0} for dish in dishes_str.split(',')]
                
                # 如果有前端操作记录，检查是否需要保护前端操作
                if has_frontend_operation:
                    # 查找现有订单的状态
                    existing_order = next((o for o in orders_db if o['id'] == order_id), None)
                    if existing_order:
                        # 如果Excel中的状态与当前状态不同，且前端操作时间较新，则保持前端状态
                        excel_status = order['status']
                        current_status = existing_order['status']
                        
                        if excel_status != current_status:
                            print(f"⚠️  订单{order_id}状态冲突: Excel={excel_status}, 前端={current_status}, 保持前端状态")
                            order['status'] = current_status
                        else:
                            # 状态一致，清除前端操作记录
                            del frontend_operations[order_id]
                            print(f"✅ 订单{order_id}状态同步，清除前端操作记录")
                    else:
                        # 新订单，清除前端操作记录
                        del frontend_operations[order_id]
                        print(f"✅ 新订单{order_id}，清除前端操作记录")
                
                orders_db.append(order)
                
            except Exception as e:
                print(f"处理第{index + 1}行数据时出错: {e}")
                continue
        
        print(f"成功读取 {len(orders_db)} 个订单")
        
    except Exception as e:
        print(f"读取Excel文件时出错: {e}")
        # 如果读取失败，保持现有数据不变

def background_excel_reader():
    """后台Excel读取线程"""
    while True:
        try:
            read_excel_orders()
            print(f"Excel数据刷新完成，当前订单数量: {len(orders_db)}")
        except Exception as e:
            print(f"后台Excel读取出错: {e}")
        
        # 等待1分钟
        time.sleep(60)

def get_orders_by_status(status=None):
    """根据状态获取订单"""
    if status is None:
        return orders_db
    return [order for order in orders_db if order['status'] == status]

def update_order_status(order_id, new_status):
    """更新订单状态"""
    global orders_db, frontend_operations
    for order in orders_db:
        if order['id'] == order_id:
            order['status'] = new_status
            # 记录前端操作时间戳
            frontend_operations[order_id] = datetime.now()
            # 同步更新Excel文件
            update_excel_order_status(order_id, new_status)
            return True
    return False

def update_excel_order_status(order_id, new_status):
    """更新Excel文件中的订单状态"""
    try:
        # 查找最新的Excel文件
        excel_files = glob.glob(os.path.join(EXCEL_FOLDER, EXCEL_PATTERN))
        if not excel_files:
            print("未找到Excel文件，无法更新状态")
            return False
        
        latest_file = max(excel_files, key=os.path.getctime)
        print(f"更新Excel文件: {latest_file}")
        
        # 使用openpyxl加载工作簿
        workbook = load_workbook(latest_file)
        worksheet = workbook.active
        
        # 找到对应的订单行（订单ID对应Excel中的行号，需要+2因为Excel从1开始且有标题行）
        row_number = order_id + 1  # 因为订单ID从1开始，Excel标题行是第1行
        
        if row_number <= worksheet.max_row:
            # 更新状态列（假设状态是第2列，B列）
            status_cell = worksheet.cell(row=row_number, column=2)
            status_cell.value = new_status
            
            # 保存文件
            workbook.save(latest_file)
            print(f"成功更新Excel文件，订单{order_id}状态改为{new_status}")
            return True
        else:
            print(f"订单ID {order_id} 超出Excel文件范围")
            return False
            
    except Exception as e:
        print(f"更新Excel文件时出错: {e}")
        return False

# Flask路由定义
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/orders')
def api_orders():
    """获取待接单订单"""
    pending_orders = get_orders_by_status(TO_BE_CONFIRMED)
    return jsonify({
        'code': 1,
        'msg': 'success',
        'data': pending_orders
    })

@app.route('/api/orders/all')
def api_all_orders():
    """获取所有订单"""
    return jsonify({
        'code': 1,
        'msg': 'success',
        'data': orders_db
    })

@app.route('/api/order/<int:order_id>/<action>', methods=['POST'])
def api_update_order(order_id, action):
    """更新订单状态"""
    try:
        if action == 'confirm':
            success = update_order_status(order_id, PREPARING)
            message = '接单成功' if success else '接单失败'
        elif action == 'reject':
            success = update_order_status(order_id, CANCELLED)
            message = '拒单成功' if success else '拒单失败'
        elif action == 'complete':
            success = update_order_status(order_id, COMPLETED)
            message = '完成订单成功' if success else '完成订单失败'
        elif action == 'cancel':
            success = update_order_status(order_id, CANCELLED)
            message = '取消订单成功' if success else '取消订单失败'
        else:
            return jsonify({'code': 0, 'msg': '无效的操作'})
        
        return jsonify({
            'code': 1 if success else 0,
            'msg': message
        })
        
    except Exception as e:
        return jsonify({'code': 0, 'msg': f'操作失败: {str(e)}'})

@app.route('/api/statistics')
def api_statistics():
    """获取统计信息"""
    total_orders = len(orders_db)
    pending_orders = len(get_orders_by_status(TO_BE_CONFIRMED))
    preparing_orders = len(get_orders_by_status(PREPARING))
    completed_orders = len(get_orders_by_status(COMPLETED))
    total_amount = sum(order['amount'] for order in orders_db)
    
    return jsonify({
        'code': 1,
        'msg': 'success',
        'data': {
            'total_orders': total_orders,
            'pending_orders': pending_orders,
            'preparing_orders': preparing_orders,
            'completed_orders': completed_orders,
            'total_amount': round(total_amount, 2)
        }
    })

@app.route('/api/orders/<status>')
def api_orders_by_status(status):
    """根据状态获取订单"""
    try:
        status_code = int(status)
        filtered_orders = get_orders_by_status(status_code)
        return jsonify({
            'code': 1,
            'msg': 'success',
            'data': filtered_orders
        })
    except ValueError:
        return jsonify({'code': 0, 'msg': '无效的状态码'})

@app.route('/api/excel-info')
def api_excel_info():
    """获取Excel文件信息"""
    try:
        ensure_orders_folder()
        excel_files = glob.glob(os.path.join(EXCEL_FOLDER, EXCEL_PATTERN))
        
        if excel_files:
            latest_file = max(excel_files, key=os.path.getctime)
            file_info = {
                'file_name': os.path.basename(latest_file),
                'file_path': latest_file,
                'last_modified': datetime.fromtimestamp(os.path.getmtime(latest_file)).isoformat(),
                'file_size': os.path.getsize(latest_file),
                'order_count': len(orders_db)
            }
        else:
            file_info = {
                'file_name': '无文件',
                'file_path': '',
                'last_modified': '',
                'file_size': 0,
                'order_count': 0
            }
        
        return jsonify({
            'code': 1,
            'msg': 'success',
            'data': file_info
        })
        
    except Exception as e:
        return jsonify({'code': 0, 'msg': f'获取文件信息失败: {str(e)}'})

@app.route('/api/excel-status')
def api_excel_status():
    """获取Excel文件状态信息"""
    try:
        ensure_orders_folder()
        excel_files = glob.glob(os.path.join(EXCEL_FOLDER, EXCEL_PATTERN))
        
        if excel_files:
            latest_file = max(excel_files, key=os.path.getctime)
            # 读取Excel文件获取最新状态
            df = pd.read_excel(latest_file, engine='openpyxl')
            
            # 统计各状态数量
            status_counts = df['状态'].value_counts().to_dict()
            
            return jsonify({
                'code': 1,
                'msg': 'success',
                'data': {
                    'file_name': os.path.basename(latest_file),
                    'last_modified': datetime.fromtimestamp(os.path.getmtime(latest_file)).isoformat(),
                    'status_counts': status_counts,
                    'total_orders': len(df)
                }
            })
        else:
            return jsonify({
                'code': 0,
                'msg': '未找到Excel文件',
                'data': None
            })
        
    except Exception as e:
        return jsonify({'code': 0, 'msg': f'获取Excel状态失败: {str(e)}'})

@app.route('/api/frontend-operations')
def api_frontend_operations():
    """获取前端操作记录"""
    try:
        operations_info = {}
        for order_id, operation_time in frontend_operations.items():
            operations_info[order_id] = {
                'operation_time': operation_time.isoformat(),
                'time_ago': str(datetime.now() - operation_time)
            }
        
        return jsonify({
            'code': 1,
            'msg': 'success',
            'data': {
                'operations_count': len(frontend_operations),
                'operations': operations_info
            }
        })
        
    except Exception as e:
        return jsonify({'code': 0, 'msg': f'获取前端操作记录失败: {str(e)}'})

# 导出函数供main.py使用
def init_app():
    """初始化应用"""
    print("📊 初始化数据读取...")
    read_excel_orders()
    
    # 启动后台Excel读取线程
    excel_thread = threading.Thread(target=background_excel_reader, daemon=True)
    excel_thread.start()
    print("🔄 后台Excel读取线程已启动，每分钟刷新一次")

def run_app():
    """运行Flask应用"""
    app.run(debug=False, host='0.0.0.0', port=5000) 