FROM alpine

RUN apk add --no-cache --virtual=build-dependencies g++ gcc make libffi-dev
RUN apk add py3-pip
RUN apk add py3-pandas
RUN pip install dash
RUN pip install coverage
RUN pip install pylint
RUN pip install pytest
RUN pip install paramiko
