FROM python:3.11-slim-bullseye
EXPOSE 80
WORKDIR /app
RUN apt-get update && apt-get -y install libpq-dev gcc
COPY pyproject.toml poetry.lock poetry.toml /app/
RUN pip install poetry && poetry install  --no-cache
COPY . /app
RUN python manage.py collectstatic

ENTRYPOINT ["bash", "entrypoint.sh"]


