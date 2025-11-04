import os
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from matplotlib import font_manager

# 导出目录（若设置则保存图片而不是show）
EXPORT_DIR = os.getenv('EXPORT_DIR')
page_no = 1

def save_show():
    global page_no
    if EXPORT_DIR:
        os.makedirs(EXPORT_DIR, exist_ok=True)
        out_path = os.path.join(EXPORT_DIR, f"page_{page_no}.png")
        plt.savefig(out_path, dpi=180, bbox_inches='tight')
        page_no += 1
        plt.close()
    else:
        plt.show()

# 尝试自动查找中文字体（支持多系统）
def get_chinese_font():
    try:
        # 尝试加载常见中文字体
        fonts = ["SimHei", "WenQuanYi Micro Hei", "Heiti TC", "Arial Unicode MS"]
        for font in fonts:
            font_prop = font_manager.FontProperties(family=font)
            if font_prop.get_name() == font:
                return font_prop
        # 如果找不到上述字体，尝试通过路径加载
        import sys
        if sys.platform.startswith('win'):
            font_path = "C:/Windows/Fonts/simhei.ttf"
        elif sys.platform.startswith('darwin'):  # macOS
            font_path = "/Library/Fonts/SimHei.ttf"
        else:  # Linux
            font_path = "/usr/share/fonts/truetype/wqy/wqy-microhei.ttc"
        
        return font_manager.FontProperties(fname=font_path)
    except:
        #  fallback方案，确保不报错
        return font_manager.FontProperties()

# 获取中文字体
my_font = get_chinese_font()

# 设置全局字体（避免重复设置）
plt.rcParams["font.family"] = my_font.get_family()
plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题

# 绘图示例
plt.figure(figsize=(10, 6))
plt.title('爆款系数随时间变化趋势', fontsize=15, fontweight='bold')
plt.xlabel('发布时间')
plt.ylabel('爆款系数')

# 假设的标注示例（补充完整参数）
title_text = "示例爆款"  # 假设的爆款标题
plt.annotate(
    f"爆款:{title_text}",
    xy=(0.5, 0.5),  # 标注位置
    xytext=(0.6, 0.6),  # 文本位置
    arrowprops=dict(facecolor='black', shrink=0.05),
    fontsize=9
)

# 图例示例
plt.plot([1, 2, 3], label='趋势线')
plt.legend()

save_show()




import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib import font_manager
import pandas as pd

# 1. 设置中文字体
try:
    # 尝试设置中文字体
    plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'DejaVu Sans']
    plt.rcParams['axes.unicode_minus'] = False
    print("中文字体设置成功")
except:
    print("中文字体设置失败，使用默认字体")

# 2. 读取数据并预处理
# 注意：使用绝对路径，确保脚本可直接运行
df = pd.read_csv('/Users/danielcrystal/work/dididudu/bilibili_up_videos.csv')

# 转换时间列
df['发布时间'] = pd.to_datetime(df['发布时间'])

# 衍生字段
df['标题长度'] = df['标题'].astype(str).str.len()
df['互动率'] = (df['点赞数'] + df['评论数'] + df['收藏数']) / df['播放量']
# 定义爆款系数（可按需调整公式）
df['爆款系数'] = df['互动率']

# 发布时段特征
df['发布小时'] = df['发布时间'].dt.hour
df['发布星期'] = df['发布时间'].dt.day_name()

# 2. 确保时间列格式正确
# 如果'发布时间'是字符串，转换为datetime
if df['发布时间'].dtype == 'object':
    df['发布时间'] = pd.to_datetime(df['发布时间'])

# 3. 各视频爆款系数趋势图（修复版）
plt.figure(figsize=(14, 8))

# 按发布时间排序
df_sorted = df.sort_values('发布时间')

# 绘制趋势线
plt.plot(df_sorted['发布时间'], df_sorted['爆款系数'], 
         marker='o', linewidth=2, markersize=6, color='steelblue', label='爆款系数')

plt.title('爆款系数随时间变化趋势', fontsize=15, fontweight='bold')
plt.xlabel('发布时间')
plt.ylabel('爆款系数')
plt.grid(True, alpha=0.3)

# 4. 修复时间轴显示
# 自动调整x轴标签，避免重叠
plt.gcf().autofmt_xdate()

# 5. 修复标注文字显示
top3_indices = df_sorted.nlargest(3, '爆款系数').index

# 检查是否有足够的数据点
if len(top3_indices) > 0:
    for idx in top3_indices:
        # 简化标注文字，避免特殊字符
        title_text = str(df_sorted.loc[idx, '标题'])[:8]  # 取前8个字符
        # 移除可能引起问题的字符
        title_text = ''.join(char for char in title_text if char.isalnum() or char in ' -_')
        
        plt.annotate(f"爆款:{title_text}", 
                    xy=(df_sorted.loc[idx, '发布时间'], df_sorted.loc[idx, '爆款系数']),
                    xytext=(15, 15), 
                    textcoords='offset points',
                    bbox=dict(boxstyle='round,pad=0.3', facecolor='yellow', alpha=0.7),
                    arrowprops=dict(arrowstyle='->', color='red', lw=1.5),
                    fontsize=9)
else:
    print("没有找到爆款视频数据")

plt.legend()
plt.tight_layout()
save_show()

