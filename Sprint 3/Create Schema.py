import mysql.connector

systemDB = mysql.connector.connect(
    host= 'localhost',
    user = 'root',
    passwd ='0000',
    database = 'Gym_Booking'
)

cursor = systemDB.cursor()
try:
    cursor.execute('''
    CREATE TABLE Member(id INT AUTO_INCREMENT PRIMARY KEY, name varchar(100) not null , phone_number varchar(50));
    ''')

    cursor.execute('''
    CREATE TABLE Class(
    id INT AUTO_INCREMENT PRIMARY KEY , name varchar(100) not null , Duration integer NOT NULL,
    Day varchar(50) NOT NULL);
    ''')

    cursor.execute('''
    CREATE TABLE Booking(
    booking_id INT AUTO_INCREMENT PRIMARY KEY , member_id INTEGER NOT NULL, class_id INTEGER NOT NULL, Booking_date DATE NOT NULL,
    FOREIGN KEY (member_id) REFERENCES Member(id),
    FOREIGN KEY (class_id) REFERENCES Class(id)
    );
    ''')
except mysql.connector.Error as err:
    print(f"Error creating tables: {err}")

