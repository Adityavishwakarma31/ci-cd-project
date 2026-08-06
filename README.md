# Ledger — Django Todo App

A minimal, classy dark-themed to-do list built with Django, vanilla HTML/CSS, and a Dockerfile for containerized deployment.

## Features
- Add / edit / delete tasks
- Mark complete with a single click (toggle)
- Priority levels: Low / Medium / High
- Task counter (Total / Pending / Done)
- Elegant dark UI with gold accents (no external CSS framework)

## Run locally (without Docker)

```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Visit http://127.0.0.1:8000/

## Run with Docker

Build the image:
```bash
docker build -t django-todo-app .
```

Run the container:
```bash
docker run -d -p 8000:8000 --name todo-app django-todo-app
```

Visit http://localhost:8000/

## Run with Docker Compose (recommended)

```bash
docker compose up --build
```

Stop it with:
```bash
docker compose down
```

## Project structure
```
todoapp/
├── manage.py
├── requirements.txt
├── Dockerfile
├── .dockerignore
├── docker-compose.yml
├── todoproject/       # Django project settings
├── todos/             # Todo app (models, views, forms, templates)
└── static/css/style.css
```

## Notes for deployment
- Uses `gunicorn` as the production WSGI server (not Django's dev server) inside Docker.
- Uses `whitenoise` to serve static files directly from the container — no need for nginx for a simple deployment.
- SQLite is used by default (fine for a portfolio/demo project). For production, swap in Postgres via `DATABASES` in `settings.py`.
- `ALLOWED_HOSTS = ['*']` is set for demo convenience — restrict this to your actual domain in real production.
