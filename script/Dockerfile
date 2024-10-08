FROM python:3.11

WORKDIR /script/src

COPY ./ /script

RUN apt-get update && apt-get install -y \
    build-essential \
    python3-pip \
    gcc \
    libffi-dev \
    libpq-dev \
    libssl-dev \
    libuv1-dev && \
    pip install --upgrade pip && \
    pip install -r /script/requirements.txt

RUN chmod +x /script/src/controller.py

CMD ["sh", "-c", "sleep 5 && uvicorn controller:app --host 0.0.0.0 --port 8000 --reload"]
