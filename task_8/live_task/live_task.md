# OOP Session Task

Geometrical shapes are interesting, and what is interesting more is abstracting them in a computer program, **try to create a program that works as follows**:

```
Enter the rectangle length: 8
Enter the rectangle height: 4

The area of the rectangle is 32
The perimeter of the rectangle is 24 

Image:
-  -  -  -  -  -  -  -  -
-                       -
-                       -
-                       -
-  -  -  -  -  -  -  -  -

Enter square side length: 5

The area of the square is 25
The perimeter of the square is 20

Image: 
-  -  -  -  -  -
-              -     
-              -     
-              -
-              -
-  -  -  -  -  -
```

You should create two classes **Rectangle** and **Square** and you should also use OOP features like **inheritance** and **polymorphism** to make this work.

Here is the base shape class that you can use:
``` Python
class Shape:
    def __init__(self):
        ...
    
    def get_input(self):
        ...
    
    def calculate_area(self):
        ...
    
    def calculate_perimeter(self):
        ...
    
    def __str__(self):
        """This should return an ASCII art representation of the shape"""
```