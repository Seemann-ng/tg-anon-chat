FROM python:3.12
LABEL authors="Seemann-ng"

COPY requirements.txt /app/requirements.txt
RUN pip3 install -r /app/requirements.txt

COPY credentials.py /app/credentials.py
COPY bot /app/bot
COPY dbtokenshandler /app/dbtokenshandler

WORKDIR /app/bot

ENV PYTHONPATH="${PYTHONPATH}:/app"
ENV PYTHONUNBUFFERED=1

CMD ["python", "main.py"]
