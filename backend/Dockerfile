FROM python:alpine3.16

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY mysite /app
WORKDIR /app

COPY ./requirements.txt /app/
RUN apk add build-base postgresql-dev libpq && pip3 install -r requirements.txt

COPY ./entrypoint.sh /
ENTRYPOINT ["sh", "/entrypoint.sh"]
EXPOSE 8000