# 6. 调试信息
print(f"数据点数: {len(df_sorted)}")
print(f"爆款系数范围: {df_sorted['爆款系数'].min():.3f} - {df_sorted['爆款系数'].max():.3f}")
print(f"时间范围: {df_sorted['发布时间'].min()} 到 {df_sorted['发布时间'].max()}")

#1. 各视频爆款系数趋势图
plt.figure(figsize=(14, 8))

# 按发布时间排序
df_sorted = df.sort_values('发布时间')

plt.plot(df_sorted['发布时间'], df_sorted['爆款系数'], 
         marker='o', linewidth=2, markersize=4)
plt.title('爆款系数随时间变化趋势', fontsize=15, fontweight='bold')
plt.xlabel('发布时间')
plt.ylabel('爆款系数')
plt.xticks(rotation=45)
plt.grid(True, alpha=0.3)

# 标注爆款视频
top3_indices = df_sorted.nlargest(3, '爆款系数').index
for idx in top3_indices:
    plt.annotate(f"爆款{df_sorted.loc[idx, '标题'][:10]}...", 
                xy=(df_sorted.loc[idx, '发布时间'], df_sorted.loc[idx, '爆款系数']),
                xytext=(10, 10), textcoords='offset points',
                arrowprops=dict(arrowstyle='->', color='red'))

plt.tight_layout()
save_show()


#2. 标题长度与播放量关系图
plt.figure(figsize=(12, 6))

# 散点图
plt.subplot(1, 2, 1)
plt.scatter(df['标题长度'], df['播放量'], alpha=0.6, color='steelblue')
plt.xlabel('标题长度')
plt.ylabel('播放量')
plt.title('标题长度 vs 播放量')

# 箱型图 - 按标题长度分组
plt.subplot(1, 2, 2)
df['标题长度分组'] = pd.cut(df['标题长度'], bins=5)
df_grouped = df.groupby('标题长度分组')['播放量'].mean().reset_index()
plt.bar(range(len(df_grouped)), df_grouped['播放量'])
plt.xticks(range(len(df_grouped)), [f"{int(x.left)}-{int(x.right)}" 
                                   for x in df_grouped['标题长度分组']], rotation=45)
plt.xlabel('标题长度区间')
plt.ylabel('平均播放量')
plt.title('不同标题长度的平均播放量')

plt.tight_layout()
save_show()


#3. 发布时段热力图
# 创建发布小时与星期的交叉表
pivot_data = df.pivot_table(values='播放量', 
                           index='发布星期', 
                           columns='发布小时', 
                           aggfunc='mean')

# 确保星期顺序正确
days_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 
              'Friday', 'Saturday', 'Sunday']
pivot_data = pivot_data.reindex(days_order)

plt.figure(figsize=(16, 8))
sns.heatmap(pivot_data, 
            cmap='YlOrRd', 
            annot=True, 
            fmt='.0f',
            cbar_kws={'label': '平均播放量'})
plt.title('发布时段热力图 (周几 vs 几点)', fontsize=15, fontweight='bold')
plt.xlabel('发布小时')
plt.ylabel('星期')
plt.tight_layout()
save_show()


# 关键洞察总结
print("=== UP主视频数据分析报告 ===")
print(f"分析视频数量: {len(df)}")
print(f"时间范围: {df['发布时间'].min()} 至 {df['发布时间'].max()}")
print(f"\n核心指标:")
print(f"平均播放量: {df['播放量'].mean():.0f}")
print(f"平均互动率: {df['互动率'].mean():.3f}")
print(f"最高爆款系数: {df['爆款系数'].max():.3f}")

# 最佳发布时间分析
best_hour = df.groupby('发布小时')['播放量'].mean().idxmax()
best_weekday = df.groupby('发布星期')['播放量'].mean().idxmax()

print(f"\n发布规律洞察:")
print(f"最佳发布小时: {best_hour}点")
print(f"最佳发布星期: {best_weekday}")

# 爆款视频分析
top_video = df.loc[df['爆款系数'].idxmax()]
print(f"\n爆款视频分析:")
print(f"标题: {top_video['标题']}")
print(f"爆款系数: {top_video['爆款系数']:.3f}")
print(f"播放量: {top_video['播放量']}")
print(f"互动率: {top_video['互动率']:.3f}")

# 标题长度建议
title_corr = df['标题长度'].corr(df['播放量'])
print(f"\n标题长度与播放量相关性: {title_corr:.3f}")

# 第四步：生成分析报告（控制台已输出关键指标）

# 第五步：高级分析（可选）
# 互动率与播放量关系
plt.figure(figsize=(10, 6))
plt.scatter(df['播放量'], df['互动率'], alpha=0.6)
plt.xlabel('播放量')
plt.ylabel('互动率')
plt.title('播放量 vs 互动率')
save_show()

# 多维度指标对比
fig, axes = plt.subplots(2, 2, figsize=(15, 12))
metrics = ['播放量', '点赞数', '评论数', '收藏数']
for i, metric in enumerate(metrics):
    ax = axes[i//2, i%2]
    df.nlargest(10, metric)[['标题', metric]].set_index('标题').plot(kind='bar', ax=ax)
    ax.set_title(f'Top 10 {metric}')
    ax.tick_params(axis='x', rotation=45)
plt.tight_layout()
save_show()