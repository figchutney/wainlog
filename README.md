# `wainlog` ⛰

A simple place to keep track of which Wainright's you've climbed in the Lake District ⛰

This app is currently a work in progress, and is not production ready (I've not written tests yet, or cleaned up some mucky typing). However, you can still run a local instance of the app nicely - see instructions below on getting set up 🤸‍♀️

https://user-images.githubusercontent.com/52138939/119268061-150ed600-bbe9-11eb-896b-9b4acd4a9b9e.mov

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

A focus has been kept on keeping the app clean and simple to use, with no unnecessary fells (hehe) and whistles.

## 2 - Setup

### 2.1 - Basics

- clone the repo
- make sure you're using Python 3.8 ([asdf](https://asdf-vm.com/#/) is good for managing multiple versions)
- [install Postgres11](https://formulae.brew.sh/formula/postgresql@9.5#default) (`brew install postgresql@11 should do the trick)
- create a virtual environment and install requirements from `requirements-dev.txt` - with the project as my current working directory, I tend to always just do:

```zsh
rm -rf .env; python -m venv .env; source .env/bin/activate; python -m pip install -U pip; python -m pip install -r requirements-dev.txt;
```

### 2.2 - Create a DB Locally

Create a new database for `wainlog`:

```zsh
psql postgres -c 'CREATE DATABSE wainlog'
```

Migrate the database to the latest version:

```zsh
PYTHONPATH=. ALEMBIC_DB_URL=postgresql:///industry_ops alembic upgrade head
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

- uses Python 3.8
- installs dependences from `requirements-dev.txt`
- checks imports with `isort`
- checks formatting with `black`
- lints code with `flake8`
- checks code scurity with `bandit`
- checks dependency security with `safety`
- checks type safety with `mpypy`
- runs tests in `tests/` with `pytest`

Pull requests can only be merged if the CI checks all pass.

The repo will eventually be hooked up with Heroku, so when a merge is made to `main` branch, it triggers a build and deployment in Heroku (more below).

### 3.8 - Deployment

`wainlog` will be deployed using Heroku on a free Dyno.

Heroku will be hooked up with the GitHub repo so that merges to `main` trigger a build in Heroku, which will result in in a deployment if successful.

The deployment is configured with two files in the root directory of the project:

- `Procfile` (runs the app with `gunicorn`)
- `runtime.txt` (tells Heroku to use Python 3.8)
