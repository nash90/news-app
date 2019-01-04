# How to run the application
## Environment to run the application
- Python 3.7.8 
- Pip 18.1
- Pipenv

## Run Application command 
- from application root activate the virtual environment 
```
### Required for the first run
pipenv install 
### Start server
cd ./app
python manage.py runserver
```
- Stop server by Ctrl + C
```
Ctrl + C
```
- Access application from http://localhost:8000/

- Sample Application RUN
```
(venv) WL-223-234:app abinash$ python3 manage.py runserver
Performing system checks...

System check identified no issues (0 silenced).
October 15, 2018 - 23:13:27
Django version 2.1.2, using settings 'mysite.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CONTROL-C.

```
## Tests
- Test Settings

Test uses following pytest.ini settings
```
[pytest]
DJANGO_SETTINGS_MODULE=mysite.settings_test
addopts = --reuse-db
```
DJANGO_SETTINGS_MODULE setting is required for providing django context to test. 

"--reuse-db" is option provided by pytest-django plugin. It is used so that test enviroment does not delete the test database

- Run Tests

Run Test from inside "app" folder with command "pytest test" after activating virtual environment. Test are located in app/test folder
```
(venv) WL-198-226:app abinash$ pytest test
================================================ test session starts =================================================
platform darwin -- Python 3.7.0, pytest-3.10.0, py-1.7.0, pluggy-0.7.1
Django settings: mysite.settings_test (from ini file)
rootdir: /Users/abinash/Desktop/CGU/Courses/Software Development/project/IST303-Group-Project/app, inifile: pytest.ini
plugins: django-3.4.3, cov-2.6.0
collected 25 items

test/test_endpoint.py ......x.x.x........                                                                      [ 76%]
test/test_model.py ......                                                                                      [100%]

======================================== 22 passed, 3 xfailed in 2.08 seconds ========================================
(venv) WL-203-33:app abinash$
```

## Coverage
- How to run test coverage
After virutal environment activation, from inside the app folder, Run "pytest --cov=news"

```
(venv) WL-203-33:app abinash$ pytest --cov=news
================================= test session starts =================================
platform darwin -- Python 3.7.0, pytest-3.10.0, py-1.7.0, pluggy-0.7.1
Django settings: mysite.settings_test (from ini file)
plugins: django-3.4.3, cov-2.6.0
collected 25 items

test/test_endpoint.py ......x.x.x........                                       [ 76%]
test/test_model.py ......                                                       [100%]

---------- coverage: platform darwin, python 3.7.0-final-0 -----------
Name                             Stmts   Miss  Cover
----------------------------------------------------
news/__init__.py                     0      0   100%
news/admin.py                       11      0   100%
news/apps.py                         3      0   100%
news/models.py                      43      4    91%
news/service/__init__.py             0      0   100%
news/service/authentication.py      12      3    75%
news/service/news_service.py        83     15    82%
news/urls.py                         7      0   100%
news/views.py                      103      7    93%
----------------------------------------------------
TOTAL                              262     29    89%


======================== 22 passed, 3 xfailed in 2.55 seconds =========================
(venv) WL-203-33:app abinash$
```
## Install FAQ
- plugin/ module not found (ModuleNotFoundError)
Install full dependency plugin by following command from app folder

```
(venv) WL-203-33:app abinash$ pip install -r ./requirement.txt
```

- Django not found/ installed

Some user reported that in the first run Django was not loaded from Virtual Environment. 
In such case please install Django after virtual environment activation by 
```
pip install Django
```

- Pytest run fail/ pytest error

At first run pytest sometimes fails due to unable to locate the pytest-django library 
To fix the issue pytest-django needs to be installed from within virtual environment
```
pip install pytest-django
```
