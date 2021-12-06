db-name=postgres
fixture-files = fixtures/users/users.json

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

django-shell:
	docker-compose exec backend bash -c "python manage.py shell_plus --ipython --print-sql"

format:
	docker-compose exec backend bash -c "isort . && black ."

recreate-db:
	docker-compose stop backend
	docker-compose exec db bash -c "runuser postgres -c 'dropdb $(db-name); createdb $(db-name)'"
	docker-compose start backend
	make migrations

load-fixtures:
	docker-compose exec -T backend bash -c "python manage.py loaddata $(fixture-files)"

test:
	docker-compose exec backend bash -c "python manage.py test $(location)"
