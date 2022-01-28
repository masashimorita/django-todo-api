# django-todo-api
Manage Todo of yours!

# Requirements

- Docker 20.10.6
- Docker Compose 2.0.0-beta.1
- pip 21.2.4
- Python 3.10.2

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
    $ make run 
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
    $ make makemigrations
    ```
- Run unit test
    ```bash
    $ make test
    ```
