import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector

# ===== MySQL Connection =====
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",  # Change this if needed
    database="student_db"
)
cursor = conn.cursor()

# ====== Functions ======

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
    clear_student_fields()
    view_students()

def view_students():
    for row in student_tree.get_children():
        student_tree.delete(row)
    cursor.execute("SELECT * FROM students")
    for r in cursor.fetchall():
        student_tree.insert("", tk.END, values=r)

def update_student():
    selected = student_tree.selection()
    if not selected:
        messagebox.showerror("Error", "Select a student to update!")
        return
    sid = student_tree.item(selected)["values"][0]
    name = name_entry.get()
    dept = dept_entry.get()
    if not name or not dept:
        messagebox.showerror("Error", "Enter new name and department!")
        return
    cursor.execute(
        "UPDATE students SET name=%s, department=%s WHERE student_id=%s",
        (name, dept, sid)
    )
    conn.commit()
    messagebox.showinfo("Success", "Student updated successfully!")
    view_students()

def delete_student():
    selected = student_tree.selection()
    if not selected:
        messagebox.showerror("Error", "Select a student to delete!")
        return
    sid = student_tree.item(selected)["values"][0]
    cursor.execute("DELETE FROM students WHERE student_id=%s", (sid,))
    conn.commit()
    messagebox.showinfo("Success", "Student deleted successfully!")
    view_students()

def add_marks():
    sid = marks_student_id.get()
    cid = course_id.get()
    marks = marks_obtained.get()
    if not sid or not cid or not marks:
        messagebox.showerror("Error", "All fields are required!")
        return
    cursor.execute(
        "INSERT INTO marks (student_id, course_id, marks_obtained) VALUES (%s, %s, %s)",
        (sid, cid, marks)
    )
    conn.commit()
    messagebox.showinfo("Success", "Marks added successfully!")
    view_marks()

def view_marks():
    for row in marks_tree.get_children():
        marks_tree.delete(row)
    cursor.execute(
        "SELECT m.mark_id, s.name, m.course_id, m.marks_obtained "
        "FROM marks m "
        "JOIN students s ON m.student_id = s.student_id"
    )
    for r in cursor.fetchall():
        marks_tree.insert("", tk.END, values=(r[0], r[1], r[2], r[3]))

def add_attendance():
    sid = att_student_id.get()
    total = total_classes.get()
    attended = attended_classes.get()
    if not sid or not total or not attended:
        messagebox.showerror("Error", "All fields are required!")
        return
    cursor.execute(
        "INSERT INTO attendance (student_id, total_classes, attended) VALUES (%s, %s, %s)",
        (sid, total, attended)
    )
    conn.commit()
    messagebox.showinfo("Success", "Attendance added successfully!")
    view_attendance()

def view_attendance():
    for row in att_tree.get_children():
        att_tree.delete(row)
    cursor.execute(
        "SELECT s.name, a.total_classes, a.attended "
        "FROM attendance a "
        "JOIN students s ON a.student_id = s.student_id"
    )
    for r in cursor.fetchall():
        percent = (r[2] / r[1]) * 100 if r[1] > 0 else 0
        att_tree.insert("", tk.END, values=(r[0], r[1], r[2], f"{percent:.2f}%"))

def clear_student_fields():
    name_entry.delete(0, tk.END)
    roll_entry.delete(0, tk.END)
    dept_entry.delete(0, tk.END)

def exit_app():
    conn.close()
    root.destroy()

# ===== Tkinter GUI =====
root = tk.Tk()
root.title("Student Management System")
root.geometry("950x700")

notebook = ttk.Notebook(root)
notebook.pack(fill="both", expand=True)

# --- TAB 1: Student Management ---
student_tab = ttk.Frame(notebook)
notebook.add(student_tab, text="Students")

tk.Label(student_tab, text="Name").grid(row=0, column=0, padx=5, pady=5)
tk.Label(student_tab, text="Roll No").grid(row=1, column=0, padx=5, pady=5)
tk.Label(student_tab, text="Department").grid(row=2, column=0, padx=5, pady=5)

