import sqlite3

con = sqlite3.connect("school_db.db")
cur = con.cursor()
cur.execute("pragma foreign_keys = on")
def db_creation():
    cur.execute("""
        CREATE TABLE IF NOT EXISTS students (
            student_id INTEGER  PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            grade INTEGER NOT NULL,
            DOB  TEXT NOT NULL
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS teachers (
            teacher_id INTEGER  PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            DOB  TEXT NOT NULL
        )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS subjects (
        subject_id INTEGER  PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        credit_hours INTEGER NOT NULL
        )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS classes (
        class_id INTEGER  PRIMARY KEY AUTOINCREMENT,
        teacher_id INTEGER,
        subject_id INTEGER,
        hall_num INTEGER,
        date TEXT,
        time TEXT,
        FOREIGN KEY(teacher_id) REFERENCES teachers(teacher_id),
        FOREIGN KEY(subject_id) REFERENCES subjects(subject_id)
        )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS enrollments(
        student_id INTEGER,
        subject_id INTEGER,
        PRIMARY KEY (student_id, subject_id),
        FOREIGN KEY(student_id) REFERENCES students(student_id),
        FOREIGN KEY(subject_id) REFERENCES subjects(subject_id)
        )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS studentClasses (
        student_id INTEGER,
        class_id INTEGER,
        PRIMARY KEY(student_id, class_id),
        FOREIGN KEY(student_id) REFERENCES students(student_id),
        FOREIGN KEY(class_id) REFERENCES classes(class_id)
        )
    """)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS teacherSubjects (
        teacher_id INTEGER,
        subject_id INTEGER,
        PRIMARY KEY(teacher_id, subject_id),
        FOREIGN KEY(teacher_id) REFERENCES teachers(teacher_id),
        FOREIGN KEY(subject_id) REFERENCES subjects(subject_id)
        )
    """)
    con.commit()
    print ("DB has been created successfully!")


def insert_student():
    try:
        print("\nAdding new student\n")
        name = input("Enter Student Name: ")
        grade = int(input("Enter Student Grade: "))
        DOB = input("Enter Student DOB: ")
        cur.execute("INSERT INTO students (name, grade, DOB) VALUES (?, ?, ?)", (name, grade, DOB))
        con.commit()
        print("Student has been added!")
    except ValueError:
        print("Student grade must be an integer!")


def insert_subject():
    print()
    name = input("Enter Subject Name: ")
    try:
        hours = int(input("Enter Credit Hours: "))
        cur.execute("INSERT INTO subjects (name, credit_hours) VALUES (?, ?)", (name, hours))
        con.commit()
        print("Subject added!")
    except ValueError:
        print("Credit Hours must be an integer!")

def insert_teacher():
    print()
    name = input("Enter Teacher Name: ")
    DOB = input("Enter Teacher DOB: ")
    cur.execute("INSERT INTO teachers (name, DOB) VALUES (?, ?)", (name, DOB))
    con.commit()
    print("Teacher added!")


def enroll_student():
    print("\nEnrolling Student into subjects...\n")
    try:
        s_id = int(input("Enter Student ID: "))
        sub_id = int(input("Enter Subject ID: "))
        try:
            cur.execute("INSERT INTO enrollments (student_id, subject_id) VALUES (?, ?)", (s_id, sub_id))
            con.commit()
            print("Enrollment Successful!")
        except sqlite3.IntegrityError:
            print("Student ID or Subject ID not found, OR student already enrolled.")
    except ValueError:
        print("IDs must be integers!")

def show_all_students():
    cur.execute("SELECT * FROM students")
    rows = cur.fetchall()
    print("\nThe List of Students:")
    print("ID | Name | Grade\n")
    for row in rows:
        print(f"{row[0]} | {row[1]} | {row[2]}")

def show_all_subjects():
    cur.execute("SELECT * FROM subjects")
    rows = cur.fetchall()
    print("\nThe List of Subjects:")
    for row in rows:
        print(f"{row[0]} | {row[1]} | {row[2]}")

def show_all_teachers():
    cur.execute("SELECT * FROM teachers")
    rows = cur.fetchall()
    print("\nThe List of Teachers:")
    for row in rows:
        print(f"{row[0]} | {row[1]} | {row[2]}")


def show_student_subjects():
    print("\nView Student Subjects\n")
    try:
        s_id = int(input("Enter Student ID to search: "))
        query = '''
                SELECT students.name, subjects.name
                FROM students
                         JOIN enrollments ON students.student_id = enrollments.student_id
                         JOIN subjects ON enrollments.subject_id = subjects.subject_id
                WHERE students.student_id = ? \
                '''
        cur.execute(query, (s_id,))
        results = cur.fetchall()

        if results:
            student_name = results[0][0]
            print(f"\n Subjects for {student_name}:")
            for row in results:
                print(f" - {row[1]}")
        else:
            print("No subjects found for this ID (or ID doesn't exist).")

    except ValueError:
        print("Please enter a valid number.")


def update_student_grade():
    print("\nUpdating Student Grade...\n")
    try:
        s_id = int(input("Enter Student ID: "))
        new_grade = int(input("Enter New Grade: "))
        cur = con.cursor()
        cur.execute("UPDATE students SET grade = ? WHERE student_id = ?", (new_grade, s_id))

        if cur.rowcount > 0:
            con.commit()
            print("Grade updated successfully!")
        else:
            print("Student ID not found.")
    except ValueError:
        print("Invalid input.")


def delete_student():
    print("\nDeleting Student...\n")
    try:
        s_id = int(input("Enter Student ID to DELETE: "))
        try:
            cur.execute("DELETE FROM students WHERE student_id = ?", (s_id,))
            if cur.rowcount > 0:
                con.commit()
                print("Student deleted successfully!")
            else:
                print("Student ID not found.")
        except sqlite3.IntegrityError:
            print("Student has related records. Delete enrollments first.")
    except ValueError:
        print("Invalid ID.")


def main():
    db_creation()

    while True:
        print("\n" + "*" * 35)
        print("SCHOOL MANAGEMENT SYSTEM MENU")
        print("*" * 35)
        print("1. Add Student")
        print("2. Add Subject")
        print("3. add teacher")
        print("4. Enroll Student")
        print("5. Show All Students")
        print("6. Show All Subjects")
        print("7. Show All Teachers")
        print("8. Show Student Subjects")
        print("9. Update Grade")
        print("10. Delete Student")
        print("11. Exit")

        choice = input("\n Choose an option (1-8): ")

        if choice == '1':
            insert_student()
        elif choice == '2':
            insert_subject()
        elif choice == '3':
            insert_teacher()
        elif choice == '4':
            enroll_student()
        elif choice == '5':
            show_all_students()
        elif choice == '6':
            show_all_subjects()
        elif choice == '7':
            show_all_teachers()
        elif choice == '8':
            show_student_subjects()
        elif choice == '9':
            update_student_grade()
        elif choice == '10':
            delete_student()
        elif choice == '11':
            break
        else:
            print("Invalid choice!")

if __name__ == "__main__":
    main()

con.close()