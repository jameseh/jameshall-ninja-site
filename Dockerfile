FROM python:3.11-slim

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

ENV PYTHONPATH=.

CMD ["python", "app.py"]
