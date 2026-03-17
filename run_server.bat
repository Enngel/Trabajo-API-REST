@echo off
cd "C:\Users\engel\Trabajo-API-REST"
call .venv\Scripts\activate.bat
python manage.py migrate
python manage.py runserver
pause

