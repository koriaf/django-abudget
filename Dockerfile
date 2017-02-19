FROM python:3.5
ENV PYTHONUNBUFFERED 1

RUN mkdir /src
RUN mkdir /static_root
WORKDIR /src

ADD system/requirements_docker.txt /src/requirements_docker.txt
ADD node_modules /src/var/node_modules

RUN pip install -r /src/requirements_docker.txt
