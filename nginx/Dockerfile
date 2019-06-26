# Dockerfile
FROM nginx:1.15.12-alpine

RUN rm /etc/nginx/conf.d/default.conf
COPY nginx.conf /etc/nginx/conf.d

# Copy angular build to be served by nxinx (temporary)
COPY angular_dist/html /usr/share/nginx/angular/html
