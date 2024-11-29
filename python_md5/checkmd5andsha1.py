import hashlib
import tkinter as tk
from tkinter import filedialog
from tkinter import simpledialog
from tkinter import messagebox

def calculate_md5(file_path):
    md5_hash = hashlib.md5()
    
    with open(file_path, 'rb') as f:
        while chunk := f.read(8192):
            md5_hash.update(chunk)
    
    return md5_hash.hexdigest()

def open_file():
    file_path = filedialog.askopenfilename()
    if file_path:
        md5 = calculate_md5(file_path)
        messagebox.showinfo("MD5 Hash", f"MD5: {md5}")

        user_md5 = simpledialog.askstring("Input", "Enter MD5 for verification:")
        
        if user_md5 == md5:
            messagebox.showinfo("Verification", "MD5 match!")
        else:
            messagebox.showerror("Verification", "MD5 do not match!")

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    open_file()

