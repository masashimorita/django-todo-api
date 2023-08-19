# django-todo-api
Manage Todo of yours!

# Requirements

- Python 3.11.4
- Django 4.2.3
- djangorestframework 3.14.0
- flake8 6.0.0

※ This project uses `requirements.txt` as package management

# Project Setup

1. Building a docker image
    ```bash
    $ make build
    ```

2. Migrate Database
    ```bash
    $ make migrate
    ```

3. Start docker container
    ```bash
    $ make up
    ```

4. Stop docker container
    ```bash
    $ make down
    ```

# Useful commands

- Log into app container
    ```bash
    $ make sh
    ```
- Make migrations for new model
    ```bash
    $ make migration
    ```
- Run unit test
    ```bash
    $ make test
    ```
- Run lint
    ```bash
    $ make lint
    ```
