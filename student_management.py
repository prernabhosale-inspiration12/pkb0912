
import mysql.connector

# Connect to MySQL
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="student_db"
)
# Create a cursor object to execute SQL queries
cursor = conn.cursor()
# Step 2: Functions for each operation
def add_student():
    name = input("Enter name: ")
    roll_no = input("Enter roll number: ")
    department = input("Enter department: ")

    cursor.execute(
        "INSERT INTO students (name, roll_no, department) VALUES (%s, %s, %s)",
        (name, roll_no, department)
    )
    conn.commit()
    print("✅ Student added successfully!\n")

def view_students():
    cursor.execute("SELECT * FROM students")
    records = cursor.fetchall()
    print("\n--- Student List ---")
    for row in records:
        print(f"ID: {row[0]}, Name: {row[1]}, Roll No: {row[2]}, Department: {row[3]}")
    print()

def update_student():
    sid = input("Enter student ID to update: ")
    name = input("Enter new name: ")
    dept = input("Enter new department: ")
    cursor.execute(
        "UPDATE students SET name=%s, department=%s WHERE student_id=%s",
        (name, dept, sid)
    )
    conn.commit()
    print("✅ Record updated successfully!\n")

def delete_student():
    sid = input("Enter student ID to delete: ")
    cursor.execute("DELETE FROM students WHERE student_id=%s", (sid,))
    conn.commit()
    print("🗑️ Student deleted successfully!\n")

def add_marks():
    sid = input("Enter student ID: ")
    cid = input("Enter course ID: ")
    marks = input("Enter marks obtained: ")
    cursor.execute(
        "INSERT INTO marks (student_id, course_id, marks_obtained) VALUES (%s, %s, %s)",
        (sid, cid, marks)
    )
    conn.commit()
    print("✅ Marks added successfully!\n")

def view_marks():
    cursor.execute(
        "SELECT s.name, c.course_name, m.marks_obtained "
        "FROM marks m "
        "JOIN students s ON m.student_id = s.student_id "
        "JOIN courses c ON m.course_id = c.course_id"
    )
    records = cursor.fetchall()
    print("\n--- Marks Report ---")
    for row in records:
        print(f"Student: {row[0]}, Course: {row[1]}, Marks: {row[2]}")
    print()

def add_attendance():
    sid = input("Enter student ID: ")
    total = int(input("Enter total classes: "))
    attended = int(input("Enter attended classes: "))
    cursor.execute(
        "INSERT INTO attendance (student_id, total_classes, attended) VALUES (%s, %s, %s)",
        (sid, total, attended)
    )
    conn.commit()
    print("✅ Attendance added successfully!\n")

def view_attendance():
    cursor.execute(
        "SELECT s.name, a.total_classes, a.attended "
        "FROM attendance a "
        "JOIN students s ON a.student_id = s.student_id"
    )
    records = cursor.fetchall()
    print("\n--- Attendance Report ---")
    for row in records:
        percent = (row[2] / row[1]) * 100 if row[1] > 0 else 0
        print(f"Student: {row[0]}, Attendance: {percent:.2f}%")
    print()
 # Step 3: Menu-driven program
while True:
    print("""
===== Student Management System =====
1. Add Student
2. View Students
3. Update Student
4. Delete Student
5. Add Marks
6. View Marks
7. Add Attendance
8. View Attendance
9. Exit
""")
    
    choice = input("Enter your choice: ")

    if choice == '1':
        add_student()
    elif choice == '2':
        view_students()
    elif choice == '3':
        update_student()
    elif choice == '4':
        delete_student()
    elif choice == '5':
        add_marks()
    elif choice == '6':
        view_marks()
    elif choice == '7':
        add_attendance()
    elif choice == '8':
        view_attendance()
    elif choice == '9':
        print("👋 Exiting...")
        break
    else:
        print("❌ Invalid choice! Try again.")
