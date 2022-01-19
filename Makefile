docker-up:
	docker-compose up -d

docker-down:
	docker-compose down --remove-orphans

docker-build:
	docker-compose build

venv:
	. venv_ubuntu/bin/activate

start:
	python3.10 manage.py runserver

collectstatic:
	python3.10 manage.py collectstatic

migrate:
	python3.10 manage.py makemigrations
	python3.10 manage.py migrate

superuser:
	python3.10 manage.py createsuperuser --noinput

loaddata:
	python3.10 manage.py loaddata category
	python3.10 manage.py loaddata product

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