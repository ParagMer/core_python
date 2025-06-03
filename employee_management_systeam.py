#pip install mysql-connector-python

# import mysql.connector

# # Connect to MySQL Server (no database yet)
# conn = mysql.connector.connect(
#     host="localhost",
#     user="root",
#     password="yourpassword"  # <-- replace with your MySQL password
# )
# cursor = conn.cursor()

# # 1. Create Database if not exists
# cursor.execute("CREATE DATABASE IF NOT EXISTS employee_db")
# cursor.execute("USE employee_db")

# # 2. Create employees table
# cursor.execute("""
# CREATE TABLE IF NOT EXISTS employees (
#     emp_id INT PRIMARY KEY AUTO_INCREMENT,
#     name VARCHAR(100),
#     department VARCHAR(50),
#     email VARCHAR(100),
#     phone VARCHAR(15)
# )
# """)

# # 3. Create attendance table
# cursor.execute("""
# CREATE TABLE IF NOT EXISTS attendance (
#     id INT PRIMARY KEY AUTO_INCREMENT,
#     emp_id INT,
#     date DATE,
#     status ENUM('Present', 'Absent'),
#     FOREIGN KEY (emp_id) REFERENCES employees(emp_id)
# )
# """)

# print("✅ Database and tables created successfully.")

# # Cleanup
# cursor.close()
# conn.close()

import mysql.connector
from datetime import date

# === Database Connection ===
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="yourpassword",   # <-- change this
    database="employee_db"
)
cursor = conn.cursor()

# === Add New Employee ===
def add_employee(name, dept, email, phone):
    query = "INSERT INTO employees (name, department, email, phone) VALUES (%s, %s, %s, %s)"
    cursor.execute(query, (name, dept, email, phone))
    conn.commit()
    print("✅ Employee added successfully.")

# === Update Employee ===
def update_employee(emp_id, name=None, dept=None, email=None, phone=None):
    updates = []
    values = []
    if name:
        updates.append("name=%s")
        values.append(name)
    if dept:
        updates.append("department=%s")
        values.append(dept)
    if email:
        updates.append("email=%s")
        values.append(email)
    if phone:
        updates.append("phone=%s")
        values.append(phone)

    values.append(emp_id)
    query = f"UPDATE employees SET {', '.join(updates)} WHERE emp_id=%s"
    cursor.execute(query, values)
    conn.commit()
    print("✅ Employee updated successfully.")

# === Delete Employee ===
def delete_employee(emp_id):
    cursor.execute("DELETE FROM attendance WHERE emp_id=%s", (emp_id,))
    cursor.execute("DELETE FROM employees WHERE emp_id=%s", (emp_id,))
    conn.commit()
    print("🗑️ Employee deleted successfully.")

# === Search Employees ===
def search_employees(keyword):
    query = "SELECT * FROM employees WHERE name LIKE %s OR department LIKE %s"
    cursor.execute(query, (f"%{keyword}%", f"%{keyword}%"))
    results = cursor.fetchall()
    for emp in results:
        print(emp)

# === Mark Attendance ===
def mark_attendance(emp_id, status='Present'):
    query = "INSERT INTO attendance (emp_id, date, status) VALUES (%s, %s, %s)"
    cursor.execute(query, (emp_id, date.today(), status))
    conn.commit()
    print("🕒 Attendance marked.")

# === Generate Monthly Report ===
def generate_monthly_report(month, year):
    query = """
    SELECT e.emp_id, e.name, COUNT(a.status) AS present_days
    FROM employees e
    JOIN attendance a ON e.emp_id = a.emp_id
    WHERE a.status = 'Present' AND MONTH(a.date) = %s AND YEAR(a.date) = %s
    GROUP BY e.emp_id;
    """
    cursor.execute(query, (month, year))
    results = cursor.fetchall()
    print(f"\n📊 Attendance Report for {month}/{year}")
    print("Emp ID | Name           | Present Days")
    print("----------------------------------------")
    for row in results:
        print(f"{row[0]:<7} | {row[1]:<14} | {row[2]}")

# === Example Usage ===
if __name__ == "__main__":
    # Add sample employee
    add_employee("John Doe", "HR", "john@example.com", "1234567890")

    # Update employee
    update_employee(1, phone="9876543210")

    # Mark attendance
    mark_attendance(1, "Present")

    # Search employee
    search_employees("HR")

    # Generate attendance report
    generate_monthly_report(6, 2025)

    # Delete employee (uncomment to test)
    # delete_employee(1)

    # Close connection
    cursor.close()
    conn.close()
