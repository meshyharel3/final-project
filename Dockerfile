# Use the official Python image from the Docker Hub
FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && \
    apt-get install -y software-properties-common git curl && \
    add-apt-repository ppa:deadsnakes/ppa && \
    apt-get update && \
    apt-get install -y python3.10 python3.10-venv python3.10-dev

RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.10 1 && \
    update-alternatives --install /usr/bin/python python /usr/bin/python3.10 1

RUN curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py && \
    python3 get-pip.py && \
    rm get-pip.py

# Set the working directory
WORKDIR /opt/status-page

# Copy the entire project
COPY . .
#COPY ./statuspage /app/statuspage

RUN bash upgrade.sh
# Expose the port that the app runs on
EXPOSE 8001

CMD ["/opt/status-page/venv/bin/gunicorn", "--pid" ,"/var/tmp/status-page.pid" ,"--pythonpath" ,"/opt/status-page/statuspage" ,"--config" ,"/opt/status-page/gunicorn.py", "statuspage.wsgi"]

