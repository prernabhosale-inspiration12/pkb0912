import tkinter as tk
from tkinter import messagebox, ttk
import mysql.connector

# ===== MySQL Connection =====
import mysql.connector

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",  # <- put your MySQL password here
    database="student_db"
)

cursor = conn.cursor()


# ===== Functions =====
def add_student():
    name = name_entry.get()
    roll = roll_entry.get()
    dept = dept_entry.get()
    if not name or not roll or not dept:
        messagebox.showerror("Error", "All fields are required!")
        return
    cursor.execute(
        "INSERT INTO students (name, roll_no, department) VALUES (%s, %s, %s)",
        (name, roll, dept)
    )
    conn.commit()
    messagebox.showinfo("Success", "Student added successfully!")
    name_entry.delete(0, tk.END)
    roll_entry.delete(0, tk.END)
    dept_entry.delete(0, tk.END)
    view_students()

def view_students():
    for row in tree.get_children():
        tree.delete(row)
    cursor.execute("SELECT * FROM students")
    records = cursor.fetchall()
    for r in records:
        tree.insert("", tk.END, values=r)

def delete_student():
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showerror("Error", "Select a student first")
        return
    sid = tree.item(selected_item)["values"][0]
    cursor.execute("DELETE FROM students WHERE student_id=%s", (sid,))
    conn.commit()
    messagebox.showinfo("Success", "Student deleted successfully!")
    view_students()

# ===== Tkinter GUI =====
root = tk.Tk()
root.title("Student Management System")

# Input fields
tk.Label(root, text="Name").grid(row=0, column=0, padx=5, pady=5)
tk.Label(root, text="Roll No").grid(row=1, column=0, padx=5, pady=5)
tk.Label(root, text="Department").grid(row=2, column=0, padx=5, pady=5)

name_entry = tk.Entry(root)
roll_entry = tk.Entry(root)
dept_entry = tk.Entry(root)

name_entry.grid(row=0, column=1, padx=5, pady=5)
roll_entry.grid(row=1, column=1, padx=5, pady=5)
dept_entry.grid(row=2, column=1, padx=5, pady=5)

# Buttons
tk.Button(root, text="Add Student", command=add_student).grid(row=3, column=0, pady=5)
tk.Button(root, text="Delete Student", command=delete_student).grid(row=3, column=1, pady=5)
tk.Button(root, text="View Students", command=view_students).grid(row=3, column=2, pady=5)

# Treeview for student list
columns = ("ID", "Name", "Roll No", "Department")
tree = ttk.Treeview(root, columns=columns, show="headings")
for col in columns:
    tree.heading(col, text=col)
tree.grid(row=4, column=0, columnspan=3, padx=5, pady=5)

view_students()  # Load initial data

root.mainloop()
