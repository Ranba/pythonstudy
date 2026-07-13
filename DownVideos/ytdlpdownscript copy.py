import yt_dlp

def download_video():
    # 用户输入视频链接
    url = input("请输入视频链接: ")

    # 配置下载选项
    ydl_opts = {
        'format': 'bv*+ba/best',  # 下载最佳视频和音频流并合并
        'merge_output_format': 'mp4',  # 合并后的格式为MP4
        'writesubtitles': True,  # 下载字幕
        'embed-subs': True,  # 将字幕嵌入视频中
        'outtmpl': '%(title)s.%(ext)s',  # 输出文件名格式
    }

    # 使用yt-dlp下载视频
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

# 调用下载函数
download_video()