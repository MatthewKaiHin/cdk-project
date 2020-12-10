FROM python:3.6-alpine

RUN adduser -D microblog

WORKDIR /microblog


COPY requirements.txt requirements.txt
RUN apk add --no-cache --update gcc musl-dev libffi-dev openssl-dev
RUN python3 -m venv venv
RUN pip3 install --upgrade pip setuptools==45.2.0
RUN pip3 install -r requirements.txt

COPY app app
COPY migrations migrations
COPY microblog.py config.py run.py boot.sh ./

ENV FLASK_APP run.py

RUN chown -R microblog:microblog ./
USER microblog
RUN chmod u+x boot.sh

EXPOSE 8080

ENTRYPOINT ["./boot.sh"]