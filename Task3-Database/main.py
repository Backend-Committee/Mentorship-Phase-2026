import sqlite3
from datetime import date

conn = sqlite3.connect('school_management.db')
cursor = conn.cursor()

def create_tables():
    # Students
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS students (
        student_id INTEGER PRIMARY KEY AUTOINCREMENT,
        first_name TEXT NOT NULL,
        last_name TEXT NOT NULL,
        date_of_birth DATE NOT NULL,
        gender TEXT CHECK(gender IN ('Male', 'Female')) NOT NULL,
        email TEXT UNIQUE NOT NULL,
        phone TEXT
    )
    ''')

    # Teachers
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS teachers (
        teacher_id INTEGER PRIMARY KEY AUTOINCREMENT,
        first_name TEXT NOT NULL,
        last_name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        phone TEXT,
        hire_date DATE
    )
    ''')

    # Subjects
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS subjects (
        subject_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL UNIQUE,
        credits INTEGER DEFAULT 1
    )
    ''')

    # Classes
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS classes (
        class_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,              -- e.g. "3rd Secondary - Science"
        grade_level TEXT,                -- e.g. "Grade 10", "Thanaweya 3"
        academic_year TEXT NOT NULL      -- e.g. "2025-2026"
    )
    ''')

    # Class_Subjects (many-to-many between classes & subjects)
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS class_subjects (
        class_subject_id INTEGER PRIMARY KEY AUTOINCREMENT,
        class_id INTEGER NOT NULL,
        subject_id INTEGER NOT NULL,
        UNIQUE(class_id, subject_id),
        FOREIGN KEY (class_id) REFERENCES classes(class_id) ON DELETE CASCADE,
        FOREIGN KEY (subject_id) REFERENCES subjects(subject_id) ON DELETE RESTRICT
    )
    ''')

    # Enrollments
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS enrollments (
        enrollment_id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id INTEGER NOT NULL,
        class_subject_id INTEGER NOT NULL,
        enrolled_on DATE DEFAULT CURRENT_DATE,
        status TEXT DEFAULT 'Active' CHECK(status IN ('Active', 'Dropped', 'Completed')),
        final_grade TEXT,   -- e.g. "A", "85", NULL while ongoing
        FOREIGN KEY (student_id) REFERENCES students(student_id) ON DELETE CASCADE,
        FOREIGN KEY (class_subject_id) REFERENCES class_subjects(class_subject_id) ON DELETE CASCADE,
        UNIQUE(student_id, class_subject_id)
    )
    ''')

    # Teacher Assignments
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS teacher_assignments (
        assignment_id INTEGER PRIMARY KEY AUTOINCREMENT,
        teacher_id INTEGER NOT NULL,
        class_subject_id INTEGER NOT NULL,
        role TEXT DEFAULT 'Main Teacher',
        assigned_on DATE DEFAULT CURRENT_DATE,
        FOREIGN KEY (teacher_id) REFERENCES teachers(teacher_id) ON DELETE RESTRICT,
        FOREIGN KEY (class_subject_id) REFERENCES class_subjects(class_subject_id) ON DELETE CASCADE,
        UNIQUE(teacher_id, class_subject_id)
    )
    ''')

    conn.commit()
    print("Tables created successfully!")


def insert_sample_data():
    # Clear for fresh start
    cursor.execute('DELETE FROM enrollments')
    cursor.execute('DELETE FROM teacher_assignments')
    cursor.execute('DELETE FROM class_subjects')
    cursor.execute('DELETE FROM students')
    cursor.execute('DELETE FROM teachers')
    cursor.execute('DELETE FROM subjects')
    cursor.execute('DELETE FROM classes')
    conn.commit()

    # Students
    add_student('Maryam', 'Hassan', '2008-05-15', 'Female', 'maryam.h@school.com', '01001234567')
    add_student('Rawan', 'Mohamed', '2007-11-22', 'Female', 'rawan.m@school.com', '01234567890')

    # Teachers
    add_teacher('Mr.', 'Khalid', 'khalid@school.com', '01111111111', '2020-09-01')
    add_teacher('Ms.', 'Nour', 'nour@school.com', '01099999999', '2022-03-15')

    # Subjects
    add_subject('Mathematics', 4)
    add_subject('Physics', 3)
    add_subject('Arabic', 2)

    # Classes
    add_class('6-A', 'Grade 6', '2025-2026')
    cursor.execute("SELECT class_id FROM classes WHERE name = '6-A'")
    class_id = cursor.fetchone()[0]

    # add the math to class 6-A
    cursor.execute("SELECT subject_id FROM subjects WHERE name = 'Mathematics'")
    math_id = cursor.fetchone()[0]
    add_class_subject(class_id, math_id)


    # Enrollments
    cursor.execute("SELECT student_id FROM students WHERE email = 'maryam.h@school.com'")
    maryam_id = cursor.fetchone()[0]
    enroll_student(maryam_id, class_id, math_id)

    cursor.execute("SELECT student_id FROM students WHERE email = 'rawan.m@school.com'")
    rawan_id = cursor.fetchone()[0]
    enroll_student(rawan_id, class_id, math_id)

    # Assignments
    cursor.execute("SELECT teacher_id FROM teachers WHERE email = 'khalid@school.com'")
    khalid_id = cursor.fetchone()[0]
    assign_teacher(khalid_id, class_id, math_id)

    print("Sample data inserted! Now views should work.")

#crud for students
def add_student(first_name, last_name, date_of_birth, gender, email, phone=None):
    try:
        cursor.execute('''
        INSERT INTO students (first_name, last_name, date_of_birth, gender, email, phone)
        VALUES (?, ?, ?, ?, ?, ?)
        ''', (first_name, last_name, date_of_birth, gender, email, phone))
        conn.commit()
        print(f"Student {first_name} {last_name} added.")
    except sqlite3.IntegrityError as e:print(f"Error adding student: {e}")

def view_all_students():
    cursor.execute('SELECT * FROM students')
    students = cursor.fetchall()
    if not students:
        print("No students yet.")
    for student in students:
        print(student)
        
def update_student_email(student_id, new_email):
    cursor.execute('UPDATE students SET email = ? WHERE student_id = ?', (new_email, student_id))
    conn.commit()
    if cursor.rowcount == 0:
        print("No student with that ID.")
    else:
        print("Email updated.")
            
def delete_student(student_id):
    cursor.execute('DELETE FROM students WHERE student_id = ?', (student_id,))
    conn.commit()
    if cursor.rowcount == 0:
        print("No student with that ID.")
    else:
        print("Student deleted.")
            
            
            
# crud for Teachers
def add_teacher(first_name, last_name, email, phone=None, hire_date=date.today()):
    try:
        cursor.execute('''
        INSERT INTO teachers (first_name, last_name, email, phone, hire_date)
        VALUES (?, ?, ?, ?, ?)
        ''', (first_name, last_name, email, phone, hire_date))
        conn.commit()
        print(f"Teacher {first_name} {last_name} added.")
    except sqlite3.IntegrityError:
        print("Email duplicate.")

def view_all_teachers():
    cursor.execute('SELECT * FROM teachers')
    teachers = cursor.fetchall()
    if not teachers:
        print("No teachers yet.")
    for teacher in teachers:
        print(teacher)

def update_teacher_phone(teacher_id, new_phone):
    cursor.execute('UPDATE teachers SET phone = ? WHERE teacher_id = ?', (new_phone, teacher_id))
    conn.commit()
    print("Phone updated." if cursor.rowcount > 0 else "No teacher with that ID.")

def delete_teacher(teacher_id):
    cursor.execute('DELETE FROM teachers WHERE teacher_id = ?', (teacher_id,))
    conn.commit()
    print("Teacher deleted." if cursor.rowcount > 0 else "No teacher with that ID.")

# ─── CRUD for Subjects ───
def add_subject(name, credits=1):
    try:
        cursor.execute('INSERT INTO subjects (name, credits) VALUES (?, ?)', (name, credits))
        conn.commit()
        print(f"Subject {name} added.")
    except sqlite3.IntegrityError:
        print("Subject name duplicate.")

def view_all_subjects():
    cursor.execute('SELECT * FROM subjects')
    subjects = cursor.fetchall()
    if not subjects:
        print("No subjects yet.")
    for subj in subjects:
        print(subj)

def update_subject_credits(subject_id, new_credits):
    cursor.execute('UPDATE subjects SET credits = ? WHERE subject_id = ?', (new_credits, subject_id))
    conn.commit()
    print("Credits updated." if cursor.rowcount > 0 else "No subject with that ID.")

def delete_subject(subject_id):
    cursor.execute('DELETE FROM subjects WHERE subject_id = ?', (subject_id,))
    conn.commit()
    print("Subject deleted." if cursor.rowcount > 0 else "No subject with that ID.")

# ─── CRUD for Classes ───
def add_class(name, grade_level, academic_year):
    cursor.execute('INSERT INTO classes (name, grade_level, academic_year) VALUES (?, ?, ?)', (name, grade_level, academic_year))
    conn.commit()
    print(f"Class {name} added.")

def view_all_classes():
    cursor.execute('SELECT * FROM classes')
    classes = cursor.fetchall()
    if not classes:
        print("No classes yet.")
    for cls in classes:
        print(cls)

def update_class_name(class_id, new_name):
    cursor.execute('UPDATE classes SET name = ? WHERE class_id = ?', (new_name, class_id))
    conn.commit()
    print("Name updated." if cursor.rowcount > 0 else "No class with that ID.")

def delete_class(class_id):
    cursor.execute('DELETE FROM classes WHERE class_id = ?', (class_id,))
    conn.commit()
    print("Class deleted." if cursor.rowcount > 0 else "No class with that ID.")

# ─── Add Class-Subject Link ───
def add_class_subject(class_id, subject_id):
    try:
        cursor.execute('INSERT INTO class_subjects (class_id, subject_id) VALUES (?, ?)', (class_id, subject_id))
        conn.commit()
        print("Class-Subject linked.")
    except sqlite3.IntegrityError:
        print("Already linked or invalid IDs.")

# ─── Enroll Student ───
def enroll_student(student_id, class_id, subject_id, status='Active'):
    try:
        cursor.execute('SELECT class_subject_id FROM class_subjects WHERE class_id = ? AND subject_id = ?', (class_id, subject_id))
        cs_id = cursor.fetchone()
        if not cs_id:
            print("No such class-subject combo. Add it first.")
            return
        cs_id = cs_id[0]
        cursor.execute('''
        INSERT INTO enrollments (student_id, class_subject_id, status)
        VALUES (?, ?, ?)
        ''', (student_id, cs_id, status))
        conn.commit()
        print("Student enrolled.")
    except sqlite3.IntegrityError:
        print("Student already enrolled or invalid IDs.")

# ─── Update Enrollment Grade ───
def update_enrollment_grade(enrollment_id, new_grade):
    cursor.execute('UPDATE enrollments SET final_grade = ? WHERE enrollment_id = ?', (new_grade, enrollment_id))
    conn.commit()
    print("Grade updated." if cursor.rowcount > 0 else "No enrollment with that ID.")

# ─── Delete Enrollment ───
def delete_enrollment(enrollment_id):
    cursor.execute('DELETE FROM enrollments WHERE enrollment_id = ?', (enrollment_id,))
    conn.commit()
    print("Enrollment deleted." if cursor.rowcount > 0 else "No enrollment with that ID.")

# ─── Assign Teacher ───
def assign_teacher(teacher_id, class_id, subject_id, role='Main Teacher'):
    try:
        cursor.execute('SELECT class_subject_id FROM class_subjects WHERE class_id = ? AND subject_id = ?', (class_id, subject_id))
        cs_id = cursor.fetchone()
        if not cs_id:
            print("No such class-subject. Add it first.")
            return
        cs_id = cs_id[0]
        cursor.execute('''
        INSERT INTO teacher_assignments (teacher_id, class_subject_id, role)
        VALUES (?, ?, ?)
        ''', (teacher_id, cs_id, role))
        conn.commit()
        print("Teacher assigned.")
    except sqlite3.IntegrityError:
        print("Already assigned or invalid IDs.")

# View Students Enrollments
def view_students_enrollments():
    cursor.execute('''
    SELECT 
        s.first_name || ' ' || s.last_name AS student_name,
        c.name AS class_name,
        subj.name AS subject,
        e.final_grade,
        e.status
    FROM students s
    LEFT JOIN enrollments e ON s.student_id = e.student_id
    LEFT JOIN class_subjects cs ON e.class_subject_id = cs.class_subject_id
    LEFT JOIN classes c ON cs.class_id = c.class_id
    LEFT JOIN subjects subj ON cs.subject_id = subj.subject_id
    ORDER BY s.last_name
    ''')
    rows = cursor.fetchall()
    if not rows:
        print("No enrollments yet.")
    for row in rows:
        print(row)
        

def main_menu():
    create_tables()
    # insert_sample_data()  # Uncomment to run once

    while True:
        print("\n=== School Management System ===")
        print("1. Add")
        print("1. Add Student")
        print("2. View All Students")
        print("3. Update Student Email")
        print("4. Delete Student")
        print("5. Add Teacher")
        print("6. View All Teachers")
        print("7. Update Teacher Phone")
        print("8. Delete Teacher")
        print("9. Add Subject")
        print("10. View All Subjects")
        print("11. Update Subject Credits")
        print("12. Delete Subject")
        print("13. Add Class")
        print("14. View All Classes")
        print("15. Update Class Name")
        print("16. Delete Class")
        print("17. Link Class to Subject")
        print("18. Enroll Student in Class-Subject")
        print("19. View Students Enrollments")
        print("20. Update Enrollment Grade")
        print("21. Delete Enrollment")
        print("22. Assign Teacher to Class-Subject")
        print("23. Insert Sample Data (run once)")
        print("24. Exit")

        choice = input("Enter choice: ")

        if choice == '1':
            fn = input("First name: ")
            ln = input("Last name: ")
            dob = input("DOB (YYYY-MM-DD): ")
            gender = input("Gender (Male/Female): ")
            email = input("Email: ")
            phone = input("Phone (optional): ") or None
            add_student(fn, ln, dob, gender, email, phone)
        elif choice == '2':
            view_all_students()
        elif choice == '3':
            sid = int(input("Student ID: "))
            new_email = input("New email: ")
            update_student_email(sid, new_email)
        elif choice == '4':
            sid = int(input("Student ID: "))
            delete_student(sid)
        elif choice == '5':
            fn = input("First name: ")
            ln = input("Last name: ")
            email = input("Email: ")
            phone = input("Phone (optional): ") or None
            hire_date = input("Hire date (YYYY-MM-DD, optional - default today): ") or date.today()
            add_teacher(fn, ln, email, phone, hire_date)
        elif choice == '6':
            view_all_teachers()
        elif choice == '7':
            tid = int(input("Teacher ID: "))
            new_phone = input("New phone: ")
            update_teacher_phone(tid, new_phone)
        elif choice == '8':
            tid = int(input("Teacher ID: "))
            delete_teacher(tid)
        elif choice == '9':
            name = input("Subject name: ")
            credits = int(input("Credits (default 1): ") or 1)
            add_subject(name, credits)
        elif choice == '10':
            view_all_subjects()
        elif choice == '11':
            sid = int(input("Subject ID: "))
            new_credits = int(input("New credits: "))
            update_subject_credits(sid, new_credits)
        elif choice == '12':
            sid = int(input("Subject ID: "))
            delete_subject(sid)
        elif choice == '13':
            name = input("Class name: ")
            grade = input("Grade level: ")
            year = input("Academic year: ")
            add_class(name, grade, year)
        elif choice == '14':
            view_all_classes()
        elif choice == '15':
            cid = int(input("Class ID: "))
            new_name = input("New name: ")
            update_class_name(cid, new_name)
        elif choice == '16':
            cid = int(input("Class ID: "))
            delete_class(cid)
        elif choice == '17':
            cid = int(input("Class ID: "))
            sid = int(input("Subject ID: "))
            add_class_subject(cid, sid)
        elif choice == '18':
            sid = int(input("Student ID: "))
            cid = int(input("Class ID: "))
            subid = int(input("Subject ID: "))
            status = input("Status (default Active): ") or 'Active'
            enroll_student(sid, cid, subid, status)
        elif choice == '19':
            view_students_enrollments()
        elif choice == '20':
            eid = int(input("Enrollment ID: "))
            grade = input("New grade: ")
            update_enrollment_grade(eid, grade)
        elif choice == '21':
            eid = int(input("Enrollment ID: "))
            delete_enrollment(eid)
        elif choice == '22':
            tid = int(input("Teacher ID: "))
            cid = int(input("Class ID: "))
            sid = int(input("Subject ID: "))
            role = input("Role (default Main Teacher): ") or 'Main Teacher'
            assign_teacher(tid, cid, sid, role)
        elif choice == '23':
            insert_sample_data()
        elif choice == '24':
            print("Bye...")
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main_menu()

conn.close()