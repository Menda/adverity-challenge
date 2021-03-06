#!/bin/bash
# This script can be used by the developer or the CI/CD to run the tests.

if [ -z "$REQUIREMENTS_INSTALLED" ]; then
    pip install -r requirements/testing.txt
    export REQUIREMENTS_INSTALLED="true"
fi

flake8 .
mypy --cache-dir /tmp/.mypy_cache .

bash scripts/wait-for-it.sh $POSTGRES_HOST:$POSTGRES_PORT -t 30

python manage.py test
