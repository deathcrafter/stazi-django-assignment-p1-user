@REM install virtualenv if not installled
pip install virtualenv --quiet

@REM remove venv directory if exists
rmdir /q /s .\venv

virtualenv venv
call .\venv\Scripts\activate.bat

@REM upgrade pip
python -m pip install --upgrade pip

@REM install required packages
pip install -r requirements.txt

@REM create migrations
python manage.py makemigrations
python manage.py migrate

@REM set superuser credentials
set DJANGO_ADMIN_USERNAME="admin"
set DJANGO_ADMIN_EMAIL="admin@stazi.com"
set DJANGO_ADMIN_PASSWORD="admin"

python manage.py createsuperuser --username %DJANGO_ADMIN_USERNAME% --email %DJANGO_ADMIN_EMAIL% --no-input

@REM run server at specified port
python manage.py runserver 8000