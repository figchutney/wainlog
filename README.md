# `wainlog` ⛰

![main](https://github.com/figchutney/wainlog/actions/workflows/main.yml/badge.svg)

👉 **Go have a play at https://wainlog-8drtz.ondigitalocean.app/** _(if you get a server error, try re-loading - Digital Ocean seems to be playing games with me)_

A simple place to keep track of which Wainright's you've climbed in the Lake District ⛰

This app is not production ready yet (I've not written tests yet, or cleaned up some mucky typing). However, you can access a test deployment of it [here](https://wainlog-8drtz.ondigitalocean.app/) - hosted on Digital Ocean's App Platform - or run a local instance following the instructions below (though Google OAuth won't work locally) 🤸‍♀️

https://github.com/figchutney/wainlog/assets/52138939/8323aa87-42a2-4e5d-836f-6cb7e2602bd1

- [`wainlog` ⛰](#wainlog-)
  - [1 - Description](#1---description)
  - [2 - Setup](#2---setup)
    - [2.1 - Basics](#21---basics)
    - [2.2 - Create a DB Locally](#22---create-a-db-locally)
    - [2.3 - Config](#23---config)
  - [3 - Development](#3---development)
    - [3.1 - Running the App](#31---running-the-app)
    - [3.2 - Migrations](#32---migrations)
    - [3.3 - Formatting / Style](#33---formatting--style)
    - [3.4 - Linting](#34---linting)
    - [3.5 - Typing](#35---typing)
    - [3.6 - Tests](#36---tests)
    - [3.7 - CI/CD](#37---cicd)
    - [3.8 - Deployment](#38---deployment)

## 1 - Description

`wainlog` allows you to keep track of which of which Wainright fells you've climbed in Lake District (incl. *when* you climbed each one). It also acts as a place to view general information about the fells (height, height rank, OS grid references etc.).

User management is via Google OAuth.

A focus has been kept on keeping the app clean and simple to use, with no unnecessary fells (hehe) and whistles.

## 2 - Setup

### 2.1 - Basics

- clone the repo
- make sure you're using Python 3.11 ([asdf](https://asdf-vm.com/#/) is good for managing multiple versions)
- [install Postgres14](https://formulae.brew.sh/formula/postgresql@14) (`brew install postgresql@14 should do the trick)
- create a virtual environment and install requirements from `requirements-dev.txt` - with the project as my current working directory, I tend to always just do:

```zsh
rm -rf .env; python -m venv .env; source .env/bin/activate; python -m pip install -U pip; python -m pip install -r requirements-dev.txt;
```

### 2.2 - Create a DB Locally

Create a new database for `wainlog`:

```zsh
psql postgres -c 'CREATE DATABASE wainlog'
```

Migrate the database to the latest version:

```zsh
PYTHONPATH=. ALEMBIC_DB_URL=postgresql:///wainlog alembic upgrade head
```

### 2.3 - Config

You can use a simple JSON file for storing dummy secrets when developing locally. Add a `.json` file called `wainlog-secrets.json` at root level:

```zsh
touch wainlog-secrets.json`
```

Add the following to the file:

```json
{   
  "DB_URL": "postgresql://localhost/wainlog",
  "GOOGLE_OAUTH_CLIENT_ID": "",
  "GOOGLE_OAUTH_CLIENT_SECRET": "",
  "SECRET_KEY": "this-is-a-bad-key"
}
```

It's probably obvious, but it's worth pointing out that these aren't the credentials that will be used in production.

## 3 - Development

### 3.1 - Running the App

- run the app with `flask run`
- navigate to `localhost:5000` in your browser

### 3.2 - Migrations

`alembic` is used for database migrations. If you change the database structure, generate a new version with `alembic`:

```zsh
PYTHONPATH=. ALEMBIC_DB_URL=postgresql:///wainlog alembic revision --autogenerate -m 'some boring short description'
```

This will chuck out a migration script to `alembic/versions/` - check it all looks good, and then migrate your local database with:

```zsh
PYTHONPATH=. ALEMBIC_DB_URL=postgresql:///wainlog alembic upgrade head
```

### 3.3 - Formatting / Style

[`black`](https://github.com/psf/black) is used for formatting, with a max line length of 79. [`isort`](https://pycqa.github.io/isort/) is used for sorting imports.

- format code with `bin/format`

### 3.4 - Linting

[`flake8`](https://flake8.pycqa.org/en/latest/) is used for linting, with a line length of 79.

- run linting checks with `bin/check`

### 3.5 - Typing

[`mypy`](http://mypy-lang.org/) is used to enforce the use of [typehints](https://www.python.org/dev/peps/pep-0484/) and check for type safety.

- run type checks with `bin/check`

### 3.6 - Tests

[`pytest`](https://docs.pytest.org/en/stable/index.html) is used for testing. Minimum test coverage is 100%. Tests live in `tests/` and will only be run by `pytest` if the module and function name is prefixed with `test_`. 

- run tests with `pytest tests`

### 3.7 - CI/CD

Whenever you push a new commit, the `CI` GitHub action (defined in `.github/workflows/main.yml`) will run, which:

- uses Python 3.11
- installs dependences from `requirements-dev.txt`
- checks imports with `isort`
- checks formatting with `black`
- lints code with `flake8`
- checks code scurity with `bandit`
- checks dependency security with `safety`
- checks type safety with `mpypy`
- runs tests in `tests/` with `pytest`

Pull requests can only be merged if the CI checks all pass.

The repo is hooked up with Digital Ocean's App Platform, so when a merge is made to `main` branch, it triggers a build and deployment in Digital Ocean (more below).

### 3.8 - Deployment

`wainlog` is deployed using Digital Ocean's App Platform. For now, the DB is just their cheapy test one they provide by default for test apps.

The deployment is configured with two files in the root directory of the project:

- `gunicorn_config.py`
- `runtime.txt` (tells Digital Ocean to use Python 3.11)
