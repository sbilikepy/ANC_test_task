# ANC_test_task 

pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py loaddata positions_db_data.json
python seed_db_employee.py
python seed_db_position.py
python seed_db_supervisor.py

