FROM python:3.9.0-alpine

WORKDIR /code/app

# Install necessary build dependencies
RUN apk add --no-cache gcc musl-dev libffi-dev rust cargo

COPY ./requirements.txt /code/requirements.txt

# Upgrade pip first
RUN pip install --upgrade pip

ENV PYTHONPATH=/code

# Install dependencies
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./app /code/app

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
