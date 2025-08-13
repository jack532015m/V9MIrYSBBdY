# 代码生成时间: 2025-08-14 06:40:35
import os
from celery import Celery

# 设置Celery应用
app = Celery('inventory', broker=os.environ.get('CELERY_BROKER_URL'))

# 库存管理器
class InventoryManager:
    def __init__(self):
        self.inventory = {}

    # 增加库存
    def add_stock(self, product_id, quantity):
        if product_id not in self.inventory:
            self.inventory[product_id] = 0
        self.inventory[product_id] += quantity
        return self.inventory[product_id]

    # 减少库存
    def reduce_stock(self, product_id, quantity):
        if product_id not in self.inventory:
            raise ValueError(f"Product {product_id} does not exist in inventory.")
        if self.inventory[product_id] < quantity:
            raise ValueError(f"Not enough stock for product {product_id}.")
        self.inventory[product_id] -= quantity
        return self.inventory[product_id]

    # 获取库存
    def get_stock(self, product_id):
        return self.inventory.get(product_id, 0)

# Celery任务
@app.task
def add_stock_task(product_id, quantity):
    inventory_manager = InventoryManager()
    return inventory_manager.add_stock(product_id, quantity)

@app.task
def reduce_stock_task(product_id, quantity):
    inventory_manager = InventoryManager()
    return inventory_manager.reduce_stock(product_id, quantity)

# 如果这是主模块，则运行worker
if __name__ == '__main__':
    app.start()
