# Gym class booking system

import mysql.connector
try:
    systemDB = mysql.connector.connect(
        host="localhost",
        user='root',
        password='0000',
    )
    cursor = systemDB.cursor()

    cursor.execute('''CREATE DATABASE IF NOT EXISTS Gym_Booking''')
except mysql.connector.Error as err:
    print(f"Error connecting to MySQL database: {err}")
