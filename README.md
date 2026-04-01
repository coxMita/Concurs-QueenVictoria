# 🇬🇧 Queen Victoria Contest Website

A Django-based web application for the **“Concursul Național de Cultură și Civilizație Britanică – Queen Victoria”**.

## Project Structure

```
CONCURS-QUEENVICTORIA/
│
├── config/                 # Django project configuration
│   ├── settings.py
│   ├── urls.py
│
├── pages/                  # Main app for pages
│   ├── views.py
│   ├── urls.py
│   └── templates/pages/    # Page-level templates
│       ├── home.html
│       ├── informatii.html
│       ├── calendar.html
│       └── blank_page.html
│
├── templates/              # Global templates
│   ├── base.html
│   └── components/
│       ├── header.html
│       ├── footer.html
│       └── sections/
│           ├── hero.html
│           ├── about_contest.html
│           └── organizer.html
│
├── static/                 # Static files
│   ├── css/
│   │   └── main.css
│   ├── ts/
│   │   └── main.js
│   └── images/
│
├── manage.py
└── db.sqlite3
```

---

## Setup & Installation

### 1. Clone the repository

```bash
git clone https://github.com/your-username/queen-victoria-site.git
cd queen-victoria-site
```

---

### 2. Create virtual environment (using uv)

```bash
uv venv
source .venv/bin/activate
```

---

### 3. Install dependencies

```bash
uv pip install django
```

---

### 4. Run migrations

```bash
python manage.py migrate
```

---

### 5. Run development server

```bash
python manage.py runserver
```

Open:

```
http://127.0.0.1:8000/
```

---

## Architecture Overview

### 🔹 Base Layout

All pages extend:

```
templates/base.html
```

It includes:

* Header component
* Footer component
* Static CSS/JS

---

### 🔹 Components System

Reusable UI elements:

```
templates/components/
```

* `header.html` → navigation
* `footer.html` → contact info
* `sections/` → homepage blocks

---

### 🔹 Page Composition

Example:

```
home.html
```

```html
{% extends "base.html" %}

{% block content %}
    {% include "components/sections/hero.html" %}
    {% include "components/sections/about_contest.html" %}
    {% include "components/sections/organizer.html" %}
{% endblock %}
```

✔ Each section is modular
✔ Easy to reuse or reorder

---

## Static Files

All static assets are stored in:

```
static/
```

Usage in templates:

```django
{% load static %}
<img src="{% static 'images/example.avif' %}">
```

---

## Pages

| Route          | Description           |
| -------------- | --------------------- |
| `/`            | Home page             |
| `/informatii/` | Detailed contest info |
| `/calendar/`   | Calendar              |
| `/parteneri/`  | Blank page            |
| `/surse/`      | Blank page            |
| `/subiecte/`   | Blank page            |
| `/rezultate/`  | Blank page            |
| `/arhiva/`     | Blank page            |
| `/tematica/`   | Blank page            |
| `/regulament/` | Blank page            |
| `/galerie/`    | Blank page            |

---

## Best Practices Used

* DRY (Don't Repeat Yourself)
* Separation of concerns
* Component-based templating
* Clean routing with Django
* Scalable folder structure

---

## Authors

* Mihai Briceag
* Stefan Sisu

---

## License

This project is for educational and competition purposes.
