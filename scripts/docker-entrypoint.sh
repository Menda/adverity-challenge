#!/bin/bash
# This script must not be used for production.

bash scripts/wait-for-it.sh $POSTGRES_HOST:$POSTGRES_PORT -t 30

echo $(date -u) "- Applying migrations"
python manage.py migrate

echo $(date -u) "- Running the server"
python manage.py runserver 0.0.0.0:8000
