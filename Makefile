start:
	python manage.py runserver

stop: docker-down

docker-up:
	docker-compose up -d

docker-down:
	docker-compose down --remove-orphans

docker-build:
	docker-compose build

venv:
	. venv_ubuntu/bin/activate

collectstatic:
	python manage.py collectstatic

migrate:
	python manage.py makemigrations
	python manage.py migrate

superuser:
	python manage.py createsuperuser --noinput

loaddata:
	python manage.py loaddata category
	python manage.py loaddata product

restore-db:
	rm -f db.sqlite3
	rm -fr mainapp/migrations
	mkdir mainapp/migrations
	touch mainapp/migrations/__init__.py
	rm -fr basketapp/migrations
	mkdir basketapp/migrations
	touch basketapp/migrations/__init__.py
	make migrate
	make superuser
	make loaddata