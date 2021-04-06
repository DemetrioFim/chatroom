cd "$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

python -m virtualenv venv
source venv/Scripts/activate
pip install -r requirements.txt -U
export FLASK_APP=chatroom.py
flask db init
flask db migrate -m "users table"
flask db upgrade
flask db migrate -m "posts table"
flask db upgrade