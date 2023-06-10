FROM python:3.10-slim-buster

RUN apt-get update \
    && apt-get upgrade -y

ENV DockerHOME=/home/app 
RUN mkdir -p $DockerHOME
WORKDIR $DockerHOME

# Force the stdout and stderr streams to be unbuffered.
# This allows log messages to be immediately dumped to Docker's stdout/stderr streams.
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip

# Install dependencies:
COPY requirements.txt $DockerHOME/requirements.txt
RUN pip install -r requirements.txt

# Copy project:
COPY django/ $DockerHOME/django/

# Copy entrypoint script:
COPY docker/django/entrypoint.sh $DockerHOME/server_entrypoint.sh
COPY docker/celery/entrypoint.sh $DockerHOME/worker_entrypoint.sh