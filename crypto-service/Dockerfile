FROM python:3.8.16-bullseye

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY ./app /app
WORKDIR /app

COPY ./requirements.txt /app/
#RUN apk add libc-dev build-base postgresql-dev libpq


RUN pip install -r requirements.txt
RUN pip install pandas
RUN pip install pymeeus ujson korean-lunar-calendar hijri-converter ephem convertdate setuptools-git pystan==2.19.1.1 LunarCalendar holidays cmdstanpy
RUN pip install prophet

COPY ./entrypoint.sh /
ENTRYPOINT ["sh", "/entrypoint.sh"]