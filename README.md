# ANC_test_task 
python.exe -m pip install --upgrade pip
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py loaddata positions_db_data.json
python seed_db_employee.py
python seed_db_position.py
python seed_db_supervisor.py

