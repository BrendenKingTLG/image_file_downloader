FROM python:3.9-slim

WORKDIR /app

COPY --chmod=777 download_files.py .
COPY --chmod=777 upload_files.py .
COPY --chmod=777 last_downloaded.txt .

RUN pip install --no-cache-dir boto3

RUN python ./download_files.py

CMD sleep 1000
