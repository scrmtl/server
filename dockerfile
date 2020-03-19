FROM python:3.9
# for django that use postgresSql
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        postgresql-client \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /usr/src/app
# TODO path to requirements.txt
COPY requirements.txt ./
RUN pip install -r requirements.txt
# TODO first param, where is the python app
COPY . .

EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]