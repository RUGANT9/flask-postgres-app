from flask import Flask
import psycopg2
import os

app = Flask(__name__)

@app.route("/")
def index():
    try:
        conn = psycopg2.connect(
            dbname=os.environ["POSTGRES_DB"],
            user=os.environ["POSTGRES_USER"],
            password=os.environ["POSTGRES_PASSWORD"],
            host=os.environ["POSTGRES_HOST"],
            port=os.environ.get("POSTGRES_PORT", 5432)
        )
        return "✅ Connected to PostgreSQL and added the Jenkins CI/CD!! finally working"
    except Exception as e:
        return f"❌ Failed to connect: {e}"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
