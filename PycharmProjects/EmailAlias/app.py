import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox


def init_db():
    conn = sqlite3.connect('email_aliases.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS EmailAliases (
                        ID INTEGER PRIMARY KEY AUTOINCREMENT,
                        EmailAddress TEXT NOT NULL,
                        EmailAlias TEXT NOT NULL,
                        ForwardingTo TEXT NOT NULL,
                        Provider TEXT NOT NULL
                    )''')
    conn.commit()
    conn.close()


def add_alias():
    def save_alias():
        email_address = entry_email.get()
        email_alias = entry_alias.get()
        forwarding_to = entry_forwarding.get()
        provider = entry_provider.get()

        if not all([email_address, email_alias, forwarding_to, provider]):
            messagebox.showerror("Error", "All fields are required!")
            return

        conn = sqlite3.connect('email_aliases.db')
        cursor = conn.cursor()
        cursor.execute('''INSERT INTO EmailAliases (EmailAddress, EmailAlias, ForwardingTo, Provider)
                          VALUES (?, ?, ?, ?)''', (email_address, email_alias, forwarding_to, provider))
        conn.commit()
        conn.close()

        messagebox.showinfo("Success", "Alias added successfully!")
        add_window.destroy()

    add_window = tk.Toplevel(root)
    add_window.title("Add Email Alias")
    add_window.geometry("400x300")

    tk.Label(add_window, text="Email Address:").place(x=20, y=20)
    entry_email = tk.Entry(add_window)
    entry_email.place(x=150, y=20)

    tk.Label(add_window, text="Email Alias:").place(x=20, y=60)
    entry_alias = tk.Entry(add_window)
    entry_alias.place(x=150, y=60)

    tk.Label(add_window, text="Forwarding To:").place(x=20, y=100)
    entry_forwarding = tk.Entry(add_window)
    entry_forwarding.place(x=150, y=100)

    tk.Label(add_window, text="Provider:").place(x=20, y=140)
    entry_provider = tk.Entry(add_window)
    entry_provider.place(x=150, y=140)

    tk.Button(add_window, text="Save", command=save_alias).place(x=150, y=200)


def search_email():
    email_address = entry_search.get()
    conn = sqlite3.connect('email_aliases.db')
    cursor = conn.cursor()
    cursor.execute('''SELECT EmailAlias, ForwardingTo, Provider FROM EmailAliases WHERE EmailAddress = ?''',
                   (email_address,))
    result = cursor.fetchone()
    conn.close()

    if result:
        entry_alias_display.delete(0, tk.END)
        entry_forwarding_display.delete(0, tk.END)
        entry_provider_display.delete(0, tk.END)
        entry_alias_display.insert(0, result[0])
        entry_forwarding_display.insert(0, result[1])
        entry_provider_display.insert(0, result[2])
    else:
        messagebox.showinfo("Not Found", "No record found for this email address.")


def populate_alias_dropdown():
    conn = sqlite3.connect('email_aliases.db')
    cursor = conn.cursor()
    cursor.execute('''SELECT DISTINCT EmailAlias FROM EmailAliases''')
    aliases = [row[0] for row in cursor.fetchall()]
    conn.close()
    alias_dropdown['values'] = aliases


def show_alias_addresses(event):
    selected_alias = alias_dropdown.get()
    conn = sqlite3.connect('email_aliases.db')
    cursor = conn.cursor()
    cursor.execute('''SELECT EmailAddress FROM EmailAliases WHERE EmailAlias = ?''', (selected_alias,))
    addresses = cursor.fetchall()
    conn.close()

    listbox_addresses.delete(0, tk.END)
    for address in addresses:
        listbox_addresses.insert(tk.END, address[0])


def populate_provider_dropdown():
    conn = sqlite3.connect('email_aliases.db')
    cursor = conn.cursor()
    cursor.execute('''SELECT DISTINCT Provider FROM EmailAliases''')
    providers = [row[0] for row in cursor.fetchall()]
    conn.close()
    provider_dropdown['values'] = providers


def show_provider_info(event):
    selected_provider = provider_dropdown.get()
    conn = sqlite3.connect('email_aliases.db')
    cursor = conn.cursor()
    cursor.execute('''SELECT EmailAlias, ForwardingTo FROM EmailAliases WHERE Provider = ?''', (selected_provider,))
    records = cursor.fetchall()
    conn.close()

    for row in tree.get_children():
        tree.delete(row)

    for record in records:
        tree.insert('', tk.END, values=record)


# Initialize database
init_db()

# Create main window
root = tk.Tk()
root.title("Email Alias Manager")
root.geometry("600x500")

# Add alias button
tk.Button(root, text="Add Email Alias", command=add_alias).place(x=20, y=20)

# Search box
tk.Label(root, text="Search by Email Address:").place(x=20, y=70)
entry_search = tk.Entry(root)
entry_search.place(x=200, y=70)
tk.Button(root, text="Search", command=search_email).place(x=400, y=70)

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

# Alias dropdown
tk.Label(root, text="Select Alias:").place(x=20, y=240)
alias_dropdown = ttk.Combobox(root)
alias_dropdown.place(x=150, y=240)
alias_dropdown.bind("<<ComboboxSelected>>", show_alias_addresses)
populate_alias_dropdown()

listbox_addresses = tk.Listbox(root)
listbox_addresses.place(x=20, y=280, width=200, height=100)

# Provider dropdown
tk.Label(root, text="Select Provider:").place(x=300, y=240)
provider_dropdown = ttk.Combobox(root)
provider_dropdown.place(x=450, y=240)
provider_dropdown.bind("<<ComboboxSelected>>", show_provider_info)
populate_provider_dropdown()

# Treeview for provider information
tree = ttk.Treeview(root, columns=("Alias", "ForwardingTo"), show="headings")
tree.heading("Alias", text="Alias")
tree.heading("ForwardingTo", text="Forwarding To")
tree.place(x=300, y=280, width=280, height=200)

# Run the application
root.mainloop()
