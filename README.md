# BlogFlask

## About Project

Blog project using Flask with the ability to create users, articles, tags and comments.

## Features
- **[Python](https://www.python.org/)** (version 3.11)
- **[Flask](https://flask.palletsprojects.com/en/2.3.x/)**
- **[PostgreSQL](https://www.postgresql.org/)**
- **[SQLAlchemy](https://www.sqlalchemy.org/)**
- **[Alembic](https://alembic.sqlalchemy.org/en/latest/)**
- **[Docker Compose](https://docs.docker.com/compose/)**
- **[Redis](https://redis.io/)**

## Quickstart

First, clone project

``` 
git clone https://github.com/Niolum/BlogFlask.git
```

Then, create .env file. set environment variables and create database.

Example ``.env``:

```
SECRET_KEY = some_secret_key

DBUSER = some_user
DBPASS = some_password
DBHOST = localhost
DBNAME = some_name_db

CACHE_TYPE=RedisCache
CACHE_REDIS_HOST=redis
CACHE_REDIS_PORT=6379
CACHE_REDIS_DB=0
CACHE_REDIS_URL=redis://localhost:6379/0
CACHE_DEFAULT_TIMEOUT=500
```

Further, set up the virtual environment and the main dependencies from the ``requirements.txt``

```
python -m venv venv
source venv/bin/activate 
# or for windows
venv/Scripts/activate 
pip install -r requirements.txt
```

Before starting, you need to execute several commands:

```
flask --app run db upgrade
```

Run application:

```
python run.py
```

For start in docker-compose change .env:

```
SECRET_KEY = some_secret_key

DBUSER = some_user
DBPASS = some_password
DBHOST = postgres
DBNAME = some_name_db

POSTGRES_USER = some_user
POSTGRES_PASSWORD = some_password
POSTGRES_DB = some_name_db

CACHE_TYPE=RedisCache
CACHE_REDIS_HOST=redis
CACHE_REDIS_PORT=6379
CACHE_REDIS_DB=0
CACHE_REDIS_URL=redis://redis:6379/0
CACHE_DEFAULT_TIMEOUT=500
```

Before running docker-compose:

```
docker volume create blogdb
```

To start the project, use the following command:

```
docker-compose up -d
```