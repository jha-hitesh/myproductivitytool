#!/bin/bash

dir="$PWD"
cur=${PWD##*/}


if [ "$1" == "migrate_models" ]; then
	echo -e "Executing makemigrations followed by migrate..."
	python manage.py makemigrations common project
	python manage.py migrate


elif [ "$1" == "showmigrations" ]; then
	echo -e "Showing migrations..."
	python manage.py showmigrations


elif [ "$1" == "shell" ]; then
	echo -e "Opening ipython..."
	python manage.py shell


elif [ "$1" == "collectstatic" ]; then
	python manage.py collectstatic --noinput


elif [ "$1" == "up" ]; then
	python manage.py runserver	


elif [ "$1" == "deletemigrations" ]; then
	echo -e "Deleting Migrations Folders"
	sudo rm -rf myroductivitytool/common/migrations/
	sudo rm -rf myroductivitytool/project/migrations/

else
	echo -e "This command is not yet supported"

fi