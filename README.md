# Installation

```bash
python -m pip install --upgrade pip
```
```bash
python install virtualenv
virtualenv [-p python3] venv
cd venv/Scripts activate
```
```bash
pip install flask
```

### Run

```bash
python app.py
```

### Check installed packages

```bash
pip freeze > packages.txt
```

To install from a packages.txt file:

```bash
pip install -r packages.txt
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