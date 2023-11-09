# Recipe Daddy

## Installation

Install postgreSQL if you don't have it installed and add it to your PATH environment variable

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

Create .env and fill it up according to stub.env

Create database named after the DB_NAME in your newly created .env in psql shell or any GUI you opt for

```bash
python manage.py makemigrations recipe_daddy
python manage.py migrate
python manage.py runserver
```
