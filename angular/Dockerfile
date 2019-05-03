### Stage 1: Build
FROM node:11.4.0-alpine as builder

RUN mkdir /app
WORKDIR /app

# Copy app dependencies.
COPY angular-app/package.json angular-app/package-lock.json /app/angular-app/

# Install app dependencies.
RUN npm install --prefix angular-app

# Copy app files.
COPY . /app

# Build app
RUN npm run build --prefix angular-app -- --output-path=./dist/out

# Copy app files.
COPY . /app

# Build app
RUN npm run build --prefix angular-app -- --output-path=./dist/out

### Stage 2: Delivery
FROM nginx:1.15.7-alpine

RUN rm -rf /usr/share/nginx/html/*

COPY --from=builder /app/angular-app/dist/out /usr/share/nginx/html

COPY ./nginx/nginx.conf /etc/nginx/conf.d/default.conf
