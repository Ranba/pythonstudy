import tkinter as tk
from tkinter import filedialog, ttk
import yt_dlp

def download_videos():
    urls = url_text.get("1.0", tk.END).strip().split("\n")
    output_dir = output_dir_entry.get()

    if not urls or urls == ['']:
        log_message("Error: Please enter at least one YouTube video URL.")
        return

    if not output_dir:
        log_message("Error: Please select an output directory.")
        return

    ydl_opts = {
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
        'outtmpl': output_dir + '/%(title)s.%(ext)s',
        'progress_hooks': [progress_hook],
        'nocolor': True  # Disable color in the output
    }

    progress_bar['value'] = 0
    progress_bar['maximum'] = len(urls)

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        for i, url in enumerate(urls):
            try:
                global current_video_index
                current_video_index = i
                log_message(f"Starting download: {url}")
                ydl.download([url])
                progress_bar['value'] = i + 1
                root.update_idletasks()
                log_message(f"Completed download: {url}")
            except Exception as e:
                log_message(f"Error occurred with {url}: {e}")
                break

    log_message("Download process completed.")

def progress_hook(d):
    if d['status'] == 'downloading':
        percent_str = d['_percent_str'].strip('%')
        try:
            percent = float(percent_str)
        except ValueError:
            percent = 0  # Handle case where percent_str cannot be converted to float
        detailed_progress_bar['value'] = percent
        detailed_progress_label.config(text=f"Downloading: {percent_str}%")
    elif d['status'] == 'finished':
        detailed_progress_bar['value'] = 100
        detailed_progress_label.config(text="Download complete")

def select_output_dir():
    output_dir = filedialog.askdirectory()
    output_dir_entry.delete(0, tk.END)
    output_dir_entry.insert(0, output_dir)

def log_message(message):
    log_text.config(state=tk.NORMAL)
    log_text.insert(tk.END, message + "\n")
    log_text.config(state=tk.DISABLED)
    log_text.yview(tk.END)

# Create GUI window
root = tk.Tk()
root.title("YouTube Video Downloader")

# URL Entry Label
url_label = tk.Label(root, text="Enter YouTube Video URLs (one per line):")
url_label.grid(row=0, column=0, padx=10, pady=5)

# URL Text Box
url_text = tk.Text(root, height=10, width=50)
url_text.grid(row=1, column=0, padx=10, pady=5)

# Output Directory Entry
output_dir_label = tk.Label(root, text="Select Output Directory:")
output_dir_label.grid(row=2, column=0, padx=10, pady=5)
output_dir_entry = tk.Entry(root, width=50)
output_dir_entry.grid(row=3, column=0, padx=10, pady=5)
output_dir_button = tk.Button(root, text="Browse", command=select_output_dir)
output_dir_button.grid(row=3, column=1, padx=10, pady=5)

# Download Button
download_button = tk.Button(root, text="Download", command=download_videos)
download_button.grid(row=4, column=0, padx=10, pady=5)

# Progress Bar
progress_bar = ttk.Progressbar(root, orient='horizontal', length=400, mode='determinate')
progress_bar.grid(row=5, column=0, padx=10, pady=5)

# Detailed Progress Bar and Label
detailed_progress_label = tk.Label(root, text="")
detailed_progress_label.grid(row=6, column=0, padx=10, pady=5)
detailed_progress_bar = ttk.Progressbar(root, orient='horizontal', length=400, mode='determinate')
detailed_progress_bar.grid(row=7, column=0, padx=10, pady=5)

# Log Text Box
log_label = tk.Label(root, text="Log Output:")
log_label.grid(row=0, column=1, padx=10, pady=5)
log_text = tk.Text(root, height=25, width=50, state=tk.DISABLED)
log_text.grid(row=1, column=1, rowspan=7, padx=10, pady=5)

# Run the GUI
root.mainloop()
