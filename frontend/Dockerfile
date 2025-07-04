FROM python:3.10-slim

WORKDIR /app

COPY pyproject.toml .
RUN pip install --upgrade pip && pip install -e .

COPY . .
