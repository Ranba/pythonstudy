import os
import sys

def main():
    # 检查命令行参数
    if len(sys.argv) > 1:
        video_url = sys.argv[1]  # 从命令行获取视频链接
    else:
        video_url = input("请输入视频链接：")  # 提示用户输入视频链接

    # 构建 yt-dlp 命令
    command = f"yt-dlp -f 'bestvideo+bestaudio' --merge-output-format mp4 --embed-metadata --write-subs --embed-subs --sub-langs zh-hans {video_url}"

    # 执行命令
    os.system(command)

    print("下载完成！")

if __name__ == "__main__":
    main()
