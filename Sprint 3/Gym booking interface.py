import mysql.connector
from datetime import date
systemDB = mysql.connector.connect(
    host= 'localhost',
    user = 'root',
    passwd ='0000',
    database = 'gym_booking'
)

cursor = systemDB.cursor()
#insertions for member
def add_member(name, phone_number):
    query = "INSERT INTO Member (name, phone_number) VALUES (%s, %s)"
    values = (name, phone_number)
    cursor.execute(query, values)
    systemDB.commit()


def validate_member(name , phone_number):
   if name == '' or len(name) > 100:
       return False
   if phone_number == '' or len(phone_number) > 50:
       return False
   return True

#insertions for class
def add_class(name, duration, day):
    query = "INSERT INTO Class (name, Duration, Day) VALUES (%s, %s, %s)"
    values = (name, duration, day)
    cursor.execute(query, values)
    systemDB.commit()

def validate_class(name, duration, day):
   if name == '' or len(name) > 100:
       return False
   if not duration.isdigit():
       return False
   if day == '' or len(day) > 50:
       return False
   return True

#insertions for booking
def add_booking(member_id, class_id, booking_date):
    query = "INSERT INTO Booking (member_id, class_id, Booking_date) VALUES (%s, %s, %s)"
    values = (member_id, class_id, booking_date)
    cursor.execute(query, values)
    systemDB.commit()

def validate_booking(member_id, class_id, booking_date):
   if not member_id.isdigit():
       return False
   if not class_id.isdigit():
       return False
   if booking_date == None:
       return False
   return True


def Member_Menu():
    while True:
        print(
'''
1) Add member
2) View all members
3) View member
4) Update member
5) Delete member
6) Back to main menu
'''
    )

        choice = input("Enter choice: ")
        if choice == '1':
            name = input("Enter member name: ")
            phone_number = input("Enter phone number: ")
            if validate_member(name, phone_number):
                add_member(name, phone_number)
                print("Member added successfully.")
        elif choice == '2':
            cursor.execute("SELECT * FROM Member")
            result = cursor.fetchall()
            for row in result:
                print(row)
        elif choice == '3':
            member_id = input("Enter member ID: ")
            cursor.execute("SELECT * FROM Member WHERE id = %s", (member_id,))
            result = cursor.fetchone()
            if result:
                print(result)
            else:
                print("Member not found.")
        elif choice == '4':
            member_id = input("Enter member ID: ")
            cursor.execute("SELECT * FROM Member WHERE id = %s", (member_id,))
            result = cursor.fetchone()
            if not result:
                print("Member not found.")
                continue
            name = input("Enter new name: ")
            phone_number = input("Enter new phone number: ")
            if validate_member(name, phone_number):
                cursor.execute("UPDATE Member SET name = %s, phone_number = %s WHERE id = %s", (name, phone_number, member_id))
                systemDB.commit()
                print("Member updated successfully.")
            else:
                print("Invalid input.")
        elif choice == '5':
            member_id = input("Enter member ID: ")
            cursor.execute("DELETE FROM Member WHERE id = %s", (member_id,))
            systemDB.commit()
            print("Member deleted successfully.")
        elif choice == '6':
            return
        else:
            print('Enter a valid choice: ')
            continue


def Classes_Menu():
    while True:
        print(
            '''
1) Add class
2) View all classes
3) View class
4) Update class
5) Delete class
6) Back to main menu            
            ''')

        choice = input("Enter choice: ")
        if choice == '1':
            name = input("Enter class name: ")
            duration = input("Enter class duration: ")
            day = input("Enter class day: ")
            if validate_class(name, duration, day):
                add_class(name, duration, day)
                print("Class added successfully")
            else:
                print("Invalid input.")
        elif choice == '2':
            cursor.execute("SELECT * FROM Class")
            result = cursor.fetchall()
            for row in result:
                print(row)
        elif choice == '3':
            class_id = input("Enter class ID: ")
            cursor.execute("SELECT * FROM Class WHERE id = %s", (class_id,))
            result=cursor.fetchone()
            if result:
                print(result)
            else:
                print("Class not found.")
        elif choice == '4':
            class_id = input("Enter class ID: ")
            cursor.execute("SELECT * FROM Class WHERE id = %s", (class_id,))
            result=cursor.fetchone()
            if not result:
                print("Class not found.")
                continue
            name = input("Enter new name: ")
            duration = input("Enter new duration: ")
            day = input("Enter new day: ")
            if validate_class(name, duration, day):
                cursor.execute("UPDATE Class SET name = %s, Duration = %s, Day = %s WHERE id = %s", (name, duration, day, class_id))
                systemDB.commit()
                print("Class updated successfully.")
            else:
                print("Invalid input.")
        elif choice == '5':
            class_id = input("Enter class ID: ")
            cursor.execute("DELETE FROM Class WHERE id = %s", (class_id,))
            systemDB.commit()
            print("Class deleted successfully.")
        elif choice == '6':
            return
        else:
            print('Enter a valid choice: ')
            continue


def Booking_Menu():
    while True:
        print(
            '''
    1) Create new booking
    2) View all bookings
    3) View booking by ID
    4) View bookings by member ID
    5) View bookings by class ID
    6) Delete booking
    7) Back to main menu       
            '''
        )
        choice = input('Enter choice: ')
        if choice == '1':
            member_id = input('Enter Member ID: ')
            class_id = input('Enter Class ID: ')
            if validate_booking(member_id, class_id, date.today()):
                add_booking(member_id, class_id, date.today())

                print("Booking added successfully.")
            else:
                print("Invalid input.")
        elif choice == '2':
            cursor.execute("SELECT * FROM Booking")
            result = cursor.fetchall()
            for row in result:
                print(row)
        elif choice == '3':
            booking_id = input("Enter booking ID: ")
            cursor.execute("SELECT * FROM Booking WHERE id = %s", (booking_id,))
            result = cursor.fetchone()
            if result:
                print(result)
            else:
                print("Booking not found.")
        elif choice == '4':
            Member_id = input('Enter Member ID: ')
            cursor.execute("SELECT * FROM Booking WHERE member_id = %s", (Member_id,))
            result = cursor.fetchall()
            for row in result:
                print(row)
        elif choice == '5':
            Class_id = input('Enter Class ID: ')
            cursor.execute("SELECT * FROM Booking WHERE class_id = %s", (Class_id,))
            result = cursor.fetchall()
            for row in result:
                print(row)
        elif choice == '6':
            booking_id = input("Enter booking ID: ")
            cursor.execute("DELETE FROM Booking WHERE id = %s", (booking_id,))
            systemDB.commit()
            print("Booking deleted successfully.")
        elif choice == '7':
            return
        else:
            print('Enter a valid choice: ')
            continue


def Main_Menu():
    while True:
        print('''
1) Manage Members
2) Manage Classes
3) Manage Bookings
4) Exit
        ''')

        choice = input("Enter choice: ")
        if choice == '1':
           Member_Menu()
        elif choice == '2':
            Classes_Menu()
        elif choice == '3':
            Booking_Menu()
        else:
            print('Enter a valid choice: ')
            continue


if __name__ == "__main__":
    Main_Menu()