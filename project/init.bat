py.exe -m venv venv
call venv\Scripts\activate.bat
pip install -r requirements.txt
cd ../src/web
python manage.py migrate
