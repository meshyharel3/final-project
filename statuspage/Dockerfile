# Dockerfile.nginx
FROM nginx:latest

# Create application directory
#RUN mkdir -p /opt/status-page/statuspage/static
RUN mkdir -p /opt/status-page/statuspage/statuspage/static
# Copy the static files for css styling
COPY ./statuspage/static/ /opt/status-page/statuspage/statuspage/static

# Copy your custom NGINX config to the container
COPY ./nginx/nginx.conf /etc/nginx/conf.d/default.conf

# Add SSL certificates
COPY ./certs/status-page.crt /etc/ssl/certs/
COPY ./certs/status-page.key /etc/ssl/private/
