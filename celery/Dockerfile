FROM python:3.10-slim

WORKDIR /app

COPY ./celery/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Add wait-for-it script
ADD https://raw.githubusercontent.com/vishnubob/wait-for-it/master/wait-for-it.sh /wait-for-it.sh
RUN chmod +x /wait-for-it.sh

COPY ./celery/rethinkdb_init.py .
COPY ./fraud_detection_backend/app /app/app
COPY ./fraud_detection_backend/config /app/config

ENV PYTHONPATH=/app

CMD ["/wait-for-it.sh", "postgresdb:5432", "--", "/wait-for-it.sh", "rethinkdb:28015", "--", "bash", "-c", "python rethinkdb_init.py && celery -A app.celery_app worker --loglevel=info"]
