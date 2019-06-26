FROM python:3.7

# set work directory
WORKDIR /usr/src/app

# set environment varibles
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install tools required for project
RUN apt-get update \
    && apt-get install -y \
    binutils \
    libproj-dev \
    gdal-bin

# Install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt /usr/src/app/requirements.txt
RUN pip install -r requirements.txt

COPY ./entrypoint.prod.sh /usr/src/app/entrypoint.prod.sh

# Copy project
COPY ./api_django /usr/src/app/api_django
WORKDIR /usr/src/app/api_django

# Run entrypoint.sh
# ENTRYPOINT ["/usr/src/app/entrypoint.prod.sh"]
