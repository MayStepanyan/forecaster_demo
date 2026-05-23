FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install git+https://github.com/Leegoo-dev/Kronos.git

COPY . .

EXPOSE 8501
