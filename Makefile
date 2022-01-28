.PHONY: build install sh run down

build:
	docker-compose build

sh:
	docker-compose run --rm app bash

run:
	docker-compose up

down:
	docker-compose down

makemigrations:
	docker-compose run --rm app python manage.py makemigrations

migrate:
	docker-compose run --rm app python manage.py migrate

test:
	docker-compose run --rm app sh -c "python manage.py test && flake8"
