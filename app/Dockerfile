FROM python:3.10-slim
WORKDIR /app
COPY . /app
RUN pip3 install flask psycopg2-binary
CMD ["python3", "app.py"]
