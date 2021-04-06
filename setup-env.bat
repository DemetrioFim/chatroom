@echo off

cd /D "%~dp0"

python -m virtualenv venv
call venv\Scripts\activate
pip install -r requirements.txt -U
set FLASK_APP=chatroom.py
