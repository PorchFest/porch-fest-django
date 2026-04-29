# porch-fest-django
## prerequisites
- clone server to local machine that supports Python, pip, and Django
- navigate to project directory
- Download and install Python from `https://www.python.org/downloads/`
- Confirm it is installed using `python --version`
- `pip install django`
- if needed delete and reinstall the venv folder using `python -m venv venv`
- `python -m pip install django`
- copy the contents of `.env.example` in the site root into a new file named `.env`
- Generate a secretkey and place it in that file.
- The contents of your `.env` file must contain
- download and run the PostgresSLQ installer from `https://www.postgresql.org/download/`
- Add this to the Windows system path if required `C:\Program Files\PostgreSQL\18\bin` (where 18 is the Postgres version number you installed)
- create a PostgresSLQ database
    - On Windows (cmd) `createdb -U postgres porch_fest`
    - On macOS/Linux `sudo -u postgres createdb porch_fest`
- You also need to install the POSTGIS Plugin in your postgres database
- Add the username and password you created to your `.env` file
- Download and install OSGeo4W from `https://trac.osgeo.org/osgeo4w/`
- `pip install -r requirements.txt`
- run `python manage.py makemigrations` to generate database tabe scripts
- run `python manage.py migrate` to build database tables
- create python super user `python manage.py createsuperuser` (you will use this username and password to login to the django admin panel)
- make a copy of the .env_exmple file and name it `.env`
- update the values in the file (ask another dev if you are sharing the project)
- `npm install -g sass`
## run project
- `python manage.py runserver`
- `sass --watch sass/style.scss static/css/style.css`