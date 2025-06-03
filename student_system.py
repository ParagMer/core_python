import psycopg2
from datetime import date

#pip install psycopg2-binary
# === Connect to PostgreSQL ===
conn = psycopg2.connect(
    dbname="student_db",
    user="postgres",
    password="yourpassword",  # <-- change this
    host="localhost",
    port="5432"
)
cursor = conn.cursor()

# === Add Student ===
def add_student(name, class_name, email):
    cursor.execute("""
        INSERT INTO students (name, class, email)
        VALUES (%s, %s, %s)
    """, (name, class_name, email))
    conn.commit()
    print("✅ Student added.")

# === Add Subject ===
def add_subject(subject_name):
    cursor.execute("""
        INSERT INTO subjects (subject_name)
        VALUES (%s)
    """, (subject_name,))
    conn.commit()
    print("📘 Subject added.")

# === Mark Attendance ===
def mark_attendance(student_id, subject_id, status):
    today = date.today()
    cursor.execute("""
        INSERT INTO attendance (student_id, subject_id, date, status)
        VALUES (%s, %s, %s, %s)
    """, (student_id, subject_id, today, status))
    conn.commit()
    print("🕒 Attendance marked.")

# === Add Marks ===
def add_marks(student_id, subject_id, exam_name, score):
    cursor.execute("""
        INSERT INTO marks (student_id, subject_id, exam_name, score)
        VALUES (%s, %s, %s, %s)
    """, (student_id, subject_id, exam_name, score))
    conn.commit()
    print("📝 Marks added.")

# === View Student Performance ===
def view_performance():
    cursor.execute("""
        SELECT s.name, sub.subject_name, AVG(m.score)
        FROM marks m
        JOIN students s ON m.student_id = s.student_id
        JOIN subjects sub ON m.subject_id = sub.subject_id
        GROUP BY s.name, sub.subject_name
        ORDER BY s.name;
    """)
    for row in cursor.fetchall():
        print(f"👩‍🎓 {row[0]} | 📘 {row[1]} | Avg Score: {row[2]:.2f}")

# === View Attendance Summary ===
def view_attendance():
    cursor.execute("""
        SELECT s.name, sub.subject_name, COUNT(*) FILTER (WHERE a.status = 'Present') AS present_days
        FROM attendance a
        JOIN students s ON a.student_id = s.student_id
        JOIN subjects sub ON a.subject_id = sub.subject_id
        GROUP BY s.name, sub.subject_name;
    """)
    for row in cursor.fetchall():
        print(f"👩‍🎓 {row[0]} | 📘 {row[1]} | Present: {row[2]} days")

# === Sample Usage ===
if __name__ == "__main__":
    # Add students
    add_student("Alice", "10A", "alice@example.com")
    add_student("Bob", "10A", "bob@example.com")

    # Add subjects
    add_subject("Math")
    add_subject("Science")

    # Add attendance
    mark_attendance(1, 1, "Present")  # Alice, Math
    mark_attendance(2, 2, "Absent")   # Bob, Science

    # Add marks
    add_marks(1, 1, "Midterm", 85)
    add_marks(1, 2, "Midterm", 78)
    add_marks(2, 1, "Midterm", 90)

    # View performance
    print("\n📊 Performance Summary:")
    view_performance()

    # View attendance
    print("\n🗓️ Attendance Summary:")
    view_attendance()

    # Close connection
    cursor.close()
    conn.close()
