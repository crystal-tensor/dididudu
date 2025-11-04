from bilibili_api import user, video
import asyncio
import pandas as pd
import time

async def get_up_videos(uid: int):
    u = user.User(uid)
    try:
        # 获取UP主视频数据（返回包含vlist的字典）
        video_dict = await u.get_videos()
    except Exception as e:
        print("get_videos() 调用异常：")
        print(e)
        return []

    print("视频数据总结构类型：", type(video_dict))
    data = []
    try:
        # 提取真正的视频列表（从dict的list→vlist路径获取）
        real_video_list = video_dict.get('list', {}).get('vlist', [])
        if not real_video_list:
            print("未找到有效的视频列表（vlist为空）")
            return data

        # 循环处理每个视频（v是包含bvid的字典）
        for v in real_video_list:
            print(f"\n正在处理视频：{v.get('title', '未知标题')}")
            bvid = v.get('bvid')  # 直接从字典获取bvid
            
            # 过滤无效BV号
            if not bvid or not bvid.startswith('BV'):
                print(f"跳过无效BV号：{bvid}")
                continue

            try:
                # 获取视频详细信息
                v_info = await video.Video(bvid=bvid).get_info()
                # 提取需要的字段
                data.append({
                    '标题': v_info['title'],
                    'BV号': v_info['bvid'],
                    '发布时间': time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(v_info['pubdate'])),
                    '播放量': v_info['stat']['view'],
                    '点赞数': v_info['stat']['like'],
                    '评论数': v_info['stat']['reply'],
                    '收藏数': v_info['stat']['favorite'],
                })
                print(f"成功获取视频：{v_info['title']}")
            except Exception as e:
                print(f"获取视频 {bvid} 信息失败：", e)
    except Exception as e:
        print(f"解析视频列表失败：{e}")
    return data

async def main():
    uid = 520819684  # 替换为目标UP主的UID（纯数字）
    videos_data = await get_up_videos(uid)
    
    if videos_data:
        # 保存数据到CSV
        df = pd.DataFrame(videos_data)
        df.to_csv('bilibili_up_videos.csv', index=False, encoding='utf-8-sig')
        print(f"\n===== 任务完成 =====")
        print(f"共成功获取 {len(videos_data)} 个视频数据")
        print(f"数据已保存到：bilibili_up_videos.csv")
    else:
        print("\n未获取到任何视频数据")

if __name__ == "__main__":
    asyncio.run(main())