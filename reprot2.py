# # 第二步：数据清洗与特征工程
# # 1. 发布时间处理
# import pandas as pd
# import matplotlib.pyplot as plt
# import seaborn as sns
# from datetime import datetime
# import numpy as np

# # 设置中文字体和图形样式
# plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
# plt.rcParams['axes.unicode_minus'] = False   # 用来正常显示负号
# sns.set_style("whitegrid")

# df['发布时间'] = pd.to_datetime(df['发布时间'])  
# df['发布日期'] = df['发布时间'].dt.date
# df['发布小时'] = df['发布时间'].dt.hour
# df['发布星期'] = df['发布时间'].dt.day_name()

# # 2. 标题长度分析
# df['标题长度'] = df['标题'].str.len()

# # 3. 计算核心指标
# # 注意：这里需要'粉丝数'，如果csv里没有，需要从其他地方获取或估算
# # 假设df中有'粉丝数'列，或者你用UP主当前粉丝数（一个常数）替代
# current_fans = 100000  # 示例值，请替换为实际粉丝数

# df['爆款系数'] = (df['播放量'] * 0.3 + df['点赞数'] * 0.3 + 
#                  df['投币数'] * 0.2 + df['收藏数'] * 0.2) / current_fans

# df['互动率'] = (df['点赞数'] + df['评论数'] + df['收藏数'] + df['分享数']) / df['播放量']

# # 4. 创建时间段标签
# df['时间段'] = pd.cut(df['发布小时'], 
#                      bins=[0, 6, 12, 18, 24], 
#                      labels=['凌晨', '上午', '下午', '晚上'])


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




# 1. 发布时间处理
df['发布时间'] = pd.to_datetime(df['发布时间'])  
df['发布日期'] = df['发布时间'].dt.date
df['发布小时'] = df['发布时间'].dt.hour
df['发布星期'] = df['发布时间'].dt.day_name()

# 2. 标题长度分析
df['标题长度'] = df['标题'].str.len()

# 3. 计算核心指标
# 注意：这里需要'粉丝数'，如果csv里没有，需要从其他地方获取或估算
# 假设df中有'粉丝数'列，或者你用UP主当前粉丝数（一个常数）替代
current_fans = 100000  # 示例值，请替换为实际粉丝数

# 确保用于计算的数值列存在；缺失时填充为 0，并转换为数值类型
required_numeric_cols = ['播放量', '点赞数', '评论数', '收藏数', '投币数']
for col in required_numeric_cols:
    if col not in df.columns:
        df[col] = 0
for col in required_numeric_cols:
    df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
print("提示：如缺少 '投币数' 列，已填充为 0 用于计算。")
df['爆款系数'] = (df['播放量'] * 0.3 + df['点赞数'] * 0.3 + 
                 df['投币数'] * 0.2 + df['收藏数'] * 0.2) / current_fans

df['互动率'] = (df['点赞数'] + df['评论数'] + df['收藏数'] + df['分享数']) / df['播放量']

# 4. 创建时间段标签
df['时间段'] = pd.cut(df['发布小时'], 
                     bins=[0, 6, 12, 18, 24], 
                     labels=['凌晨', '上午', '下午', '晚上'])