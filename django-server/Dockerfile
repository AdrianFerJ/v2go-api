FROM python:3.7

ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get install -y \
    binutils \
    libproj-dev \
    gdal-bin

RUN mkdir /code
WORKDIR /code
COPY . /code/
EXPOSE 8000
RUN pip install -r requirements.txt

# Change workdir to /api_django/
# WORKDIR /code/api_django
# RUN python manage.py collectstatic --noinput