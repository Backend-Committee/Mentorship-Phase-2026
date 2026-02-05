import sqlite3
import json

def connect_db():
    con = sqlite3.connect("Management_System.db")
    # عشان نفعل foreign_keys
    con.execute('PRAGMA foreign_keys = ON;')
    return con

def create_tables():
    con = connect_db()
    cur = con.cursor()
    
    cur.execute("""CREATE TABLE IF NOT EXISTS Student(
                    ST_ID INTEGER PRIMARY KEY,
                    Name Text Not NULL,
                    date_of_birth INTEGER,
                    address  Text,
                    parents_contact_number INTEGER
                    )""")
    
    cur.execute("""CREATE TABLE IF NOT EXISTS Teachers(
                    TE_ID INTEGER PRIMARY KEY,
                    Name Text Not NULL,
                    SALARY INTEGER,
                    Academic_specialty Text
    )""")
    
    cur.execute("""CREATE TABLE IF NOT EXISTS Subjects(
                    SU_ID INTEGER PRIMARY KEY,
                    Title Text Not NULL,
                    Credit INTEGER
    )""")
    
    cur.execute("""CREATE TABLE IF NOT EXISTS Classes(
                    CL_ID INTEGER PRIMARY KEY,
                    Class_name TEXT NOT NULL,
                    Maximu_capacity INTEGER
    )""")
    #Enrollment is connecting between Subjects And Student
    cur.execute("""CREATE TABLE IF NOT EXISTS Enrollment(
                    EN_ID INTEGER PRIMARY KEY,
                    ST_ID INTEGER,
                    SU_ID INTEGER,
                    Grade INTEGER,
                    Semester TEXT,
                    Attendance_Rate INTEGER,
                    FOREIGN KEY (ST_ID) REFERENCES Student(ST_ID),
                    FOREIGN KEY (SU_ID) REFERENCES Subjects(SU_ID)
    )""")
    #Supervision is connecting between Teachers And Student
    cur.execute("""CREATE TABLE IF NOT EXISTS Supervision(
                    Sup_ID INTEGER PRIMARY KEY,
                    ST_ID INTEGER,
                    TE_ID INTEGER,
                    Evaluation_Notes TEXT,
                    FOREIGN KEY (ST_ID) REFERENCES Student (ST_ID),
                    FOREIGN KEY (TE_ID) REFERENCES Teachers (TE_ID)
    )""")
    con.commit()
    con.close()

def insert_sample_data():
    con = connect_db()
    cur = con.cursor()
    
    # insert data into Student
    students_data = [
        ('Ahmed Ali', 2005, 'Cairo', 1012345678),
        ('Sara Ahmed', 2006, 'Giza', 1122334455),
        ('John Doe', 2005, 'Alexandria', 1277889900),
        ('Lila Youssef', 2007, 'Mansoura', 1555667788)
    ]
    cur.executemany("INSERT OR IGNORE INTO Student(Name, date_of_birth, address, parents_contact_number) VALUES(?,?,?,?)", students_data)

    # insert data into Teachers
    teachers_data = [
        ('Mr. Samy', 9000, 'Mathematics'),
        ('Ms. Mona', 8500, 'Physics'),
        ('Mr. Khaled', 9500, 'Computer Science')
    ]
    cur.executemany("INSERT OR IGNORE INTO Teachers (Name, SALARY, Academic_specialty) VALUES(?,?,?)", teachers_data)

    # insert data into Subjects
    subjects_data = [('Math 101', 3), ('Physics 1', 4), ('CS 50', 3)]
    cur.executemany("INSERT OR IGNORE INTO Subjects (Title, Credit) VALUES (?, ?)", subjects_data)

    # insert data into Classes
    classes_data = [('Class 1-A', 30), ('Science Lab', 20), ('Computer Lab 1', 25)]
    cur.executemany("INSERT OR IGNORE INTO Classes (Class_name, Maximu_capacity) VALUES (?, ?)", classes_data)

    # insert data into Enrollment
    enrollments = [(1, 1, 95, 'First', 100), (1, 3, 98, 'First', 95), (2, 2, 88, 'First', 90), (3, 3, 92, 'First', 85), (4, 1, 85, 'First', 92)]
    cur.executemany("INSERT OR IGNORE INTO Enrollment (ST_ID, SU_ID, Grade, Semester, Attendance_Rate) VALUES (?,?,?,?,?)", enrollments)

    # insert data into Supervision
    supervisions = [(1, 1, 'Excellent in Math'), (2, 2, 'Great improvement'), (3, 3, 'High tech skills'), (4, 1, 'Needs more practice')]
    cur.executemany("INSERT OR IGNORE INTO Supervision (ST_ID, TE_ID, Evaluation_Notes) VALUES (?, ?, ?)", supervisions)

    con.commit()
    con.close()
    print("\n✅ All tables populated with sample data successfully.")

def show_enrollments():
    con = connect_db()
    cur = con.cursor()
    query = """
    SELECT Student.Name, Subjects.Title 
    FROM Enrollment
    JOIN Student ON Enrollment.ST_ID = Student.ST_ID
    JOIN Subjects ON Enrollment.SU_ID = Subjects.SU_ID
    """
    cur.execute(query)
    rows = cur.fetchall()
    print("\n--- Enrollment Report (JOIN) ---")
    for row in rows:
        print(f"Student: {row[0]} | Subject: {row[1]}")
    con.close()

def update_and_delete_demo():
    con = connect_db()
    cur = con.cursor()
    cur.execute("UPDATE Student SET address='Alexandria' WHERE ST_ID = 1") 
    cur.execute("DELETE FROM Supervision WHERE Evaluation_Notes = 'Needs more practice'")
    con.commit()
    con.close()
    print("\n✅ Update and Delete operations performed.")

def export_all_to_json():
    con = connect_db()
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    
    db_data = {}
    tables = ['Student', 'Teachers', 'Subjects', 'Classes', 'Enrollment', 'Supervision']
    
    for table in tables:
        cur.execute(f"SELECT * FROM {table}")
        db_data[table] = [dict(row) for row in cur.fetchall()]
    
    with open('School_Database.json', 'w', encoding='utf-8') as f:
        json.dump(db_data, f, ensure_ascii=False, indent=4)
    
    con.close()
    print("\n✅ Database exported to 'School_Database.json' successfully!")

def menu():
    create_tables()
    while True:
        print("\n--- School Management System Menu ---")
        print("1. Insert Sample Data (All Tables)")
        print("2. Show Enrollment Report (SELECT & JOIN)")
        print("3. Run Update & Delete Demo")
        print("4. Export All Data to JSON")
        print("5. Exit")
        
        choice = input("Enter choice: ")
        if choice == '1': insert_sample_data()
        elif choice == '2': show_enrollments()
        elif choice == '3': update_and_delete_demo()
        elif choice == '4': export_all_to_json()
        elif choice == '5': break
        else: print("Invalid choice.")

if __name__ == "__main__":
    menu()