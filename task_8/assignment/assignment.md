# Khazna Storage Management System

Khazna is a storage company that provides **secure storage services** to its customers.  
The company owns multiple **warehouses across the country** where customers can store their goods.

Khazna wants to build a **computer system** to manage its operations.  
You have been tasked with designing and implementing this system using **Object-Oriented Programming (OOP)**.


## System Entities

Your program should manage the following types of data.


## Customers

Customers are people who store their goods in Khazna warehouses.

Each customer should have:

- **ID**
- **Name**
- **Phone Number**
- **Address**

## Employees

Employees work for Khazna and help operate the warehouses.

Each employee should have:

- **ID**
- **Name**
- **Phone Number**
- **Address**
- **Salary**
- **Working Hours**

## Stored Items

Stored items represent the goods that customers store in the warehouses.

Each item should contain:

- **ID**
- **Name**
- **Weight**
- **Size**
- **Quantity**
- **Owner (Customer)**

Each item must belong to a **customer**.

## Program Requirements

Your program must include a **menu-based interface** that allows the user to manage the system.

The program should allow the user to perform the following operations.

---

## Customer Management

The system should allow the user to:

- List all customers
- View the details of a specific customer
- Add a new customer
- Delete a customer

---

## Employee Management

The system should allow the user to:

- List all employees
- View the details of a specific employee
- Add a new employee
- Delete an employee

---

## Item Management

The system should allow the user to:

- List all stored items
- View the details of a specific item
- Add a new item
- Delete an item

When adding an item, the program should ensure that the **owner (customer) exists**.


# Notes
- Feel free to extend the system or add any features you want
- You are **not required** to use a database or file storage,
It is completely acceptable to store data using **lists or other in-memory data structures**.


