import json
import os

import boto3
import pymysql
from flask import Flask

app = Flask(__name__)

AWS_REGION = os.environ.get("AWS_REGION", "us-east-1")
SECRET_NAME = os.environ.get("SECRET_NAME", "rds-secret")


def get_database_secret():
    client = boto3.client(
        "secretsmanager",
        region_name=AWS_REGION
    )

    response = client.get_secret_value(
        SecretId=SECRET_NAME
    )

    return json.loads(response["SecretString"])


def get_connection():
    secret = get_database_secret()

    return pymysql.connect(
        host=secret["host"],
        user=secret["username"],
        password=secret["password"],
        database=secret["dbname"],
        port=int(secret.get("port", 3306)),
        cursorclass=pymysql.cursors.DictCursor
    )


@app.route("/")
def home():
    return "Production Flask Application"


@app.route("/health")
def health():
    return {
        "status": "healthy"
    }


@app.route("/db")
def database():
    connection = get_connection()

    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) AS count FROM users")
            result = cursor.fetchone()

        return {
            "database": "connected",
            "users": result["count"]
        }

    finally:
        connection.close()


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=8000
    )