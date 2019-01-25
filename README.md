# v2go-web-ap
V2go web app's repo contains client and server apps (django angular), and infastructure setup for both apps, postgres, redis, and nginx using docker 


## PROJECT SET UP

### Python and django
**Required:** Python3.7 (doesn't need to be the default system python) and pip

```bash
# install pipenv
$ pip install pipenv

# create venv and activate it
$ pipenv --python 3.7  # or path/to/python if no python 
$ pipenv shell

# Make sure pip is not v18.1, while venv is active.(Known issue with v18.1, fix src: https://github.com/pypa/pipenv/issues/2924)
$ (venv) pip --version

# IF pip==18.1, THEN downgrade to 18.0 (from within venv)
$ (venv) pip install pipenv
$ (venv) pipenv run pip install pip==18.0

# If pip ==18.0 and Pipfile available,  then install packages
$ (venv) pipenv install

# IF not using pipenv or no Pipfile already available, use this to install packages
$ (vevn) pip install \
              channels==2.1.2 \
              channels-redis==2.3.0 \
              Django==2.1.5 \
              djangorestframework==3.8.2 \
              nose==1.3.7 \
              Pillow==5.2.0 \
              pytest-asyncio==0.9.0 \
              pytest-django==3.4.2
```