FROM python:3.10.4-alpine3.15

RUN  apk add --no-cache --virtual=build-dependencies g++ gcc make libffi-dev

RUN pip install pandas
