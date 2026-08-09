# start from Python 3.x base image
FROM python:3.8-alpine

RUN apk update \
    && apk add apache2-utils \
    && apk add bash \
    && mkdir /pypi-server 

WORKDIR /pypi-server

#creating packages directory and Authentication Directory
RUN mkdir packages \
    && mkdir auth

#Installing pypi server and pass lib module for authentication
RUN python3 -m pip install pypiserver passlib
COPY ./docker_entry.sh /pypi-server

#Making the entrypoint file executable
RUN chmod +rx ./docker_entry.sh
ENTRYPOINT ["/pypi-server/docker_entry.sh"]
EXPOSE 80