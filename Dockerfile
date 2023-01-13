FROM alpine

RUN apk add --no-cache --virtual=build-dependencies g++ gcc make libffi-dev
RUN apk add py3-pip
RUN apk add py3-pandas
RUN pip install dash
RUN pip install paramiko

COPY script /app/script
WORKDIR /app/script/web_app

EXPOSE 8050/tcp

ENTRYPOINT ["python3", "/app/script/web_app/app.py"]
