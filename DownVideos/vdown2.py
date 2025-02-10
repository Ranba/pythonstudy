import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import yt_dlp
import os
import json

class YoutubeDownloaderGUI:
    def __init__(self, master):
        self.master = master
        master.title("YouTube Downloader")

        self.last_download_path = tk.StringVar(value=self.load_last_path())
        self.video_info = None

        # **视频链接输入框**
        self.url_label = ttk.Label(master, text="视频链接:")
        self.url_label.grid(row=0, column=0, padx=10, pady=5, sticky=tk.W)
        self.url_entry = ttk.Entry(master, width=50)
        self.url_entry.grid(row=0, column=1, padx=10, pady=5, sticky=tk.EW)

        # **解析按钮**
        self.parse_button = ttk.Button(master, text="解析", command=self.parse_url)
        self.parse_button.grid(row=0, column=2, padx=10, pady=5)

        # **标题标签**
        self.title_label = ttk.Label(master, text="标题:")
        self.title_label.grid(row=1, column=0, padx=10, pady=5, sticky=tk.W)
        self.title_value = tk.StringVar()
        self.title_display = ttk.Label(master, textvariable=self.title_value)
        self.title_display.grid(row=1, column=1, padx=10, pady=5, sticky=tk.W)

        # **时长标签**
        self.duration_label = ttk.Label(master, text="时长:")
        self.duration_label.grid(row=2, column=0, padx=10, pady=5, sticky=tk.W)
        self.duration_value = tk.StringVar()
        self.duration_display = ttk.Label(master, textvariable=self.duration_value)
        self.duration_display.grid(row=2, column=1, padx=10, pady=5, sticky=tk.W)

        # **下载按钮**
        self.download_button = ttk.Button(master, text="下载最佳质量", command=self.download_best)
        self.download_button.grid(row=3, column=1, padx=10, pady=10)

        # **进度条**
        self.progress_bar = ttk.Progressbar(master, orient="horizontal", length=300, mode="determinate")
        self.progress_bar.grid(row=4, column=0, columnspan=3, padx=10, pady=5, sticky=tk.EW)
        self.progress_bar["value"] = 0

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

                self.video_info = info
                self.title_value.set(info.get('title', ''))
                self.duration_value.set(str(info.get('duration', '')))

        except Exception as e:
            messagebox.showerror("解析错误", str(e))

    def download_best(self):
        if not self.video_info:
            messagebox.showerror("错误", "请先解析视频链接")
            return

        download_path = filedialog.askdirectory(initialdir=self.last_download_path.get(), title="选择下载目录")
        if not download_path:
            return

        self.save_last_path(download_path)
        self.last_download_path.set(download_path)

        video_title = self.video_info.get('title', 'video')
        output_template = os.path.join(download_path, f"{video_title}.%(ext)s")

        ydl_opts = {
            'format': 'bestvideo+bestaudio/best',
            'merge_output_format': 'mp4',
            'outtmpl': output_template,
            'progress_hooks': [self.progress_hook],
            'quiet': True,
        }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([self.video_info['webpage_url']])
            messagebox.showinfo("完成", "下载完成！")

        except Exception as e:
            messagebox.showerror("下载错误", str(e))
        finally:
            self.progress_bar["value"] = 0

    def progress_hook(self, d):
        if d['status'] == 'downloading':
            percentage = d['_percent_str']
            #print(d)
            #print(percentage)
            try:
                percentage = float(percentage.strip('%'))
                self.progress_bar["value"] = percentage
                self.master.update_idletasks()
            except:
                pass

root = tk.Tk()
gui = YoutubeDownloaderGUI(root)
root.mainloop()
