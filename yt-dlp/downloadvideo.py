import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
import yt_dlp

def download_video():
    url = url_entry.get()
    output_dir = output_dir_entry.get()

    if not url:
        messagebox.showerror("Error", "Please enter a YouTube video URL.")
        return

    if not output_dir:
        messagebox.showerror("Error", "Please select an output directory.")
        return

    ydl_opts = {
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
        'outtmpl': output_dir + '/%(title)s.%(ext)s'
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            ydl.download([url])
            messagebox.showinfo("Success", "Video downloaded successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

def select_output_dir():
    output_dir = filedialog.askdirectory()
    output_dir_entry.delete(0, tk.END)
    output_dir_entry.insert(0, output_dir)

# Create GUI window
root = tk.Tk()
root.title("YouTube Video Downloader")

# URL Entry
url_label = tk.Label(root, text="Enter YouTube Video URL:")
url_label.pack()
url_entry = tk.Entry(root, width=50)
url_entry.pack()

# Output Directory Entry
output_dir_label = tk.Label(root, text="Select Output Directory:")
output_dir_label.pack()
output_dir_entry = tk.Entry(root, width=50)
output_dir_entry.pack()
output_dir_button = tk.Button(root, text="Browse", command=select_output_dir)
output_dir_button.pack()

# Download Button
download_button = tk.Button(root, text="Download", command=download_video)
download_button.pack()

# Run the GUI
root.mainloop()
