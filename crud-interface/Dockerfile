FROM python:3.9-slim

WORKDIR /code/app

# Install necessary build dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    python3-dev \
    libffi-dev \
    libssl-dev \
    && rm -rf /var/lib/apt/lists/*

COPY ./requirements.txt /code/requirements.txt

# Upgrade pip first
RUN pip install --upgrade pip

ENV PYTHONPATH=/code

# Install dependencies
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./app /code/app

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
