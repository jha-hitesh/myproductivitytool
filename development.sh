#!/bin/bash

dir="$PWD"
cur=${PWD##*/}


elif [ "$1" == "migrate_schemas" ]; then
	echo -e "Executing makemigrations followed by migrate..."
	python manage.py makemigrations customer common personnel claims taskapp --settings=config.settings --configuration=Development
	python manage.py migrate_schemas --executor=parallel --settings=config.settings --configuration=Development


elif [ "$1" == "showmigrations" ]; then
	echo -e "Showing migrations..."
	python manage.py showmigrations --settings=config.settings --configuration=Development


elif [ "$1" == "shell" ]; then
	echo -e "Opening ipython..."
	python manage.py shell --settings=config.settings --configuration=Development


elif [ "$1" == "tenant_shell" ]; then
	echo -e "Running schema specific command"
	python manage.py tenant_command shell --schema="$2" --settings=config.settings --configuration=Development


elif [ "$1" == "collectstatic" ]; then
	python manage.py collectstatic --noinput --settings=config.settings --configuration=Development


elif [ "$1" == "test" ]; then
	echo -e "Executing test cases..."
	python manage.py test tenant_schemas.test services --keepdb --settings=config.settings.test --settings=config.settings --configuration=Development


elif [ "$1" == "start_celery" ]; then
	echo -e "Starting celery workers..."
	celery worker -A myroductivitytool.taskapp.celery

else
	echo -e "This command is not yet supported"

fi