# Bank System

## Currently Working Features:
* Customers and Accounts CRUD operation.
* Deposits and Withdrawal are validated first then applied.
* Every transaction is recorded in the database with its date.

## لسه فاضل تكه

التطبيق شغال وخلص تقريبا وممكن تجربيه/تجربه فاضل بس

* authentication
* transfer transaction
* postman testing

## ازاي تستخدمه ؟
``` 
python manage.py migrate
python manage.py runserver
```

ودي ال endpoints اللي فيها الأكشن:
* http://127.0.0.1:8000/customer/
* http://127.0.0.1:8000/account/
* http://127.0.0.1:8000/deposit/
* http://127.0.0.1:8000/withdraw/
* http://127.0.0.1:8000/staff/

## ERD
![ERD DIAGRAM IMAGE](https://github.com/Backend-Committee/Mentorship-Phase-2026/blob/Omar-Azzam/task_7/ERD.PNG)
