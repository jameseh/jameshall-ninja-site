FROM python:3.11-slim

WORKDIR /

COPY . .

RUN pip install -r requirements.txt

EXPOSE 443

WORKDIR SanicPlus

CMD ["python", "app.py"]
