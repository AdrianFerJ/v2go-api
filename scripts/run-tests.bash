#!/usr/bin/env bash

# if any command inside script returns error, exit and return that error 
set -e

# magic line to ensure that we're always inside the root of our application,
# no matter from which directory we'll run script
# thanks to it we can just enter `./scripts/run-tests.bash`
cd "${0%/*}/.."
cd "django-server"
# pipenv shell

cd api_django

./manage.py test main.tests volt_finder.tests volt_reservation.tests

if [ $? -eq 0 ]; then
    echo "Passed!" && exit 0
else
    echo "Failed!" && exit 1
fi
