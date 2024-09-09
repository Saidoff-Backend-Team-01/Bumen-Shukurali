FROM python:3.10-slim


WORKDIR /app


COPY . .

RUN pip install -r requirements.txt

EXPOSE 8888

CMD ["gunicorn", "--bind", "0.0.0.0:8888", "core.wsgi:application"]