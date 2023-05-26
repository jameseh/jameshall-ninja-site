FROM python:3.11-slim

WORKDIR /

COPY . .

RUN pip install -r requirements.txt

EXPOSE 8080

WORKDIR SanicPlus

CMD ["python", "app.py"]
