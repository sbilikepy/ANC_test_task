# Test Task for Python Fullstack Developer Position

## Overview

This project includes the implementation of a web application that displays an
employee hierarchy and provides CRUD operations for managing employee data.

### Features

1. **Employee Hierarchy Tree**:
    - Displays a tree-like structure of employees.
    - Includes lazy loading to show additional levels on demand.

2. **Employee List Page**:
    - Lists all employees with sortable and searchable fields.
    - Provides sorting and searching functionality using Ajax for a seamless
      user experience.

3. **Authentication**:
    - Implements user authentication to restrict access to certain sections of
      the application.

4. **CRUD Operations**:
    - Provides full CRUD functionality for managing employee records, including
      reassigning subordinates when a supervisor changes.

### Models

- **Employee**: Stores information about each employee, including full name,
  position, hire date, email, and supervisor.
- **Position**: Represents various positions in the hierarchy with a defined
  level.

### Technologies Used

- **Python**: 🐍
- **Django**: For backend development and database management.
- **Twitter Bootstrap**: For basic styling of the web pages.
- **Django ORM Seeder**: To populate the database with initial data.
- **Ajax, JS**: For dynamic sorting and searching of employee records.

## Note on Database
To avoid having to populate the database from scratch, a database file 
with fake data is included in this project. If you want to use this 
pre-populated database, simply skip the seeding steps below.

## Installation

```
git clone https://github.com/sbilikepy/ANC_test_task.git
```

```
cd ANC_test_task
```

1. If you are using PyCharm - it may propose you to automatically create venv
   for your project
   and install requirements in it, but if not:
    ```
    python -m venv venv
    venv\Scripts\activate (on Windows)
    source venv/bin/activate (on macOS)
    ```

```
python.exe -m pip install --upgrade pip
```

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

![HIERARCHY](https://c.tenor.com/Pm6rIOnmIBYAAAAC/tenor.gif)
