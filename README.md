# Recipe Daddy

## Installation

Run postgreSQL locally

```bash
sudo service postgreSQL start
or
sudo brew services start postgresql
```

## How to start

Create Virtual Environment

```bash
python3 -m venv env
```

Select python interpreter with env
Ctrl + Shift + `

```bash
pip install -r requirements.txt
```

Create .env according to stub.env

```bash
python manage.py makemigrations recipe_daddy
python manage.py migrate
python manage.py runserver
```
