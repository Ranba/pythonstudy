import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import yt_dlp
import json
import os

class YoutubeDownloaderGUI:
    def __init__(self, master):
        self.master = master
        master.title("YouTube Downloader")

        self.last_download_path = tk.StringVar(value=self.load_last_path())

        # **视频链接输入框**
        self.url_label = ttk.Label(master, text="视频链接:")
        self.url_label.grid(row=0, column=0, padx=10, pady=5, sticky=tk.W)
        self.url_entry = ttk.Entry(master, width=50)
        self.url_entry.grid(row=0, column=1, padx=10, pady=5, sticky=tk.EW)

        # **解析按钮**
        self.parse_button = ttk.Button(master, text="解析", command=self.parse_url)
        self.parse_button.grid(row=0, column=2, padx=10, pady=5)

        # **视频信息列表**
        self.info_label = ttk.Label(master, text="可用格式:")
        self.info_label.grid(row=1, column=0, padx=10, pady=5, sticky=tk.W)
        self.info_list = tk.Listbox(master, width=70, height=15)
        self.info_list.grid(row=2, column=0, columnspan=3, padx=10, pady=5, sticky=tk.EW)

        # **下载按钮**
        self.download_button = ttk.Button(master, text="下载", command=self.download_selected)
        self.download_button.grid(row=3, column=1, padx=10, pady=10)
    
    def load_last_path(self):
        try:
            with open("last_path.json", "r") as f:
                data = json.load(f)
                return data.get("last_path", "")
        except FileNotFoundError:
            return ""

    def save_last_path(self, path):
        with open("last_path.json", "w") as f:
            json.dump({"last_path": path}, f)

    def parse_url(self):
        url = self.url_entry.get()
        if not url:
            messagebox.showerror("错误", "请输入视频链接")
            return

        try:
            ydl_opts = {
                'quiet': True,
                'no_warnings': True,
                'simulate': True,
                'forceprint': True,
            }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)

                self.info_list.delete(0, tk.END)
                self.info_list.insert(tk.END, f"标题: {info.get('title')}")
                self.info_list.insert(tk.END, f"时长: {info.get('duration')} 秒")
                self.info_list.insert(tk.END, "----------------------")

                for idx, format_info in enumerate(info.get('formats', [])):
                    format_string = f"{idx}: {format_info.get('format_note', '未知')} - {format_info.get('ext', '未知')} - {format_info.get('width', '未知')}x{format_info.get('height', '未知')} - {format_info.get('filesize_approx', '未知')} 字节"
                    self.info_list.insert(tk.END, format_string)

                self.video_info = info  # 保存视频信息，供下载时使用

        except Exception as e:
            messagebox.showerror("解析错误", str(e))

    def download_selected(self):
        try:
            selected_index = self.info_list.curselection()
            if not selected_index:
                messagebox.showerror("错误", "请选择要下载的格式")
                return

            selected_index = int(selected_index[0])
            if selected_index < 3:
                messagebox.showerror("错误", "请选择视频或音频格式，不要选择标题或时长")
                return

            format_index = selected_index - 3  # 减去标题、时长和分隔符的行数
            selected_format = self.video_info['formats'][format_index]

            download_path = filedialog.askdirectory(initialdir=self.last_download_path.get(), title="选择下载目录")
            if not download_path:
                return  # 用户取消选择

            self.save_last_path(download_path)
            self.last_download_path.set(download_path)

            ydl_opts = {
                'format': selected_format['format_id'],
                'outtmpl': os.path.join(download_path, f"{self.video_info['title']}.%(ext)s"),
                'quiet': False,
            }

            def download_hook(d):
                if d['status'] == 'finished':
                    messagebox.showinfo("完成", "下载完成！")

            ydl_opts['progress_hooks'] = [download_hook]

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([self.video_info['webpage_url']])

        except Exception as e:
            messagebox.showerror("下载错误", str(e))

root = tk.Tk()
gui = YoutubeDownloaderGUI(root)
root.mainloop()
