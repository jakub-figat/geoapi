db-name=postgres
fixture-files =

build-dev:
	-cp -n ./config/.env.template ./config/.env
	docker-compose build

migrations:
	docker-compose exec backend bash -c "python manage.py makemigrations && python manage.py migrate"

up-dev:
	docker-compose run --rm backend bash -c "python manage.py migrate"
	docker-compose up

backend-bash:
	docker-compose exec backend bash

format:
	docker-compose exec backend bash -c "isort . && black ."

recreate-db:
	docker-compose stop backend
	docker-compose exec db bash -c "runuser postgres -c 'dropdb $(db-name); createdb $(db-name)'"
	make migrations
	docker-compose start backend

test:
	docker-compose exec backend bash -c "python manage.py test $(location)"
