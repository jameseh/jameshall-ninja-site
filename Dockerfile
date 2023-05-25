FROM python:3.11-slim

WORKDIR ./SanicPlus

COPY . .

RUN pip install -r requirements.txt

EXPOSE 443

CMD ["python", "app.py"]
