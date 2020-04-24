# Installation

```bash
python -m pip install --upgrade pip
```
```bash
python install virtualenv
virtualenv [-p python3] venv
venv/Scripts/activate
```
Go to File => settings => Project:<name> => Python Interpreter => 
*cog icon* => *add/change venv interpreter*
```bash
pip install flask
```

### Run

```bash
$ set FLASK_APP=flaskr
$ set FLASK_ENV=development
$ flask init-db
$ flask run
```

### Enable debug mode
```bash
C:\path\to\app>set FLASK_ENV=development
```

### Check installed packages

```bash
pip freeze > requirements.txt
```

To install from a requirements.txt file:

```bash
pip install -r requirements.txt
```

## Project architecture
- app\
    * __init\__.py\
    * run.py
    - models
        * \__init\__.py
    - controllers
        * \__init\__.py
    - static
    - templates    
     
Each \__ini\__ indicates a module

## ORM
```bash
pip install flask-sqlalchemy
```