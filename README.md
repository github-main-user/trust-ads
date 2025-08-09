# Trust Ads

Documentation is available on: [English 🇺🇸](README.md) | [Russian 🇷🇺](README.ru.md)

This is a Django REST Framework backend for a classified ads platform with user authentication, role management, ad posting, reviews, and search functionality.

## Features

- User registration and authentication with JWT
- Role-based access control: regular users and admins
- Password change and reset via email
- CRUD operations for ads
  - Users can manage their own ads
  - Admins can manage all ads
- Reviews on ads with CRUD and permissions
- API documentation with Swagger and Redoc (via `drf-spectacular`)
- CORS headers enabled for frontend integration
- Dockerized setup with `docker compose`

## Tech Stack

- Python 3.13+
- Django 5.x
- Django REST Framework
- PostgreSQL
- Simple JWT for authentication
- drf-spectacular for API docs
- Docker & Docker Compose
- Nginx
- Pytest

## Setup

### Requirements

- Docker and Docker Compose installed

### Running locally with Docker

1. Clone the repo:
```bash
git clone https://github.com/github-main-user/trust-ads.git
cd trust-ads
```

2. Setup environment variables
```shell
cp .env.example .env
```

3. Build and run containers:
```bash
docker compose up --build
```

4. The backend API will be available at: `http://localhost:80/`

- `http://localhost:80/api/v1/docs/` - swagger documentation
- `http://localhost:80/api/v1/redoc/` - redoc documentation
- `http://localhost:80/admin/` - admin panel

### Admin panel
To create an admin user use this command:
```shell
docker compose exec web python manage.py createsuperuser
```

For demonstration purposes some sample data has been prepared in fixtures.
You can load them using this command:
```shell
docker compose exec web python manage.py loaddata fixtures.json
```

## Tests

Command to run tests:
```shell
docker compose run --rm web pytest
```

### Test Coverage

You can see coverage using the command below:
```shell
docker compose run --rm web bash -c "coverage run -m pytest && coverage report"
```

## Notes

* Admin role users have full control over ads and comments.
* Anonymous users can only view ads.
* Ads and comments are sorted by creation date descending.
* Pagination limits ads listing to 4 per page.
* Password reset flow is email token based.
