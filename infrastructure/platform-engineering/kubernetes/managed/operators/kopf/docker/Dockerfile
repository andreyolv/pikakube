FROM python:3.9.16-bullseye

RUN apt-get update -y
RUN apt-get install -y curl vim

COPY requirements.txt .
RUN pip install --upgrade pip \
    && pip install -r requirements.txt

COPY . .

CMD ["kopf", "run", "operator.py"]