# 代码生成时间: 2025-09-23 15:25:33
import os
from celery import Celery

# 设置Celery
os.environ.setdefault('CELERY_BROKER_URL', 'redis://localhost:6379/0')
os.environ.setdefault('CELERY_RESULT_BACKEND', 'redis://localhost:6379/0')

app = Celery('shopping_cart', broker=os.environ['CELERY_BROKER_URL'],
             backend=os.environ['CELERY_RESULT_BACKEND'])


# 购物车类定义
class ShoppingCart:
    def __init__(self):
        self.items = []

    def add_item(self, item):
        """添加商品到购物车
        :param item: {'name': '商品名称', 'quantity': '商品数量', 'price': '商品价格'}
        :type item: dict
        :return: None
        """
        if not isinstance(item, dict) or 'name' not in item or 'quantity' not in item or 'price' not in item:
            raise ValueError('Invalid item format')
        self.items.append(item)

    def remove_item(self, item_name):
        """从购物车中移除商品
        :param item_name: 商品名称
        :return: None
        """
        self.items = [item for item in self.items if item['name'] != item_name]

    def get_total_price(self):
        """计算购物车中所有商品的总价
        :return: 总价
        """
        total_price = sum(item['quantity'] * item['price'] for item in self.items)
        return total_price


# 异步任务：添加商品到购物车
@app.task
def async_add_item(cart_id, item):
    try:
        cart = ShoppingCart()
        cart.add_item(item)
        # 这里可以添加代码将购物车保存到数据库或缓存
        print(f'Item added to cart {cart_id}')
    except ValueError as e:
        print(f'Error adding item to cart {cart_id}: {e}')


# 异步任务：从购物车中移除商品
@app.task
def async_remove_item(cart_id, item_name):
    try:
        cart = ShoppingCart()
        cart.remove_item(item_name)
        # 这里可以添加代码将购物车保存到数据库或缓存
        print(f'Item removed from cart {cart_id}')
    except Exception as e:
        print(f'Error removing item from cart {cart_id}: {e}')


# 异步任务：计算购物车总价
@app.task
def async_get_total_price(cart_id):
    try:
        cart = ShoppingCart()
        total_price = cart.get_total_price()
        # 这里可以添加代码将购物车总价保存到数据库或缓存
        print(f'Total price for cart {cart_id} is {total_price}')
    except Exception as e:
        print(f'Error calculating total price for cart {cart_id}: {e}')
