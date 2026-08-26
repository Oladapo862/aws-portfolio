FROM python:3.12-slim

WORKDIR /app

COPY flask/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY flask/app.py .

EXPOSE 8000

CMD ["python", "app.py"]
