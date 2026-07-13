import yt_dlp
import os
from tkinter import *
from tkinter import filedialog, messagebox

def download_video():
    url = url_entry.get()
    output_dir = output_dir_var.get()

    if not url:
        messagebox.showerror("错误", "请输入视频链接")
        return

    if not output_dir:
        messagebox.showerror("错误", "请选择输出目录")
        return

    ydl_opts = {
        'format': 'bv*+ba/best',
        'merge_output_format': 'mp4',
        'writesubtitles': True,
        'embed-subs': True,
        'outtmpl': os.path.join(output_dir, '%(title)s.%(ext)s'),
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        messagebox.showinfo("成功", "视频下载完成！")
    except Exception as e:
        messagebox.showerror("错误", f"下载失败: {e}")

def select_output_directory():
    directory = filedialog.askdirectory()
    if directory:
        output_dir_var.set(directory)

# 创建主窗口
root = Tk()
root.title("YouTube 视频下载器")
root.geometry('500x300')

# 视频链接输入框
Label(root, text='粘贴视频链接:', font=('Arial', 12)).pack(pady=10)
url_entry = Entry(root, width=60)
url_entry.pack(pady=5)

# 输出目录选择
output_dir_var = StringVar()
Label(root, text='选择输出目录:', font=('Arial', 12)).pack(pady=10)
output_dir_entry = Entry(root, textvariable=output_dir_var, width=60)
output_dir_entry.pack(pady=5)
Button(root, text='浏览', command=select_output_directory).pack(pady=5)

# 下载按钮
Button(root, text='下载视频', font=('Arial', 12), command=download_video).pack(pady=20)

# 启动主循环
root.mainloop()
