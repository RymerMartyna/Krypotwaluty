FROM python:3.8.16-bullseye

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY ./app /app
WORKDIR /app

COPY ./requirements.txt /app/
#RUN apk add libc-dev build-base postgresql-dev libpq


RUN pip install -r requirements.txt
RUN pip install prophet

COPY ./entrypoint.sh /
ENTRYPOINT ["sh", "/entrypoint.sh"]