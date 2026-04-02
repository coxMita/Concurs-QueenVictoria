# Queen Victoria Contest Website

A Django-based web application for the **"Concursul Național de Cultură și Civilizație Britanică – Queen Victoria"**.

---

## Project Structure

```
CONCURS-QUEENVICTORIA/
│
├── config/                         # Django project configuration
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
│
├── pages/                          # Main Django app
│   ├── models.py                   # All database models
│   ├── views.py                    # Public page views
│   ├── urls.py                     # Public URL routes
│   ├── admin.py                    # Django admin configuration
│   ├── panel_views.py              # Custom admin panel views
│   ├── panel_urls.py               # Custom admin panel URL routes
│   │
│   └── templates/
│       ├── pages/                  # Public page templates
│       │   ├── home.html
│       │   ├── informatii.html
│       │   ├── calendar.html
│       │   ├── parteneri.html
│       │   ├── subiecte.html
│       │   ├── rezultate.html
│       │   ├── arhiva.html
│       │   ├── tematica.html
│       │   ├── regulament.html
│       │   ├── galerie.html
│       │   └── blank_page.html
│       │
│       └── panel/                  # Custom admin panel templates
│           ├── base.html
│           ├── login.html
│           ├── dashboard.html
│           ├── config.html
│           ├── arhiva.html
│           ├── arhiva_folder.html
│           ├── rezultate_years.html
│           ├── rezultate_judete.html
│           ├── rezultate_etape.html
│           └── rezultate_docs.html
│
├── templates/                      # Project-wide templates
│   ├── base.html                   # Base layout (header + footer + blocks)
│   └── components/
│       ├── header.html
│       ├── footer.html
│       └── sections/
│           ├── home/
│           │   ├── hero.html
│           │   ├── about_contest.html
│           │   └── organizer.html
│           ├── informatii/
│           │   ├── informatii_intro.html
│           │   ├── informatii_etape.html
│           │   ├── informatii_structura.html
│           │   ├── informatii_calificare.html
│           │   ├── informatii_premiere.html
│           │   └── informatii_contestatii.html
│           ├── Subiecte/
│           │   ├── content.html
│           │   └── button_section.html
│           ├── tematica/
│           │   └── tematica.html
│           ├── regulament/
│           │   └── regulament.html
│           └── galerie/
│               └── galerie.html
│
├── static/
│   ├── css/
│   │   ├── main.css                # Public site styles
│   │   └── panel.css               # Custom admin panel styles
│   ├── ts/
│   │   └── main.js
│   ├── images/                     # AVIF images (background, gallery, partners, hero)
│   └── pdfs/                       # Static PDFs (tematica, regulament, guide)
│
├── media/                          # User-uploaded files (PDFs via admin/panel)
│   ├── archive/                    # Uploaded archive documents
│   └── rezultate/                  # Uploaded results documents
│
├── requirements.txt
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

### 2. Create virtual environment

```bash
uv venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
uv pip install -r requirements.txt
```

### 4. Run migrations

```bash
python manage.py migrate
```

### 5. Create a superuser

```bash
python manage.py createsuperuser
```

### 6. Run development server

```bash
python manage.py runserver
```

---

## Public Pages

| Route | Description |
|---|---|
| `/` | Home page |
| `/informatii/` | Contest information |
| `/calendar/` | Competition calendar |
| `/parteneri/` | Partners |
| `/surse/` | Sources |
| `/subiecte/` | Subjects |
| `/rezultate/` | Results — 3-level accordion (Year → Judet → Etapa → PDFs) |
| `/arhiva/` | Archive — folders with downloadable PDFs |
| `/tematica/` | Tematica PDF viewer |
| `/regulament/` | Regulament PDF viewer |
| `/galerie/` | Photo gallery |

---

## Admin Interfaces

### Django Admin — `/admin/`

Standard Django admin. Registered models:

- **ArchiveFolder** / **ArchiveDocument** — Arhiva subiecte & bareme with bulk PDF upload
- **RezultateYear** / **RezultateJudet** / **RezultateEtapa** / **RezultateDocument** — Results hierarchy with auto-populate action
- **JudetConfig** / **EtapaConfig** — Default lists used when creating new years/judete

### Custom Panel — `/panel/`

A purpose-built management UI for easier content management. Requires staff login.

| Route | Description |
|---|---|
| `/panel/` | Redirects to login |
| `/panel/login/` | Login with admin credentials |
| `/panel/dashboard/` | Overview with stats and recent items |
| `/panel/rezultate/` | Create years (auto-populates judete + etape from config) |
| `/panel/rezultate/<year_id>/` | Manage judete for a year |
| `/panel/rezultate/<year_id>/<judet_id>/` | Manage etape for a judet |
| `/panel/rezultate/<year_id>/<judet_id>/<etapa_id>/` | Upload/delete PDFs (drag & drop) |
| `/panel/config/` | Edit default JudetConfig & EtapaConfig lists |
| `/panel/arhiva/` | Create/delete archive folders |
| `/panel/arhiva/<folder_id>/` | Upload/delete PDFs in an archive folder (drag & drop) |

---

## Data Models

### Arhiva

```
ArchiveFolder
└── ArchiveDocument (PDF, upload_to: archive/<folder>/)
```

### Rezultate

```
JudetConfig          ← global defaults for auto-population
EtapaConfig          ← global defaults for auto-population

RezultateYear
└── RezultateJudet
    └── RezultateEtapa
        └── RezultateDocument (PDF, upload_to: rezultate/<year>/<judet>/<etapa>/)
```

When a new `RezultateYear` is created (via panel or admin action), all judete from `JudetConfig` and all etape from `EtapaConfig` are automatically generated.

---

## Architecture

All public pages extend `templates/base.html` which provides:
- `{% block title %}` — page title
- `{% block body_class %}` — CSS class for page-specific background
- `{% block content %}` — main content

The panel uses a separate `pages/templates/panel/base.html` with a sidebar layout and its own `static/css/panel.css`, completely independent of the public site styles.

---

## Authors

- Mihai Briceag
- Stefan Sisu

---

## License

This project is for educational and competition purposes.
