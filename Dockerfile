FROM alpine

RUN apk add --no-cache --virtual=build-dependencies g++ gcc make libffi-dev
RUN apk add py3-pip
RUN apk add py3-pandas
RUN pip install dash
RUN pip install coverage
RUN pip install pylint
RUN pip install pytest
RUN pip install paramiko

COPY script /app/script

EXPOSE 8080

ENTRYPOINT ["python", "/app/script/web_app/app.py"]
