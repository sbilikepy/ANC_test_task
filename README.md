# Test task for ANC team


This project includes the implementation of a web application that displays an employee hierarchy and provides CRUD operations for managing employee data.


## Installation Steps



`
git clone https://github.com/sbilikepy/ANC_test_task.git
`
1. If you are using PyCharm - it may propose you to automatically create venv for your project 
    and install requirements in it, but if not:
    ```
    python -m venv venv
    venv\Scripts\activate (on Windows)
    source venv/bin/activate (on macOS)
    ```
`
cd dir
`

`
python.exe -m pip install --upgrade pip
`

`
pip install -r requirements.txt
`

`
python manage.py makemigrations
`

`
python manage.py migrate
`

`
python manage.py loaddata positions_db_data.json
`

`
python seed_db_employee.py
`

`
python seed_db_position.py
`

`
python seed_db_supervisor.py
`

`
python manage.py runserver 
`

![Alt Text](https://s2.ezgif.com/tmp/ezgif-2-54d2753c6d.gif)
![Alt Text](https://s3.ezgif.com/tmp/ezgif-3-72b0edb7db.gif)

