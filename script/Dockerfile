FROM python:latest

WORKDIR /script/src

COPY ./ /script

COPY requirements.txt /script

RUN apt-get update && apt-get install -y python3-pip
RUN pip install -r /script/requirements.txt

RUN chmod +x /script/src/controller.py

CMD ["uvicorn", "controller:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]