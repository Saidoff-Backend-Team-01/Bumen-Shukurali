#!/usr/bin/make

include .env

define SERVERS_JSON
{
	"Servers": {
		"1": {
			"Name": "Dastyor",
			"Group": "Servers",
			"Host": "$(DATABASE_HOST)",
			"Port": "$(DB_PORT)",
			"MaintenanceDB": "postgres",
			"Username": "$(DATABASE_PASSWORD)",
			"SSLMode": "prefer",
			"PassFile": "/tmp/pgpassfile"
		}
	}
}
endef
export SERVERS_JSON
export PYTHONPATH=:$(PWD)


help:
	@echo "make"
	@echo "	hello"
	@echo "		print hello world"
	@echo "	init-locale"
	@echo "		Initialize locale messages: make update-locale ARGS='ru'"

hello:
	echo "Hello, World"
run:
	python3 manage.py runserver
migrations:
	python3 manage.py makemigrations
migrate:
	python3 manage.py migrate
createsuperuser:
	python3 manage.py createsuperuser
lint:
	./bin/lint
test:
	pytest
initial-db:
	python3 manage.py populate_db
