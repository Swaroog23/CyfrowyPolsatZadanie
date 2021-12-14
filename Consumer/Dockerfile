# syntax=docker/dockerfile:1
FROM python:3.9.7
ENV PYTHONUNBUFFERED=1
WORKDIR /Consumer
COPY . ./Consumer
RUN pip install -r Consumer/requirements.txt
CMD python3 Consumer/worker.py