import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox

def center_window(window, width, height):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)
    window.geometry(f"{width}x{height}+{x}+{y}")

def init_db():
    conn = sqlite3.connect('email_aliases.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS AliasEmail (
                        ID INTEGER PRIMARY KEY AUTOINCREMENT,
                        AliasEmail TEXT NOT NULL,
                        OriginEmail TEXT NOT NULL,
                        Provider TEXT NOT NULL
                    )''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS PrivateEmail (
                        ID INTEGER PRIMARY KEY AUTOINCREMENT,
                        PrivateEmail TEXT NOT NULL,
                        AliasEmail TEXT NOT NULL
                    )''')
    conn.commit()
    conn.close()

def add_alias_email():
    def save_alias_email():
        alias_email = entry_alias_email.get()
        origin_email = entry_origin_email.get()
        provider = entry_provider.get()

        if not all([alias_email, origin_email, provider]):
            messagebox.showerror("Error", "All fields are required!")
            return

        conn = sqlite3.connect('email_aliases.db')
        cursor = conn.cursor()
        cursor.execute('''INSERT INTO AliasEmail (AliasEmail, OriginEmail, Provider)
                          VALUES (?, ?, ?)''', (alias_email, origin_email, provider))
        conn.commit()
        conn.close()

        messagebox.showinfo("Success", "Alias email added successfully!")
        alias_email_window.destroy()

    alias_email_window = tk.Toplevel(root)
    alias_email_window.title("Add Alias Email")
    center_window(alias_email_window, 400, 300)

    tk.Label(alias_email_window, text="Alias Email Address:").place(x=20, y=20)
    entry_alias_email = tk.Entry(alias_email_window)
    entry_alias_email.place(x=150, y=20)

    tk.Label(alias_email_window, text="Origin Email Address:").place(x=20, y=60)
    entry_origin_email = tk.Entry(alias_email_window)
    entry_origin_email.place(x=150, y=60)

    tk.Label(alias_email_window, text="Provider:").place(x=20, y=100)
    entry_provider = tk.Entry(alias_email_window)
    entry_provider.place(x=150, y=100)

    tk.Button(alias_email_window, text="Save", command=save_alias_email).place(x=150, y=160)

def add_private_email():
    def save_private_email():
        private_email = entry_private_email.get()
        selected_alias = alias_dropdown.get()

        if not all([private_email, selected_alias]):
            messagebox.showerror("Error", "All fields are required!")
            return

        conn = sqlite3.connect('email_aliases.db')
        cursor = conn.cursor()
        cursor.execute('''INSERT INTO PrivateEmail (PrivateEmail, AliasEmail)
                          VALUES (?, ?)''', (private_email, selected_alias))
        conn.commit()
        conn.close()

        messagebox.showinfo("Success", "Private email added successfully!")
        private_email_window.destroy()

    private_email_window = tk.Toplevel(root)
    private_email_window.title("Add Private Email")
    center_window(private_email_window, 400, 300)

    tk.Label(private_email_window, text="Private Email Address:").place(x=20, y=20)
    entry_private_email = tk.Entry(private_email_window)
    entry_private_email.place(x=150, y=20)

    tk.Label(private_email_window, text="Alias Email:").place(x=20, y=60)
    alias_dropdown = ttk.Combobox(private_email_window)
    alias_dropdown.place(x=150, y=60)

    conn = sqlite3.connect('email_aliases.db')
    cursor = conn.cursor()
    cursor.execute('''SELECT AliasEmail FROM AliasEmail''')
    aliases = [row[0] for row in cursor.fetchall()]
    conn.close()
    alias_dropdown['values'] = aliases

    tk.Button(private_email_window, text="Save", command=save_private_email).place(x=150, y=120)

def create_menu():
    menu_bar = tk.Menu(root)

    file_menu = tk.Menu(menu_bar, tearoff=0)
    file_menu.add_command(label="退出", command=root.quit)
    menu_bar.add_cascade(label="文件", menu=file_menu)

    add_menu = tk.Menu(menu_bar, tearoff=0)
    add_menu.add_command(label="添加别名邮箱", command=add_alias_email)
    add_menu.add_command(label="添加隐私邮箱", command=add_private_email)
    menu_bar.add_cascade(label="添加", menu=add_menu)

    root.config(menu=menu_bar)



# Initialize database
init_db()

# Create main window
root = tk.Tk()
root.title("Email Alias Manager")
center_window(root, 600, 400)

# Create menu
create_menu()

# Search box
tk.Label(root, text="Search by Email Address:").place(x=20, y=70)
entry_search = tk.Entry(root)
entry_search.place(x=200, y=70)
tk.Button(root, text="Search", command=add_private_email).place(x=400, y=70)

# Display search results
tk.Label(root, text="Alias:").place(x=20, y=110)
entry_alias_display = tk.Entry(root)
entry_alias_display.place(x=150, y=110)

tk.Label(root, text="Forwarding To:").place(x=20, y=150)
entry_forwarding_display = tk.Entry(root)
entry_forwarding_display.place(x=150, y=150)

tk.Label(root, text="Provider:").place(x=20, y=190)
entry_provider_display = tk.Entry(root)
entry_provider_display.place(x=150, y=190)

# Run the application
root.mainloop()
