class Users():
    def __init__(self, name, age):
        self.name = name
        self.age = age

    users_list = []
    def add_user(self):
        self.name = print(input("Enter your Name: "))    
        self.age = print(input("Enter Age: "))



    def welcome(self):
        print(f"Welcome!! {self.name}")


class Books():
    def __init__(self, title, author, year):
        self.title = title
        self.author = author
        self.year = year    


    def properties(self):
        print(f'''Book Properties: 
----------------------              
Book Name: {self.title}
Book Author: {self.author},
Release Date: {self.year}
''')



b1 = Books("book1", "john green", 1990)
b1.properties()
  
u1 = Users()  
u1.add_user()