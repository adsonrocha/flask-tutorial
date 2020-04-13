# Installation

```bash
python -m pip install --upgrade pip
```
```bash
python install virtualenv
virtualenv [-p python3] venv
cd venv/Scripts activate
```
Go to File => settings => Project:<name> => Python Interpreter => 
*cog icon* => *add/change venv interpreter*
```bash
pip install flask
```

### Run

```bash
python app.py
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
- app
    - models\
        \__init\__.py
    - controllers\
        \__init\__.py
    - static
    - templates\
     \__init\__.py\
run.py
     
Each \__ini\__ indicates a module

## ORM
```bash
pip install flask-sqlalchemy
```