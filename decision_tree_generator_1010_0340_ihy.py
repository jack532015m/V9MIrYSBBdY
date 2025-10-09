# 代码生成时间: 2025-10-10 03:40:28
import csv
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from celery import Celery
from celery import shared_task

# 初始化Celery应用
app = Celery('decision_tree_generator')
app.conf.broker_url = 'amqp://guest@localhost//'
app.conf.result_backend = 'rpc://'

"""
决策树生成器任务
此函数接受CSV文件路径作为输入，生成并保存决策树模型。
"""
@shared_task
def generate_decision_tree(csv_path, target_column):
    """
    :param csv_path: CSV文件路径，包含用于训练决策树的数据
    :param target_column: 目标列名，用于训练决策树的标签列
    :return: 决策树模型的准确性
    """
    try:
        # 读取CSV文件
        with open(csv_path, newline='') as csvfile:
            datareader = csv.DictReader(csvfile)
            data = [row for row in datareader]
            
        # 提取特征和标签
        features = [row.keys() - {target_column} for row in data]
        feature_values = [list(row.values()) for row in data]
        
        # 将标签转换为数值类型
        labels = [int(row[target_column]) for row in data]
        
        # 划分训练集和测试集
        X_train, X_test, y_train, y_test = train_test_split(
            feature_values, labels, test_size=0.2, random_state=42
        )
        
        # 训练决策树模型
        clf = DecisionTreeClassifier()
        clf.fit(X_train, y_train)
        
        # 预测测试集
        y_pred = clf.predict(X_test)
        
        # 计算模型准确性
        accuracy = accuracy_score(y_test, y_pred)
        
        # 返回模型准确性
        return accuracy
    except Exception as e:
        # 处理任何异常
        return f"An error occurred: {str(e)}"

# 以下是示例代码，展示如何调用generate_decision_tree任务
# result = generate_decision_tree.delay('data.csv', 'target')
# print(f"Model accuracy: {result.get()}")