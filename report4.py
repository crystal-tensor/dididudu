第四步：生成分析报告
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