name_entry = tk.Entry(student_tab)
roll_entry = tk.Entry(student_tab)
dept_entry = tk.Entry(student_tab)
name_entry.grid(row=0, column=1, padx=5, pady=5)
roll_entry.grid(row=1, column=1, padx=5, pady=5)
dept_entry.grid(row=2, column=1, padx=5, pady=5)

tk.Button(student_tab, text="Add Student", command=add_student).grid(row=3, column=0, pady=5)
tk.Button(student_tab, text="Update Student", command=update_student).grid(row=3, column=1, pady=5)
tk.Button(student_tab, text="Delete Student", command=delete_student).grid(row=3, column=2, pady=5)
tk.Button(student_tab, text="View Students", command=view_students).grid(row=3, column=3, pady=5)

columns = ("ID", "Name", "Roll No", "Department")
student_tree = ttk.Treeview(student_tab, columns=columns, show="headings")
for col in columns:
    student_tree.heading(col, text=col)
student_tree.grid(row=4, column=0, columnspan=4, padx=5, pady=5)

# --- TAB 2: Marks ---
marks_tab = ttk.Frame(notebook)
notebook.add(marks_tab, text="Marks")

tk.Label(marks_tab, text="Student ID").grid(row=0, column=0, padx=5, pady=5)
tk.Label(marks_tab, text="Course ID").grid(row=1, column=0, padx=5, pady=5)
tk.Label(marks_tab, text="Marks Obtained").grid(row=2, column=0, padx=5, pady=5)

marks_student_id = tk.Entry(marks_tab)
course_id = tk.Entry(marks_tab)
marks_obtained = tk.Entry(marks_tab)
marks_student_id.grid(row=0, column=1, padx=5, pady=5)
course_id.grid(row=1, column=1, padx=5, pady=5)
marks_obtained.grid(row=2, column=1, padx=5, pady=5)

tk.Button(marks_tab, text="Add Marks", command=add_marks).grid(row=3, column=0, pady=5)
tk.Button(marks_tab, text="View Marks", command=view_marks).grid(row=3, column=1, pady=5)

marks_tree = ttk.Treeview(marks_tab, columns=("ID", "Name", "Course ID", "Marks"), show="headings")
for col in ("ID", "Name", "Course ID", "Marks"):
    marks_tree.heading(col, text=col)
marks_tree.grid(row=4, column=0, columnspan=3, padx=5, pady=5)

# --- TAB 3: Attendance ---
attendance_tab = ttk.Frame(notebook)
notebook.add(attendance_tab, text="Attendance")

tk.Label(attendance_tab, text="Student ID").grid(row=0, column=0, padx=5, pady=5)
tk.Label(attendance_tab, text="Total Classes").grid(row=1, column=0, padx=5, pady=5)
tk.Label(attendance_tab, text="Attended").grid(row=2, column=0, padx=5, pady=5)

att_student_id = tk.Entry(attendance_tab)
total_classes = tk.Entry(attendance_tab)
attended_classes = tk.Entry(attendance_tab)
att_student_id.grid(row=0, column=1, padx=5, pady=5)
total_classes.grid(row=1, column=1, padx=5, pady=5)
attended_classes.grid(row=2, column=1, padx=5, pady=5)

tk.Button(attendance_tab, text="Add Attendance", command=add_attendance).grid(row=3, column=0, pady=5)
tk.Button(attendance_tab, text="View Attendance", command=view_attendance).grid(row=3, column=1, pady=5)

att_tree = ttk.Treeview(attendance_tab, columns=("Name", "Total", "Attended", "Percent"), show="headings")
for col in ("Name", "Total", "Attended", "Percent"):
    att_tree.heading(col, text=col)
att_tree.grid(row=4, column=0, columnspan=3, padx=5, pady=5)

# --- Exit Button ---
tk.Button(root, text="Exit", command=exit_app, bg="red", fg="white").pack(pady=10)

view_students()  # Load initial data
root.mainloop()
