# 第一步：数据加载与探索
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import numpy as np

# 设置中文字体和图形样式
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False   # 用来正常显示负号
sns.set_style("whitegrid")

# 加载数据
df = pd.read_csv('bilibili_up_videos.csv')

# 查看数据基本信息和前几行
print("数据形状:", df.shape)
print("\n数据列名:", df.columns.tolist())
print("\n前5行数据:")
print(df.head())

# 检查缺失值
print("\n缺失值情况:")
print(df.isnull().sum())

