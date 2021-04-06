@echo off

cd /D "%~dp0"

python -m virtualenv venv
call venv\Scripts\activate
pip install -r requirements.txt -U
set FLASK_APP=chatroom.py
flask db init
flask db migrate -m "users table"
flask db upgrade
flask db migrate -m "posts table"
flask db upgrade