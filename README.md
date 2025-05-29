# ReEnAct

Regionale Energiewende aktiv gestalten

[![Built with Cookiecutter Django](https://img.shields.io/badge/built%20with-Cookiecutter%20Django-ff69b4.svg?logo=cookiecutter)](https://github.com/cookiecutter/cookiecutter-django/)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

License: MIT

## Settings

Moved to [settings](http://cookiecutter-django.readthedocs.io/en/latest/settings.html).

## Installation

### Docker

Build dev container with

`docker-compose -f local.yml up -d --build`

or for production (requires manual creation of `.envs/.production/.django`):

`docker-compose -f production.yml up -d --build`

### Local

1. Clone repo, setup virtual environment and install dependencies

first: 
```shell
git clone git@github.com:rl-institut/ReEnAct_web.git
cd ReEnAct_web
```
then set up your virtualenvironment with virtualenv (works well with python version 3.12) and then install dependencies with uv (should be faster): 
```shell
virtualenv reenact_venv
source reenact_venv/bin/activate
pip install uv
uv pip install -r ./requirements/local.txt
```
OR use uv ([documentation](https://docs.astral.sh/uv/pip/environments/)) for your virtual environment as well and then for installing dependencies:
```shell
pip install uv
uv reenact_venv --python 3.12
source reenact_venv/bin/activate
uv pip install -r ./requirements/local.txt
```
you can also use conda for setting up the venv, but it might cause problems with celery.

2. Setup local PostgreSQL server and configure using pgadmin4 (Linux)

- Install: `sudo apt install postgresql pgadmin4` (only if not already installed)
- Start pgadmin4
  - Create database "reenact_webapp"
  - Create user "reenact_user" with some password, e.g. "my_reenact_user_pass"
- Grant write permissions to this DB for the user
- Activate postGIS via SQL query: `CREATE EXTENSION postgis;`

3. Create `.env` file with the following content
```
# General
# ------------------------------------------------------------------------------
USE_DOCKER=yes
IPYTHONDIR=/app/.ipython
# Redis
# ------------------------------------------------------------------------------
REDIS_URL=redis://redis:6379/0

# Celery
# ------------------------------------------------------------------------------

CELERY_BROKER_URL=redis://redis:6379/0

# Flower
CELERY_FLOWER_USER=dVSdYOthZmldNnHOnGLAgKhnETvRbOXs
CELERY_FLOWER_PASSWORD=YbGI8ju9tsiODB0ACmcEGC1yMoOe3BI51PwV8niA6AH6oXLPMQ6Fahc3NWFHaQlK

# PostgreSQL
# ------------------------------------------------------------------------------
POSTGRES_HOST=postgres
POSTGRES_PORT=5432
POSTGRES_DB=reenact_webapp
POSTGRES_USER=reenact_user
POSTGRES_PASSWORD=my_reenact_user_pass

DATABASE_URL=postgres://reenact_user:my_reenact_user_pass@localhost:5432/reenact_webapp
```
(make sure you use the same password in `POSTGRES_PASSWORD` as in step 2)

4. Activate the `.env` file

Run `export DJANGO_READ_DOT_ENV=True;` - ff this fails, try `source .env`

Activate pre-commit:
```shell
pre-commit install
```

5. Migrate and start app

```shell
python manage.py migrate
python manage.py runserver
```

## Add dependencies

This can be done in `requirements/` folder by adding dependency to related *.in file and compile/lock dependencies.
Via `uv` (you must install uv first - recommended!):
```shell
uv pip compile -o requirements/local.txt requirements/local.in
uv pip compile -o requirements/production.txt requirements/production.in
```
or via `pip-compile` (you must install pip-tools first):
```shell
pip-compile -o requirements/local.txt requirements/local.in
pip-compile -o requirements/production.txt requirements/production.in
```

## Basic Commands

### Setting Up Your Users

- To create a **normal user account**, just go to Sign Up and fill out the form. Once you submit it, you'll see a "Verify Your E-mail Address" page. Go to your console to see a simulated email verification message. Copy the link into your browser. Now the user's email should be verified and ready to go.

- To create a **superuser account**, use this command:

      $ python manage.py createsuperuser

For convenience, you can keep your normal user logged in on Chrome and your superuser logged in on Firefox (or similar), so that you can see how the site behaves for both kinds of users.

### Type checks

Running type checks with mypy:

    $ mypy reenact

### Test coverage

To run the tests, check your test coverage, and generate an HTML coverage report:

    $ coverage run -m pytest
    $ coverage html
    $ open htmlcov/index.html

#### Running tests with pytest

    $ pytest

### Live reloading and Sass CSS compilation

Moved to [Live reloading and SASS compilation](https://cookiecutter-django.readthedocs.io/en/latest/developing-locally.html#sass-compilation-live-reloading).

### Celery

This app comes with Celery.

To run a celery worker:

```bash
cd reenact
celery -A config.celery_app worker -l info
```

Please note: For Celery's import magic to work, it is important _where_ the celery commands are run. If you are in the same folder with _manage.py_, you should be right.

To run [periodic tasks](https://docs.celeryq.dev/en/stable/userguide/periodic-tasks.html), you'll need to start the celery beat scheduler service. You can start it as a standalone process:

```bash
cd reenact
celery -A config.celery_app beat
```

or you can embed the beat service inside a worker with the `-B` option (not recommended for production use):

```bash
cd reenact
celery -A config.celery_app worker -B -l info
```

### Sentry

Sentry is an error logging aggregator service. You can sign up for a free account at <https://sentry.io/signup/?code=cookiecutter> or download and host it yourself.
The system is set up with reasonable defaults, including 404 logging and integration with the WSGI application.

You must set the DSN url in production.

## Deployment

The following details how to deploy this application.

### Docker

See detailed [cookiecutter-django Docker documentation](http://cookiecutter-django.readthedocs.io/en/latest/deployment-with-docker.html).
