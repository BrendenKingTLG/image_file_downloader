FROM python:3.9-slim

WORKDIR /app

COPY download_files.py .
COPY last_downloaded.txt .

RUN pip install --no-cache-dir boto3

RUN ./download_files.py

CMD sleep 1000
