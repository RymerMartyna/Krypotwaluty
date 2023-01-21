FROM python:3.11
WORKDIR /app
COPY deployment/requirements/app.requirements.txt ./requirements.txt
RUN pip install -r requirements.txt && rm requirements.txt

COPY src .
EXPOSE 8000

CMD ./manage.py runserver --insecure 0.0.0.0:8000
