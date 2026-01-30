from sqlalchemy import create_engine, select
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker
from sqlalchemy.exc import IntegrityError

from utils import get_opt, get_int

class Base(DeclarativeBase): ...

class Student(Base):
    __tablename__ = "students"

    id: Mapped[int] = mapped_column(primary_key=True)
    full_name: Mapped[str] = mapped_column(unique=True)
    level: Mapped[int]

engine = create_engine("sqlite:///database.db")
session_factory = sessionmaker(engine)

def create_student():
    id = get_int("Student ID: ")
    full_name = input("Full name: ").strip()
    level = get_int("Level: ")
    
    if len(full_name) == 0:
        print("the full name can't be empty!")
        return
    
    if level < 1 or level > 4:
        print("the level must be between 1 and 4")
        return
    
    student = Student(id=id, full_name=full_name, level=level)
    
    try:        
        with session_factory.begin() as session:
                session.add(student)
    except IntegrityError as e:
        print(e.orig)

def update_student():
    id = get_int("Student ID: ")
    
    with session_factory.begin() as session:
        student = session.execute(select(Student).where(Student.id==id)).scalar_one_or_none()
        if student == None:
            print("This student doesn't exist!")
            return
        
        print(f"Existing full name: {student.full_name}")
        full_name = input("Full name: ").strip()
        print(f"Existing level: {student.level}")
        level = get_int("Level: ")
        
        if len(full_name) == 0:
            print("the full name can't be empty!")
            return
        
        if level < 1 or level > 4:
            print("the level must be between 1 and 4")
            return 
        
        student.full_name = full_name
        student.level = level
        print("Student updated successfully!")

def delete_student():
    id = get_int("Student ID: ")
    
    with session_factory.begin() as session:
        student = session.execute(select(Student).where(Student.id==id)).scalar_one_or_none()
        if student == None:
            print("This student doesn't exist!")
            return
        
        session.delete(student)
        print("Student deleted successfully!")

def read_student():
    id = get_int("Student ID: ")
    
    with session_factory.begin() as session:
        student = session.execute(select(Student).where(Student.id==id)).scalar_one_or_none()
        if student == None:
            print("This student doesn't exist!")
            return
        
        print(f"Full name: {student.full_name}")
        print(f"Level: {student.level}")

def read_all_students():
    with session_factory.begin() as session:
        students = session.execute(select(Student)).scalars()
        
        for student in students:
            print(f"ID: {student.id}")
            print(f"Full name: {student.full_name}")
            print(f"Level: {student.level}")
            print()
            
        
if __name__ == "__main__":
    with engine.begin() as conn:
        Base.metadata.create_all(conn)
    
    print("WELCOME TO STUDENTS MANAGER")
    print()
    print("1- Create A Student")
    print("2- Update A Student")
    print("3- Delete A Student")
    print("4- Read A Student")
    print("5- Read All Students")
    print()
    choice = get_opt(1, 5)
    
    if choice == 1:
        create_student()
    elif choice == 2:
        update_student()
    elif choice == 3:
        delete_student()
    elif choice == 4:
        read_student()
    elif choice == 5:
        read_all_students()